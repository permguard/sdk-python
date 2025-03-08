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

from typing import Callable, Optional


class AZEndpoint:
    """Represents the authorization server endpoint."""
    
    def __init__(self, endpoint: str, port: int):
        self.endpoint = endpoint
        self.port = port


class AZConfig:
    """Configuration for the authorization client."""
    
    def __init__(self):
        self.pdp_endpoint: Optional[AZEndpoint] = None

    def apply(self, option: Callable[["AZConfig"], None]) -> "AZConfig":
        """Apply an AZOption function to modify the configuration."""
        option(self)
        return self


def with_endpoint(endpoint: str, port: int) -> Callable[[AZConfig], None]:
    """Set the gRPC endpoint for the authorization server."""
    return lambda c: setattr(c, "pdp_endpoint", AZEndpoint(endpoint, port))
