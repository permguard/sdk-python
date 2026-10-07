# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional, Protocol

from permguard.models import Configuration, EvaluateRequest, EvaluateResponse


class Transport(Protocol):
    def evaluate(self, request: EvaluateRequest, many: bool, timeout: Optional[float]) -> EvaluateResponse: ...

    def configuration(self, timeout: Optional[float]) -> Configuration: ...

    def close(self) -> None: ...
