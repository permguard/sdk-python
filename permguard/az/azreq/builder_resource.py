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
from permguard.az.azreq.model import Resource


class ResourceBuilder:
    """Builder for creating a Resource object."""

    def __init__(self, kind: str):
        """Initialize the builder with a resource type."""
        self._resource = Resource(type=kind, properties={})

    def with_id(self, id: str) -> "ResourceBuilder":
        """Set the ID of the resource."""
        self._resource.id = id
        return self

    def with_property(self, key: str, value: Any) -> "ResourceBuilder":
        """Set a property of the resource."""
        self._resource.properties[key] = value
        return self

    def build(self) -> Resource:
        """Build and return the Resource object."""
        return self._resource.model_copy(deep=True)
