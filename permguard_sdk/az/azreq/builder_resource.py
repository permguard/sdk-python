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


class Resource:
    """Class representing a resource."""
    def __init__(self, kind: str):
        self.type = kind  # Type of the resource
        self.id = None    # ID of the resource, initially None
        self.properties = None  # Properties dictionary, initially None


class ResourceBuilder:
    """Builder for the Resource object."""
    def __init__(self, kind: str):
        # Initialize the builder with a new Resource instance
        self.resource = Resource(kind)

    def with_id(self, id: str) -> 'ResourceBuilder':
        """Sets the ID of the resource."""
        self.resource.id = id
        return self

    def with_property(self, key: str, value: any) -> 'ResourceBuilder':
        """Sets a property of the resource."""
        # Initialize properties dictionary if it doesn't exist
        if self.resource.properties is None:
            self.resource.properties = {}
        self.resource.properties[key] = value
        return self

    def build(self) -> Resource:
        """Builds and returns the Resource object with a deep copy of properties."""
        # Create a new Resource instance with the same type
        instance = Resource(self.resource.type)
        # Copy the ID
        instance.id = self.resource.id
        # Deep copy the properties if they exist, otherwise keep as None
        instance.properties = deepcopy(self.resource.properties) if self.resource.properties else None
        return instance