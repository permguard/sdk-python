# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

import grpc


class Refusal(Exception):
    """A structured PDP failure. A deny is a successful response, not a refusal.

    A call that fails in the client is a refusal too, the same on HTTP and gRPC and in every
    Permguard SDK: class `unavailable`, code `timeout` when the call's timeout passed, code
    `unreachable` when the data plane could not be reached (BUG-0284).
    """

    UNAVAILABLE = 'unavailable'
    TIMEOUT = 'timeout'
    UNREACHABLE = 'unreachable'

    def __init__(
        self,
        error_class: str,
        code: str,
        message: str,
        *,
        http_status: Optional[int] = None,
        grpc_code: Optional[grpc.StatusCode] = None,
    ) -> None:
        super().__init__(f'{code}: {message}' if code else message)
        self.error_class = error_class
        self.code = code
        self.message = message
        self.http_status = http_status
        self.grpc_code = grpc_code
