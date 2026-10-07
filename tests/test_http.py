# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, ClassVar, Dict, Iterator, Tuple, cast

import pytest

from permguard import Client, EvaluateRequest, Refusal


class Handler(BaseHTTPRequestHandler):
    seen: ClassVar[Dict[str, Any]] = {}

    def do_POST(self) -> None:
        length = int(self.headers.get('Content-Length', '0'))
        Handler.seen = json.loads(self.rfile.read(length))
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
