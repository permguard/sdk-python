<!--
Copyright (c) 2022 Nitro Agility S.r.l.
SPDX-License-Identifier: Apache-2.0
-->

# Permguard Python SDK

The official synchronous Python client for the stateless Permguard PDP
interface `permguard.api.pdp.native.v1`.

The same API supports both server bindings:

- `http://` and `https://` use JSON;
- `grpc://` and `grpcs://` use `permguard.data.v1.PolicyDecisionPoint`.

## Installation

```bash
pip install permguard
```

Python 3.8 or newer is required.

## Evaluate one request

```python
from permguard import Action, Client, Entity, EvaluateRequest

with Client("grpc://localhost:7443") as client:
    response = client.evaluate(
        EvaluateRequest(
            zone="acme",
            ledger="documents",
            subject=Entity(type="user", id="amy@example.com"),
            resource=Entity(type="document", id="quarterly-report"),
            action=Action(name="read"),
        )
    )

print("permitted:", response.decision)
```

Use `http://localhost:7443` to send the same request over HTTP/JSON. A deny is a
successful response whose `decision` is `False`. Validation, authorization,
availability, and server failures raise `permguard.Refusal`, preserving their
stable class and code.

## Partition inputs

Runtime data is addressed to the partition name declared by the ledger profile:

```python
from permguard import PartitionInput

request.partition_inputs["authorization"] = PartitionInput(
    type="permguard.cedar.entities.v1",
    data=[
        {
            "uid": {"type": "Team", "id": "engineering"},
            "attrs": {"active": True},
            "parents": [],
        }
    ],
)
```

The key selects a partition already declared by the profile. The input `type`
is checked against that declaration; it does not select a runtime.

## Evaluate a batch

```python
from permguard import (
    Action,
    Entity,
    EvaluateRequest,
    Evaluation,
    EvaluationOptions,
    EvaluationsSemantic,
)

response = client.evaluate_many(
    EvaluateRequest(
        zone="acme",
        ledger="documents",
        subject=Entity(type="user", id="amy@example.com"),
        evaluations=[
            Evaluation(
                resource=Entity(type="document", id="one"),
                action=Action(name="read"),
                request_id="one",
            ),
            Evaluation(
                resource=Entity(type="document", id="two"),
                action=Action(name="read"),
                request_id="two",
            ),
        ],
        options=EvaluationOptions(
            evaluations_semantic=EvaluationsSemantic.EXECUTE_ALL,
        ),
    )
)
```

Call `client.get_configuration()` to read the interface discovery document.
The client reuses its HTTP connection or gRPC channel; use it as a context
manager or call `close()`.

Static HTTP headers and gRPC metadata can be supplied through `headers`. HTTPS
accepts an `ssl.SSLContext`; gRPCS accepts `grpc.ChannelCredentials`.

## Compatibility

This major version implements `permguard.api.pdp.native.v1`. Compatibility is
tied to that versioned interface rather than to a server minor release.

## Development and release

```bash
hatch run protoc
hatch run dev
hatch -e lint run all
hatch build
```

The existing tag-based PyPI workflow remains the release mechanism. The
package version is still read from `permguard/__about__.py` and set from the
release tag.

## License

Apache License 2.0. See [LICENSE](LICENSE) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
