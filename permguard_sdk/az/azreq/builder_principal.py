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

from permguard.az.azreq.model import Principal


# Valore predefinito per Principal
PRINCIPAL_DEFAULT_KIND = "user"


class PrincipalBuilder:
    """Builder for creating a Principal object."""

    def __init__(self, id: str):
        """Initialize the builder with a default principal type."""
        self._principal = Principal(id=id, type=PRINCIPAL_DEFAULT_KIND)

    def with_kind(self, kind: str) -> "PrincipalBuilder":
        """Set the kind/type of the principal."""
        self._principal.type = kind
        return self

    def with_source(self, source: str) -> "PrincipalBuilder":
        """Set the source of the principal."""
        self._principal.source = source
        return self

    def build(self) -> Principal:
        """Build and return the Principal object."""
        return self._principal.model_copy(deep=True)
