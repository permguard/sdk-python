# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, ClassVar, Dict, Iterator, Tuple, cast

import pytest

from permguard import Client, EvaluateRequest, Refusal
from permguard._http_transport import _http_class


class Handler(BaseHTTPRequestHandler):
    seen: ClassVar[Dict[str, Any]] = {}

    def do_POST(self) -> None:
        length = int(self.headers.get('Content-Length', '0'))
        Handler.seen = json.loads(self.rfile.read(length))
        ledger = Handler.seen.get('ledger')
        if ledger == 'slow':
            time.sleep(1.5)
        if ledger == 'too-large':
            self._raw(413, b'length limit exceeded', 'text/plain')
            return
        if ledger == 'empty-401':
            self._raw(401, b'', None)
            return
        if ledger == 'not-json':
            self._raw(200, b'not json', 'text/plain')
            return
        if Handler.seen.get('ledger') == 'bad':
            self._json(
                400,
                {'class': 'validation', 'code': 'ledger_invalid', 'message': 'bad ledger'},
            )
            return
        self._json(
            200,
            {
                'decision': False,
                'request_id': Handler.seen.get('request_id'),
                'context': {'policies': ['policy-1']},
            },
        )

    def do_GET(self) -> None:
        self._json(
            200,
            {
                'interface': 'permguard.api.pdp.native.v1',
                'pdp': 'http://test',
                'endpoints': {'evaluation': 'e', 'evaluations': 'es'},
                'capabilities': [],
                'store_scope': {
                    'in': 'payload',
                    'zone': 'required',
                    'ledger': 'required',
                    'profile': 'optional',
                },
            },
        )

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _raw(self, status: int, body: bytes, content_type: Any) -> None:
        self.send_response(status)
        if content_type is not None:
            self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: Dict[str, Any]) -> None:
        encoded = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


@pytest.fixture
def http_endpoint() -> Iterator[Tuple[str, ThreadingHTTPServer]]:
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = cast(Tuple[str, int], server.server_address)
    try:
        yield f'http://{host}:{port}', server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_http_native_contract(http_endpoint: Tuple[str, ThreadingHTTPServer]) -> None:
    endpoint, _ = http_endpoint
    with Client(endpoint, headers={'Authorization': 'Bearer test'}) as client:
        response = client.evaluate(EvaluateRequest(zone='acme', ledger='documents', request_id='r1'))
        configuration = client.get_configuration()

    assert response.decision is False
    assert response.request_id == 'r1'
    assert response.context is not None
    assert response.context.policies == ['policy-1']
    assert Handler.seen['zone'] == 'acme'
    assert configuration.interface == 'permguard.api.pdp.native.v1'


def test_http_refusal_is_structured(http_endpoint: Tuple[str, ThreadingHTTPServer]) -> None:
    endpoint, _ = http_endpoint
    with Client(endpoint) as client, pytest.raises(Refusal) as caught:
        client.evaluate(EvaluateRequest(zone='acme', ledger='bad'))

    assert caught.value.error_class == 'validation'
    assert caught.value.code == 'ledger_invalid'
    assert caught.value.http_status == 400


def test_http_fallback_and_endpoint_validation_match_shared_contract() -> None:
    assert _http_class(409) == 'conflict'
    with pytest.raises(ValueError, match='embedded credentials'):
        Client('http://user:secret@pdp.example')


def test_http_per_call_timeout_holds_on_a_reused_connection(
    http_endpoint: Tuple[str, ThreadingHTTPServer],
) -> None:
    """BUG-0276: each call's timeout bounds it on the connection kept open."""
    endpoint, _ = http_endpoint
    with Client(endpoint, timeout=5) as client:
        client.evaluate(EvaluateRequest(zone='acme', ledger='documents'))
        started = time.monotonic()
        with pytest.raises(Refusal) as caught:
            client.evaluate(EvaluateRequest(zone='acme', ledger='slow'), timeout=0.5)
        assert (caught.value.error_class, caught.value.code) == ('unavailable', 'timeout')
        assert time.monotonic() - started < 1.4, 'bounded by the call, not by the server'
        # A call with no timeout of its own is bounded by the client's, not by 0.5 s.
        client.evaluate(EvaluateRequest(zone='acme', ledger='documents'))
        response = client.evaluate(EvaluateRequest(zone='acme', ledger='slow'))
        assert response.decision is False


def test_http_error_body_that_is_not_json_is_a_refusal(
    http_endpoint: Tuple[str, ThreadingHTTPServer],
) -> None:
    """BUG-0282: the status is read first; a non-JSON error body is the refusal's message."""
    endpoint, _ = http_endpoint
    with Client(endpoint) as client:
        with pytest.raises(Refusal) as caught:
            client.evaluate(EvaluateRequest(zone='acme', ledger='too-large'))
        assert caught.value.http_status == 413
        assert caught.value.code == 'http_status'
        assert caught.value.error_class == 'internal'
        assert 'length limit exceeded' in str(caught.value)
        with pytest.raises(Refusal) as caught:
            client.evaluate(EvaluateRequest(zone='acme', ledger='empty-401'))
        assert caught.value.http_status == 401
        assert caught.value.error_class == 'authorization'
        with pytest.raises(RuntimeError, match='decode Permguard HTTP response'):
            client.evaluate(EvaluateRequest(zone='acme', ledger='not-json'))
