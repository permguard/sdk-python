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

# Constant for the default principal kind
PRINCIPAL_DEFAULT_KIND = "user"


class Principal:
    """Class representing a principal."""
    def __init__(self, id: str):
        self.id = id
        self.type = PRINCIPAL_DEFAULT_KIND
        self.source = None


class PrincipalBuilder:
    """Builder for the Principal object."""
    def __init__(self, id: str):
        self.principal = Principal(id)

    def with_kind(self, kind: str) -> 'PrincipalBuilder':
        """Sets the kind of the principal."""
        self.principal.type = kind
        return self

    def with_source(self, source: str) -> 'PrincipalBuilder':
        """Sets the source of the principal."""
        self.principal.source = source
        return self

    def build(self) -> 'Principal':
        """Builds and returns the Principal object."""
        instance = Principal(self.principal.id)
        instance.type = self.principal.type
        instance.source = self.principal.source
        return instance
