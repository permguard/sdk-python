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

import copy
from typing import Any, Dict


class ContextBuilder:
    """Builder for creating a context dictionary."""

    def __init__(self):
        """Initialize the builder with an empty context dictionary."""
        self._context: Dict[str, Any] = {}

    def with_property(self, key: str, value: Any) -> "ContextBuilder":
        """Set a property for the context."""
        self._context[key] = value
        return self

    def build(self) -> Dict[str, Any]:
        """Build and return the context dictionary."""
        return copy.deepcopy(self._context)
