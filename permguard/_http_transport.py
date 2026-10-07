# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import http.client
import json
import ssl
import threading
from http import HTTPStatus
from typing import Any, Dict, Mapping, Optional
from urllib.parse import ParseResult

from permguard._wire import configuration_from_dict, request_to_dict, response_from_dict
from permguard.errors import Refusal
from permguard.models import Configuration, EvaluateRequest, EvaluateResponse

EVALUATION_PATH = '/access/v1/evaluation'
EVALUATIONS_PATH = '/access/v1/evaluations'
CONFIGURATION_PATH = '/.well-known/permguard-pdp-v1-configuration'
MAX_RESPONSE_BYTES = 16 << 20


class HTTPTransport:
    def __init__(
        self,
        endpoint: ParseResult,
        timeout: float,
        headers: Mapping[str, str],
        tls_context: Optional[ssl.SSLContext],
    ) -> None:
        if endpoint.path not in ('', '/') or endpoint.params or endpoint.query or endpoint.fragment:
            raise ValueError('HTTP Permguard endpoint must not contain a path, query, or fragment')
        if endpoint.hostname is None:
            raise ValueError('HTTP Permguard endpoint requires a host')
        self._scheme = endpoint.scheme.lower()
        self._host = endpoint.hostname
        self._port = endpoint.port
        self._timeout = timeout
        self._headers = dict(headers)
        self._tls_context = tls_context
        self._connection: Optional[http.client.HTTPConnection] = None
        self._lock = threading.Lock()

    def evaluate(self, request: EvaluateRequest, many: bool, timeout: Optional[float]) -> EvaluateResponse:
        path = EVALUATIONS_PATH if many else EVALUATION_PATH
        payload = self._call('POST', path, request_to_dict(request), timeout)
        return response_from_dict(payload)

    def configuration(self, timeout: Optional[float]) -> Configuration:
        return configuration_from_dict(self._call('GET', CONFIGURATION_PATH, None, timeout))

    def close(self) -> None:
        with self._lock:
            if self._connection is not None:
                self._connection.close()
                self._connection = None

    def _connect(self, timeout: float) -> http.client.HTTPConnection:
        if self._scheme == 'https':
            return http.client.HTTPSConnection(
                self._host,
                self._port,
                timeout=timeout,
                context=self._tls_context,
            )
        return http.client.HTTPConnection(self._host, self._port, timeout=timeout)

    def _call(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]],
        timeout: Optional[float],
    ) -> Dict[str, Any]:
        body = None if payload is None else json.dumps(payload, separators=(',', ':')).encode('utf-8')
        headers = dict(self._headers)
        headers['Accept'] = 'application/json'
        if body is not None:
            headers['Content-Type'] = 'application/json'

        with self._lock:
            if self._connection is None:
                self._connection = self._connect(timeout or self._timeout)
            elif timeout is not None:
                self._connection.timeout = timeout
            try:
                self._connection.request(method, path, body=body, headers=headers)
                response = self._connection.getresponse()
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            except (OSError, http.client.HTTPException) as error:
                self._connection.close()
                self._connection = None
                raise RuntimeError(f'call Permguard HTTP endpoint: {error}') from error

        if len(raw) > MAX_RESPONSE_BYTES:
            raise RuntimeError(f'Permguard HTTP response exceeds {MAX_RESPONSE_BYTES} bytes')
        try:
            decoded = json.loads(raw.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError(f'decode Permguard HTTP response: {error}') from error
        if not isinstance(decoded, dict):
            raise RuntimeError('decode Permguard HTTP response: expected a JSON object')
        if response.status < HTTPStatus.OK or response.status >= HTTPStatus.MULTIPLE_CHOICES:
            raise _refusal(response.status, decoded)
        return decoded


def _refusal(status: int, payload: Mapping[str, Any]) -> Refusal:
    error_class = str(payload.get('class') or _http_class(status))
    code = str(payload.get('code') or 'http_status')
    message = str(payload.get('message') or http.client.responses.get(status, 'HTTP request failed'))
    return Refusal(error_class, code, message, http_status=status)


def _http_class(status: int) -> str:
    if status in (HTTPStatus.BAD_REQUEST, HTTPStatus.UNPROCESSABLE_ENTITY):
        return 'validation'
    if status == HTTPStatus.CONFLICT:
        return 'conflict'
    if status in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
        return 'authorization'
    if status == HTTPStatus.NOT_FOUND:
        return 'not_found'
    if status in (HTTPStatus.SERVICE_UNAVAILABLE, HTTPStatus.GATEWAY_TIMEOUT):
        return 'unavailable'
    return 'internal'
