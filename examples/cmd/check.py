# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

import os

from permguard import Action, Client, Entity, EvaluateRequest, Refusal


def main() -> None:
    endpoint = os.environ.get('PERMGUARD_PDP_URL', 'grpc://localhost:7443')
    request = EvaluateRequest(
        zone='acme',
        ledger='documents',
        subject=Entity(type='user', id='amy@example.com'),
        resource=Entity(type='document', id='quarterly-report'),
        action=Action(name='read'),
        request_id='example-1',
    )

    try:
        with Client(endpoint) as client:
            response = client.evaluate(request)
    except Refusal as refusal:
        raise SystemExit(
            f'PDP refused the request: class={refusal.error_class} code={refusal.code} message={refusal.message}'
        ) from refusal

    print(f'permitted: {response.decision}')


if __name__ == '__main__':
    main()
