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

from typing import Any

from permguard.az.azreq.model import Action


class ActionBuilder:
    """Builder for creating an Action object."""

    def __init__(self, name: str):
        """Initialize the builder with an action name."""
        self._action = Action(name=name, properties={})

    def with_property(self, key: str, value: Any) -> "ActionBuilder":
        """Set a property for the action."""
        self._action.properties[key] = value
        return self

    def build(self) -> Action:
        """Build and return the Action object with a deep copy of properties."""
        return self._action.model_copy(deep=True)
