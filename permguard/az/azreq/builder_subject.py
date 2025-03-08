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
from permguard.az.azreq.model import Subject


# Valore predefinito per Subject
SUBJECT_DEFAULT_KIND = "user"

# Tipi di Subject
USER_TYPE = "user"
ROLE_ACTOR_TYPE = "role-actor"
TWIN_ACTOR_TYPE = "twin-actor"


class SubjectBuilder:
    """Builder for creating a Subject object."""

    def __init__(self, id: str):
        """Initialize the builder with a default subject type."""
        self._subject = Subject(id=id, type=SUBJECT_DEFAULT_KIND, properties={})

    def with_user_type(self) -> "SubjectBuilder":
        """Set the subject type to USER."""
        self._subject.type = USER_TYPE
        return self

    def with_role_actor_type(self) -> "SubjectBuilder":
        """Set the subject type to ROLE-ACTOR."""
        self._subject.type = ROLE_ACTOR_TYPE
        return self

    def with_twin_actor_type(self) -> "SubjectBuilder":
        """Set the subject type to TWIN-ACTOR."""
        self._subject.type = TWIN_ACTOR_TYPE
        return self

    def with_type(self, sub_type: str) -> "SubjectBuilder":
        """Set the subject type."""
        self._subject.type = sub_type
        return self

    def with_source(self, source: str) -> "SubjectBuilder":
        """Set the source of the subject."""
        self._subject.source = source
        return self

    def with_property(self, key: str, value: Any) -> "SubjectBuilder":
        """Set a property of the subject."""
        self._subject.properties[key] = value
        return self

    def build(self) -> Subject:
        """Build and return the Subject object."""
        return self._subject.model_copy(deep=True)
