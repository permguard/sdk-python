# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from concurrent import futures
from typing import Iterator, Tuple

import grpc
import pytest

from permguard import Client, EvaluateRequest, Evaluation, Refusal
from permguard._grpc_transport import _grpc_class
from permguard._wire import MAX_EXACT_PROTO_INTEGER, request_to_dict, request_to_proto
from permguard.data.v1 import pdp_pb2, pdp_pb2_grpc


class PDP(pdp_pb2_grpc.PolicyDecisionPointServicer):
    def Evaluate(
        self,
        request: pdp_pb2.EvaluateRequest,
        context: grpc.ServicerContext,
    ) -> pdp_pb2.EvaluateResponse:
        if request.ledger == 'bad':
            context.set_trailing_metadata(
                (('permguard-error-class', 'validation'), ('permguard-error-code', 'ledger_invalid'))
            )
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'bad ledger')
        return pdp_pb2.EvaluateResponse(
            decision=True,
            request_id=request.request_id,
            context=pdp_pb2.DecisionContext(policies=['policy-1']),
        )

    def EvaluateMany(
        self,
        request: pdp_pb2.EvaluateRequest,
        _context: grpc.ServicerContext,
    ) -> pdp_pb2.EvaluateResponse:
        return pdp_pb2.EvaluateResponse(
            decision=False,
            evaluations=[
                pdp_pb2.Decision(decision=True, request_id='one'),
                pdp_pb2.Decision(decision=False, request_id='two'),
            ],
        )

    def GetConfiguration(
        self,
        _request: pdp_pb2.GetConfigurationRequest,
        _context: grpc.ServicerContext,
    ) -> pdp_pb2.GetConfigurationResponse:
        return pdp_pb2.GetConfigurationResponse(
            interface='permguard.api.pdp.native.v1',
            pdp='grpc://test',
        )


@pytest.fixture
def grpc_endpoint() -> Iterator[Tuple[str, grpc.Server]]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    pdp_pb2_grpc.add_PolicyDecisionPointServicer_to_server(PDP(), server)  # type: ignore[no-untyped-call]
    port = server.add_insecure_port('127.0.0.1:0')
    server.start()
    try:
        yield f'grpc://127.0.0.1:{port}', server
    finally:
        server.stop(grace=None).wait(timeout=5)


def test_grpc_native_contract(grpc_endpoint: Tuple[str, grpc.Server]) -> None:
    service = pdp_pb2.DESCRIPTOR.services_by_name['PolicyDecisionPoint']
    assert service.full_name == 'permguard.data.v1.PolicyDecisionPoint'
    endpoint, _ = grpc_endpoint
    with Client(endpoint) as client:
        response = client.evaluate(EvaluateRequest(zone='acme', ledger='documents', request_id='r1'))
        batch = client.evaluate_many(
            EvaluateRequest(zone='acme', ledger='documents', evaluations=[Evaluation(), Evaluation()])
        )
        configuration = client.get_configuration()

    assert response.decision is True
    assert response.request_id == 'r1'
    assert response.context is not None
    assert response.context.policies == ['policy-1']
    assert batch.decision is False
    assert len(batch.evaluations) == 2
    assert configuration.interface == 'permguard.api.pdp.native.v1'


def test_grpc_refusal_is_structured(grpc_endpoint: Tuple[str, grpc.Server]) -> None:
    endpoint, _ = grpc_endpoint
    with Client(endpoint) as client, pytest.raises(Refusal) as caught:
        client.evaluate(EvaluateRequest(zone='acme', ledger='bad'))

    assert caught.value.error_class == 'validation'
    assert caught.value.code == 'ledger_invalid'
    assert caught.value.grpc_code == grpc.StatusCode.INVALID_ARGUMENT


def test_grpc_mapper_preserves_presence_and_rejects_lossy_integers() -> None:
    request = EvaluateRequest(
        zone='acme',
        ledger='documents',
        evaluations=[Evaluation(context={}, partition_inputs={})],
    )
    payload = request_to_dict(request)
    assert payload['evaluations'][0]['context'] == {}
    assert payload['evaluations'][0]['partition_inputs'] == {}

    wire = request_to_proto(request)
    assert wire.evaluations[0].HasField('context')
    assert wire.evaluations[0].HasField('partition_inputs')

    with pytest.raises(ValueError, match='not exactly representable'):
        request_to_proto(
            EvaluateRequest(
                zone='acme',
                ledger='documents',
                context={'too_large': MAX_EXACT_PROTO_INTEGER + 1},
            )
        )


def test_grpc_conflict_fallback_matches_shared_contract() -> None:
    for code in (
        grpc.StatusCode.FAILED_PRECONDITION,
        grpc.StatusCode.ALREADY_EXISTS,
        grpc.StatusCode.ABORTED,
    ):
        assert _grpc_class(code) == 'conflict'
