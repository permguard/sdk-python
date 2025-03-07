# Copyright 2025 Nitro Agility S.r.l.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from copy import deepcopy


class Subject:
    """Placeholder class for Subject (to be defined as needed)."""
    pass


class Resource:
    """Placeholder class for Resource (to be defined as needed)."""
    pass


class Action:
    """Placeholder class for Action (to be defined as needed)."""
    pass


class Evaluation:
    """Class representing an evaluation."""
    def __init__(self, subject: 'Subject', resource: 'Resource', action: 'Action'):
        self.subject = subject
        self.resource = resource
        self.action = action
        self.request_id = None
        self.context = None


class EvaluationBuilder:
    """Builder for the Evaluation object."""
    def __init__(self, subject: 'Subject', resource: 'Resource', action: 'Action'):
        self.az_evaluation = Evaluation(subject, resource, action)

    def with_request_id(self, request_id: str) -> 'EvaluationBuilder':
        """Sets the request ID of the Evaluation."""
        self.az_evaluation.request_id = request_id
        return self

    def with_context(self, context: dict) -> 'EvaluationBuilder':
        """Sets the context of the Evaluation."""
        self.az_evaluation.context = context
        return self

    def build(self) -> 'Evaluation':
        """Builds and returns the Evaluation object with a deep copy of the context."""
        instance = Evaluation(self.az_evaluation.subject, self.az_evaluation.resource, self.az_evaluation.action)
        instance.request_id = self.az_evaluation.request_id
        instance.context = deepcopy(self.az_evaluation.context) if self.az_evaluation.context else None
        return instance
