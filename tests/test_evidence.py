# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from permguard import (
    Attestation,
    EvaluateRequest,
    Evidence,
    EvidencePosition,
    ResponseSigning,
)
from permguard._wire import (
    configuration_from_dict,
    configuration_from_proto,
    request_to_dict,
    request_to_proto,
    response_from_dict,
    response_from_proto,
)
from permguard.data.v1 import pdp_pb2


def test_the_nonce_the_attestation_and_the_evidence_travel_on_both_transports() -> None:
    """BUG-0274: a request asks for a signed response with its nonce, and the answer's
    attestation and decision evidence reach the caller over both transports."""
    request = EvaluateRequest(zone='z', ledger='l', request_nonce='bm9uY2Utb2Ytc2l4dGVlbg')
    assert request_to_proto(request).request_nonce == 'bm9uY2Utb2Ytc2l4dGVlbg'
    assert request_to_dict(request)['request_nonce'] == 'bm9uY2Utb2Ytc2l4dGVlbg'
    assert 'request_nonce' not in request_to_dict(EvaluateRequest(zone='z', ledger='l'))

    from_grpc = response_from_proto(
        pdp_pb2.EvaluateResponse(
            decision=True,
            context=pdp_pb2.DecisionContext(
                id='d-1',
                evidence=pdp_pb2.Evidence(
                    mode='required',
                    status='recorded',
                    record_id='rec-1',
                    position=pdp_pb2.EvidencePosition(host_id='h', run='r', sequence='7'),
                ),
            ),
            attestation=pdp_pb2.Attestation(protected='p', payload='b', signature='s'),
        )
    )
    from_http = response_from_dict(
        {
            'decision': True,
            'context': {
                'id': 'd-1',
                'evidence': {
                    'mode': 'required',
                    'status': 'recorded',
                    'record_id': 'rec-1',
                    'position': {'host_id': 'h', 'run': 'r', 'sequence': '7'},
                },
            },
            'attestation': {'protected': 'p', 'payload': 'b', 'signature': 's'},
        }
    )
    assert from_grpc == from_http
    assert from_http.context is not None
    assert from_http.context.evidence == Evidence(
        mode='required',
        status='recorded',
        record_id='rec-1',
        position=EvidencePosition(host_id='h', run='r', sequence='7'),
    )
    assert from_http.attestation == Attestation(protected='p', payload='b', signature='s')


def test_the_discovery_document_is_read_whole_on_both_transports() -> None:
    """BUG-0274: the discovery document's version, lifecycle, limits and response signing reach
    the caller over both transports."""
    from_grpc = configuration_from_proto(
        pdp_pb2.GetConfigurationResponse(
            version='0.1.33',
            component='data-plane',
            state='serving',
            stage='v1',
            limits={'max_evaluations': 64},
            response_signing=pdp_pb2.ResponseSigning(
                state='optional', validity_seconds=300, clock_skew_seconds=30
            ),
        )
    )
    from_http = configuration_from_dict(
        {
            'version': '0.1.33',
            'component': 'data-plane',
            'state': 'serving',
            'stage': 'v1',
            'limits': {'max_evaluations': 64},
            'response_signing': {
                'state': 'optional',
                'validity_seconds': 300,
                'clock_skew_seconds': 30,
            },
        }
    )
    assert from_grpc == from_http
    assert (from_http.version, from_http.state, from_http.stage, from_http.sunset) == (
        '0.1.33',
        'serving',
        'v1',
        None,
    )
    assert from_http.limits == {'max_evaluations': 64}
    assert from_http.response_signing == ResponseSigning(
        state='optional', validity_seconds=300, clock_skew_seconds=30
    )
