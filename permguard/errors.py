# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

import grpc


class Refusal(Exception):
    """A structured PDP failure. A deny is a successful response, not a refusal."""

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
