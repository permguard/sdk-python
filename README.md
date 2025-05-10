# The official Python SDK for Permguard

[![GitHub License](https://img.shields.io/github/license/permguard/sdk-python)](https://github.com/permguard/sdk-python?tab=Apache-2.0-1-ov-file#readme)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/permguard)](https://x.com/intent/follow?original_referer=https%3A%2F%2Fdeveloper.x.com%2F&ref_src=twsrc%5Etfw%7Ctwcamp%5Ebuttonembed%7Ctwterm%5Efollow%7Ctwgr%5ETwitterDev&screen_name=Permguard)

[![Documentation](https://img.shields.io/website?label=Docs&url=https%3A%2F%2Fwww.permguard.com%2F)](https://www.permguard.com/)
[![Build, test and publish the artifacts](https://github.com/permguard/sdk-python/actions/workflows/sdk-python-ci.yml/badge.svg)](https://github.com/permguard/sdk-python/actions/workflows/sdk-python-ci.yml)

<p align="left">
  <img src="https://raw.githubusercontent.com/permguard/permguard-assets/main/pink-txt//1line.svg" class="center" width="400px" height="auto"/>
</p>

The Permguard Python SDK provides a simple and flexible client to perform authorization checks against a Permguard Policy Decision Point (PDP) service using gRPC.
Plase refer to the [Permguard Documentation](https://www.permguard.com/) for more information.

---

## Prerequisites

- **Python 3.8, 3.9, 3.10, 3.11** (supported versions)

This package is compatible with the following Python versions:

- `Programming Language :: Python :: 3.8`
- `Programming Language :: Python :: 3.9`
- `Programming Language :: Python :: 3.10`
- `Programming Language :: Python :: 3.11`

Make sure you have one of these versions installed before proceeding.

---

## Installation

Run the following command to install the SDK:

```bash
pip install permguard
```

---

## Usage Example

Below is a sample Python code demonstrating how to create a Permguard client, build an authorization request using a builder pattern, and process the authorization response:

```python
from permguard.az.azreq.builder_principal import PrincipalBuilder
from permguard.az.azreq.builder_request_atomic import AZAtomicRequestBuilder
from permguard.az_client import AZClient
from permguard.az_config import with_endpoint


az_client = AZClient(with_endpoint("localhost", 9094))

principal = PrincipalBuilder("amy.smith@acmecorp.com").build()

entities = [
    {
        "uid": {"type": "MagicFarmacia::Platform::BranchInfo", "id": "subscription"},
        "attrs": {"active": True},
        "parents": [],
    }
]

req = (
    AZAtomicRequestBuilder(
        895741663247,
        "809257ed202e40cab7e958218eecad20",
        "platform-creator",
        "MagicFarmacia::Platform::Subscription",
        "MagicFarmacia::Platform::Action::create",
    )
    .with_request_id("1234")
    .with_principal(principal)
    .with_entities_items("cedar", entities)
    .with_subject_role_actor_type()
    .with_subject_source("keycloack")
    .with_subject_property("isSuperUser", True)
    .with_resource_id("e3a786fd07e24bfa95ba4341d3695ae8")
    .with_resource_property("isEnabled", True)
    .with_action_property("isEnabled", True)
    .with_context_property("time", "2025-01-23T16:17:46+00:00")
    .with_context_property("isSubscriptionActive", True)
    .build()
)

ok, response = az_client.check(req)

if ok:
    print("✅ authorization permitted")
else:
    print("❌ authorization denied")
    if response and response.context:
        if response.context.reason_admin:
            print(f"-> reason admin: {response.context.reason_admin.message}")
        if response.context.reason_user:
            print(f"-> reason user: {response.context.reason_user.message}")
        for eval in response.evaluations:
            if eval.context and eval.context.reason_user:
                print(f"-> reason admin: {eval.context.reason_admin.message}")
                print(f"-> reason user: {eval.context.reason_user.message}")
    if response and response.evaluations:
        for eval in response.evaluations:
            if eval.context:
                if eval.context.reason_admin:
                    print(f"-> evaluation requestid {eval.request_id}: reason admin: {eval.context.reason_admin.message}")
                if eval.context.reason_user:
                    print(f"-> evaluation requestid {eval.request_id}: reason user: {eval.context.reason_user.message}")
```

---

## Version Compatibility

Our SDK follows a versioning scheme aligned with the PermGuard server versions to ensure seamless integration. The versioning format is as follows:

**SDK Versioning Format:** `x.y.z`

- **x.y**: Indicates the compatible PermGuard server version.
- **z**: Represents the SDK's patch or minor updates specific to that server version.

**Compatibility Examples:**

- `SDK Version 1.3.0` is compatible with `PermGuard Server 1.3`.
- `SDK Version 1.3.1` includes minor improvements or bug fixes for `PermGuard Server 1.3`.

**Incompatibility Example:**

- `SDK Version 1.3.0` **may not be guaranteed** to be compatible with `PermGuard Server 1.4` due to potential changes introduced in server version `1.4`.

**Important:** Ensure that the major and minor versions (`x.y`) of the SDK match those of your PermGuard server to maintain compatibility.

---

Created by [Nitro Agility](https://www.nitroagility.com/).
