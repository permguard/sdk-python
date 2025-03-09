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
from permguard.az.azreq.model import (
    AZRequest, AZModel, PolicyStore, Entities, Principal, Subject, Resource, Action, Evaluation
)


# Costanti per i tipi di store
POLICY_STORE_KIND = "LEDGER"
CEDAR_ENTITY_KIND = "CEDAR"


class AZRequestBuilder:
    """Builder for creating an AZRequest object."""

    def __init__(self, zone_id: int, ledger_id: str):
        """Initialize the builder with a default AZModel."""
        self._az_request = AZRequest(
            authorization_model=AZModel(
                zone_id=zone_id,
                policy_store=PolicyStore(kind=POLICY_STORE_KIND, id=ledger_id),
                entities=Entities()
            ),
            evaluations=[]
        )

    def with_principal(self, principal: Principal) -> "AZRequestBuilder":
        """Set the principal for the AZRequest."""
        self._az_request.authorization_model.principal = principal
        return self

    def with_request_id(self, request_id: str) -> "AZRequestBuilder":
        """Set the request ID for the AZRequest."""
        self._az_request.request_id = request_id
        return self

    def with_subject(self, subject: Subject) -> "AZRequestBuilder":
        """Set the subject for the AZRequest."""
        self._az_request.subject = subject
        return self

    def with_resource(self, resource: Resource) -> "AZRequestBuilder":
        """Set the resource for the AZRequest."""
        self._az_request.resource = resource
        return self

    def with_action(self, action: Action) -> "AZRequestBuilder":
        """Set the action for the AZRequest."""
        self._az_request.action = action
        return self

    def with_context(self, context: Dict[str, Any]) -> "AZRequestBuilder":
        """Set the context for the AZRequest."""
        self._az_request.context = context
        return self

    def with_entities_map(self, schema: str, entities: Dict[str, Any]) -> "AZRequestBuilder":
        """Set the entities map in the AZRequest."""
        self._az_request.authorization_model.entities.schema_name = schema
        self._az_request.authorization_model.entities.items = [entities]
        return self

    def with_entities_items(self, schema: str, entities: List[Dict[str, Any]]) -> "AZRequestBuilder":
        """Set the entities items in the AZRequest."""
        self._az_request.authorization_model.entities.schema_name = schema
        self._az_request.authorization_model.entities.items = entities or []
        return self

    def with_evaluation(self, evaluation: Evaluation) -> "AZRequestBuilder":
        """Add an evaluation to the AZRequest."""
        self._az_request.evaluations.append(evaluation)
        return self

    def build(self) -> AZRequest:
        """Build and return the AZRequest object."""
        return self._az_request.model_copy(deep=True)

