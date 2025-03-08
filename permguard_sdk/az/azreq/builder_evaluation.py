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

from typing import Dict, Any

from permguard.az.azreq.model import Evaluation, Subject, Resource, Action


class EvaluationBuilder:
    """Builder for creating an Evaluation object."""

    def __init__(self, subject: Subject, resource: Resource, action: Action):
        """Initialize the builder with required subject, resource, and action."""
        self._evaluation = Evaluation(
            subject=subject,
            resource=resource,
            action=action,
            context={}
        )

    def with_request_id(self, request_id: str) -> "EvaluationBuilder":
        """Set the request ID of the Evaluation."""
        self._evaluation.request_id = request_id
        return self

    def with_context(self, context: Dict[str, Any]) -> "EvaluationBuilder":
        """Set the context of the Evaluation."""
        self._evaluation.context = context
        return self

    def build(self) -> Evaluation:
        """Build and return the Evaluation object."""
        return self._evaluation.model_copy(deep=True)
