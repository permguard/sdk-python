# Copyright 2025 Nitro Agility S.r.l.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Any, List

from permguard.az.azreq.model import AZRequest, Principal
from permguard.az.azreq.builder_subject import SubjectBuilder
from permguard.az.azreq.builder_resource import ResourceBuilder
from permguard.az.azreq.builder_action import ActionBuilder
from permguard.az.azreq.builder_context import ContextBuilder
from permguard.az.azreq.builder_request_composed import AZRequestBuilder


# Costanti per i tipi di subject
USER_TYPE = "user"
ROLE_ACTOR_TYPE = "role-actor"
TWIN_ACTOR_TYPE = "twin-actor"


class AZAtomicRequestBuilder:
    """Builder for creating an AZAtomicRequest object."""

    def __init__(self, zone_id: int, ledger_id: str, subject_id: str, resource_kind: str, action_name: str):
        """Initialize the builder with mandatory fields."""
        self._az_request_builder = AZRequestBuilder(zone_id, ledger_id)
        self._az_subject_builder = SubjectBuilder(subject_id)
        self._az_resource_builder = ResourceBuilder(resource_kind)
        self._az_action_builder = ActionBuilder(action_name)
        self._az_context_builder = ContextBuilder()
        self._request_id: str = ""
        self._principal: Principal = None

    def with_entities_map(self, schema: str, entities: Dict[str, Any]) -> "AZAtomicRequestBuilder":
        """Set the entities map in the AZRequest."""
        self._az_request_builder.with_entities_map(schema, entities)
        return self

    def with_entities_items(self, schema: str, entities: List[Dict[str, Any]]) -> "AZAtomicRequestBuilder":
        """Set the entities items in the AZRequest."""
        self._az_request_builder.with_entities_items(schema, entities)
        return self

    def with_request_id(self, request_id: str) -> "AZAtomicRequestBuilder":
        """Set the request ID for the AZRequest."""
        self._request_id = request_id
        return self

    def with_principal(self, principal: Principal) -> "AZAtomicRequestBuilder":
        """Set the principal for the AZRequest."""
        self._principal = principal
        return self

    def with_subject_user_type(self) -> "AZAtomicRequestBuilder":
        """Set the subject type to USER."""
        self._az_subject_builder.with_type(USER_TYPE)
        return self

    def with_subject_role_actor_type(self) -> "AZAtomicRequestBuilder":
        """Set the subject type to ROLE-ACTOR."""
        self._az_subject_builder.with_type(ROLE_ACTOR_TYPE)
        return self

    def with_subject_twin_actor_type(self) -> "AZAtomicRequestBuilder":
        """Set the subject type to TWIN-ACTOR."""
        self._az_subject_builder.with_type(TWIN_ACTOR_TYPE)
        return self

    def with_subject_type(self, kind: str) -> "AZAtomicRequestBuilder":
        """Set the subject type."""
        self._az_subject_builder.with_type(kind)
        return self

    def with_subject_source(self, source: str) -> "AZAtomicRequestBuilder":
        """Set the source of the subject."""
        self._az_subject_builder.with_source(source)
        return self

    def with_subject_property(self, key: str, value: Any) -> "AZAtomicRequestBuilder":
        """Set a property of the subject."""
        self._az_subject_builder.with_property(key, value)
        return self

    def with_resource_id(self, id: str) -> "AZAtomicRequestBuilder":
        """Set the resource ID."""
        self._az_resource_builder.with_id(id)
        return self

    def with_resource_property(self, key: str, value: Any) -> "AZAtomicRequestBuilder":
        """Set a property of the resource."""
        self._az_resource_builder.with_property(key, value)
        return self

    def with_action_property(self, key: str, value: Any) -> "AZAtomicRequestBuilder":
        """Set a property of the action."""
        self._az_action_builder.with_property(key, value)
        return self

    def with_context_property(self, key: str, value: Any) -> "AZAtomicRequestBuilder":
        """Set a property of the context."""
        self._az_context_builder.with_property(key, value)
        return self

    def build(self) -> AZRequest:
        """Build and return the AZRequest object."""
        subject = self._az_subject_builder.build()
        resource = self._az_resource_builder.build()
        action = self._az_action_builder.build()
        context = self._az_context_builder.build()

        self._az_request_builder \
            .with_principal(self._principal) \
            .with_request_id(self._request_id) \
            .with_subject(subject) \
            .with_resource(resource) \
            .with_action(action) \
            .with_context(context)

        return self._az_request_builder.build()
