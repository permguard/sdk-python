# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import ssl
from types import TracebackType
from typing import Mapping, Optional, Type
from urllib.parse import urlparse

import grpc

from permguard._grpc_transport import GRPCTransport
from permguard._http_transport import HTTPTransport
from permguard._transport import Transport
from permguard.models import Configuration, EvaluateRequest, EvaluateResponse


class Client:
    """A reusable client for the Permguard native PDP v1 interface."""

    def __init__(
        self,
        endpoint: str,
        *,
        timeout: float = 5.0,
        headers: Optional[Mapping[str, str]] = None,
        tls_context: Optional[ssl.SSLContext] = None,
        grpc_credentials: Optional[grpc.ChannelCredentials] = None,
    ) -> None:
        if timeout <= 0:
            raise ValueError('timeout must be greater than zero')
        parsed = urlparse(endpoint)
        if not parsed.netloc:
            raise ValueError('Permguard endpoint requires a host')
        if parsed.username is not None or parsed.password is not None:
            raise ValueError('Permguard endpoint must not contain embedded credentials')
        scheme = parsed.scheme.lower()
        held_headers = dict(headers or {})
        if scheme in ('http', 'https'):
            self._transport: Transport = HTTPTransport(parsed, timeout, held_headers, tls_context)
        elif scheme in ('grpc', 'grpcs'):
            self._transport = GRPCTransport(parsed, held_headers, grpc_credentials)
        else:
            raise ValueError(f'unsupported Permguard endpoint scheme {parsed.scheme!r}')
        self._timeout = timeout

    def evaluate(self, request: EvaluateRequest, *, timeout: Optional[float] = None) -> EvaluateResponse:
        """Evaluate one request."""

        if request is None:
            raise ValueError('Permguard evaluation request cannot be None')
        return self._transport.evaluate(request, False, self._call_timeout(timeout))

    def evaluate_many(self, request: EvaluateRequest, *, timeout: Optional[float] = None) -> EvaluateResponse:
        """Evaluate a boxcarred request."""

        if request is None:
            raise ValueError('Permguard evaluation request cannot be None')
        return self._transport.evaluate(request, True, self._call_timeout(timeout))

    def get_configuration(self, *, timeout: Optional[float] = None) -> Configuration:
        """Return the PDP native v1 discovery document."""

        return self._transport.configuration(self._call_timeout(timeout))

    def close(self) -> None:
        self._transport.close()

    def _call_timeout(self, timeout: Optional[float]) -> float:
        held = self._timeout if timeout is None else timeout
        if held <= 0:
            raise ValueError('timeout must be greater than zero')
        return held

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()
