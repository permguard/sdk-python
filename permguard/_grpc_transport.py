# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Dict, Mapping, Optional, Sequence, Tuple
from urllib.parse import ParseResult

import grpc

from permguard._wire import configuration_from_proto, request_to_proto, response_from_proto
from permguard.data.v1 import pdp_pb2, pdp_pb2_grpc
from permguard.errors import Refusal
from permguard.models import Configuration, EvaluateRequest, EvaluateResponse

GRPC_ERROR_CLASS = 'permguard-error-class'
GRPC_ERROR_CODE = 'permguard-error-code'


class GRPCTransport:
    def __init__(
        self,
        endpoint: ParseResult,
        headers: Mapping[str, str],
        credentials: Optional[grpc.ChannelCredentials],
    ) -> None:
        if endpoint.path not in ('', '/') or endpoint.params or endpoint.query or endpoint.fragment:
            raise ValueError('gRPC Permguard endpoint must not contain a path, query, or fragment')
        if endpoint.hostname is None:
            raise ValueError('gRPC Permguard endpoint requires a host')
        target = endpoint.netloc
        if endpoint.scheme.lower() == 'grpcs':
            self._channel = grpc.secure_channel(target, credentials or grpc.ssl_channel_credentials())
        else:
            self._channel = grpc.insecure_channel(target)
        self._stub = pdp_pb2_grpc.PolicyDecisionPointStub(self._channel)  # type: ignore[no-untyped-call]
        self._metadata: Sequence[Tuple[str, str]] = tuple((name.lower(), value) for name, value in headers.items())

    def evaluate(self, request: EvaluateRequest, many: bool, timeout: Optional[float]) -> EvaluateResponse:
        method = self._stub.EvaluateMany if many else self._stub.Evaluate
        try:
            response = method(request_to_proto(request), timeout=timeout, metadata=self._metadata)
        except grpc.RpcError as error:
            raise _refusal(error) from error
        return response_from_proto(response)

    def configuration(self, timeout: Optional[float]) -> Configuration:
        try:
            response = self._stub.GetConfiguration(
                pdp_pb2.GetConfigurationRequest(),
                timeout=timeout,
                metadata=self._metadata,
            )
        except grpc.RpcError as error:
            raise _refusal(error) from error
        return configuration_from_proto(response)

    def close(self) -> None:
        self._channel.close()


def _refusal(error: grpc.RpcError) -> Refusal:
    values: Dict[str, str] = {}
    metadata = error.trailing_metadata() or error.initial_metadata() or ()
    for key, value in metadata:
        values[key] = value.decode('ascii') if isinstance(value, bytes) else str(value)
    grpc_code = error.code()
    return Refusal(
        values.get(GRPC_ERROR_CLASS, _grpc_class(grpc_code)),
        values.get(GRPC_ERROR_CODE, grpc_code.name.lower()),
        error.details() or str(error),
        grpc_code=grpc_code,
    )


def _grpc_class(code: grpc.StatusCode) -> str:
    if code in (grpc.StatusCode.INVALID_ARGUMENT, grpc.StatusCode.OUT_OF_RANGE):
        return 'validation'
    if code in (grpc.StatusCode.FAILED_PRECONDITION, grpc.StatusCode.ALREADY_EXISTS, grpc.StatusCode.ABORTED):
        return 'conflict'
    if code in (grpc.StatusCode.UNAUTHENTICATED, grpc.StatusCode.PERMISSION_DENIED):
        return 'authorization'
    if code == grpc.StatusCode.NOT_FOUND:
        return 'not_found'
    if code in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED):
        return 'unavailable'
    return 'internal'
