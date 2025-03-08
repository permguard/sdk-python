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

from typing import Optional, Tuple

from permguard.internal.az.azreq.grpc.v1.pdp_client import authorization_check
from permguard.az_config import AZConfig, AZEndpoint
from permguard.az.azreq.model import AZRequest, AZResponse


class AZClient:
    """Client to interact with the authorization server."""

    def __init__(self, *opts):
        """Initialize the authorization client with optional configuration options."""
        self._az_config = AZConfig()
        self._az_config.pdp_endpoint = AZEndpoint(endpoint="localhost", port=9094)

        # Apply configuration options
        for opt in opts:
            opt(self._az_config)

    def check(self, req: AZRequest) -> Tuple[bool, Optional[AZResponse]]:
        """Check the input authorization request with the authorization server."""
        target = f"{self._az_config.pdp_endpoint.endpoint}:{self._az_config.pdp_endpoint.port}"
       
        can_execute = authorization_check(target, req)
        decision = can_execute.decision if can_execute else False
        return decision, can_execute
