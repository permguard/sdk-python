# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

"""Against a real data plane: ``scripts/e2e-server.sh`` starts it from the Permguard release
PERMGUARD_CONTRACT pins, serving a ledger ``e2e/policies`` that permits ``User:alice`` to
``read`` (BUG-0077). Run with ``python -m pytest -q e2e``."""

import os
from typing import Any, Callable

import pytest

from permguard import Action, Client, Entity, EvaluateRequest, Evaluation, Refusal


def _endpoint(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail('E2E_HTTP and E2E_GRPC name the data plane scripts/e2e-server.sh started')
    return value


def _ask(subject: str) -> EvaluateRequest:
    return EvaluateRequest(
        zone='e2e',
        ledger='policies',
        subject=Entity(type='User', id=subject),
        resource=Entity(type='Document', id='d'),
        action=Action(name='read'),
    )


def _refusal_code(call: Callable[[], Any]) -> str:
    with pytest.raises(Refusal) as refused:
        call()
    return refused.value.code


@pytest.mark.parametrize('variable', ['E2E_HTTP', 'E2E_GRPC'])
def test_against_a_real_data_plane(variable: str) -> None:
    """Over both transports: a permit with its decision evidence, a deny, a batch, a refusal, a
    request for a signed response, and the discovery document (BUG-0077, BUG-0274)."""
    client = Client(_endpoint(variable))
    try:
        permit = client.evaluate(_ask('alice'))
        assert permit.decision, 'alice reads'
        assert permit.context is not None and permit.context.evidence is not None
        assert permit.context.evidence.status, "the decision's evidence"
        assert not client.evaluate(_ask('bob')).decision, 'bob reads'

        batch = _ask('alice')
        batch.evaluations = [
            Evaluation(subject=Entity(type='User', id='alice')),
            Evaluation(subject=Entity(type='User', id='bob')),
        ]
        many = client.evaluate_many(batch)
        assert [item.decision for item in many.evaluations] == [True, False], 'the batch'

        missing = _ask('alice')
        missing.ledger = 'nope'
        assert _refusal_code(lambda: client.evaluate(missing)) == 'ledger_not_served'

        # The nonce reaches the plane: a signed response is addressed to an authenticated caller,
        # and this one presents no token, so the plane refuses rather than answer unsigned. The
        # attestation's mapping is the unit tests'.
        signed = _ask('alice')
        signed.request_nonce = 'ZTJlLW5vbmNlLTE2LWJ5dGVz'
        assert _refusal_code(lambda: client.evaluate(signed)) == 'unauthenticated'

        configuration = client.get_configuration()
        assert configuration.version and configuration.stage
        assert configuration.limits.get('max_evaluations', 0) > 0
        assert configuration.response_signing.state
    finally:
        client.close()
