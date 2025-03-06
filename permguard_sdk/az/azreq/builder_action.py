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


class Action:
    """Class representing an action."""
    def __init__(self, name: str):
        self.name = name
        self.properties = None  # Initialized as None, matching the Go behavior


class ActionBuilder:
    """Builder for creating Action objects."""
    def __init__(self, name: str):
        self.action = Action(name)

    def with_property(self, key: str, value: any) -> 'ActionBuilder':
        """Sets a property for the action."""
        if self.action.properties is None:
            self.action.properties = {}
        self.action.properties[key] = value
        return self

    def build(self) -> Action:
        """Builds and returns the Action object with a deep copy of properties."""
        instance = Action(self.action.name)
        instance.properties = deepcopy(self.action.properties) if self.action.properties else None
        return instance
