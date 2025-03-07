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

from copy import deepcopy


# Constants
SUBJECT_DEFAULT_KIND = "USER"
USER_TYPE = "USER"
ROLE_ACTOR_TYPE = "ROLE-ACTOR"
TWIN_ACTOR_TYPE = "TWIN-ACTOR"


class Subject:
    """Class representing a subject."""
    def __init__(self, id: str):
        self.id = id
        self.type = SUBJECT_DEFAULT_KIND
        self.source = None
        self.properties = None


class SubjectBuilder:
    """Builder for the Subject object."""
    def __init__(self, id: str):
        # Initialize the builder with a new Subject instance
        self.subject = Subject(id)

    def with_user_type(self) -> 'SubjectBuilder':
        """Sets the type of the subject to UserType for the AZRequest."""
        self.subject.type = USER_TYPE
        return self

    def with_role_actor_type(self) -> 'SubjectBuilder':
        """Sets the type of the subject to RoleActorType for the AZRequest."""
        self.subject.type = ROLE_ACTOR_TYPE
        return self

    def with_twin_actor_type(self) -> 'SubjectBuilder':
        """Sets the type of the subject to TwinActorType for the AZRequest."""
        self.subject.type = TWIN_ACTOR_TYPE
        return self

    def with_type(self, subject_type: str) -> 'SubjectBuilder':
        """Sets the type of the subject."""
        self.subject.type = subject_type
        return self

    def with_source(self, source: str) -> 'SubjectBuilder':
        """Sets the source of the subject."""
        self.subject.source = source
        return self

    def with_property(self, key: str, value: any) -> 'SubjectBuilder':
        """Sets a property of the subject."""
        # Initialize properties dictionary if it doesn't exist
        if self.subject.properties is None:
            self.subject.properties = {}
        self.subject.properties[key] = value
        return self

    def build(self) -> Subject:
        """Builds and returns the Subject object with a deep copy of properties."""
        # Create a new Subject instance with the same ID
        instance = Subject(self.subject.id)
        # Copy the type, source, and properties
        instance.type = self.subject.type
        instance.source = self.subject.source
        # Deep copy the properties if they exist, otherwise keep as None
        instance.properties = deepcopy(self.subject.properties) if self.subject.properties else None
        return instance
