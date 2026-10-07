# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EvaluationsSemantic(str, Enum):
    """How a boxcarred request is executed and combined."""

    EXECUTE_ALL = 'execute_all'
    DENY_ON_FIRST_DENY = 'deny_on_first_deny'
    PERMIT_ON_FIRST_PERMIT = 'permit_on_first_permit'


@dataclass
class Entity:
    """A subject, resource, or caller."""

    type: str
    id: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Action:
    """The operation being evaluated."""

    name: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PartitionInput:
    """Runtime data addressed to one named profile partition."""

    type: str
    data: Any = None


PartitionInputs = Dict[str, PartitionInput]


@dataclass
class Evaluation:
    """One entry in a boxcarred request."""

    subject: Optional[Entity] = None
    resource: Optional[Entity] = None
    action: Optional[Action] = None
    context: Optional[Dict[str, Any]] = None
    partition_inputs: Optional[PartitionInputs] = None
    request_id: Optional[str] = None


@dataclass
class EvaluationOptions:
    """Boxcarred evaluation options."""

    evaluations_semantic: Optional[EvaluationsSemantic] = None


@dataclass
class EvaluateRequest:
    """The payload of ``permguard.api.pdp.native.v1``."""

    zone: str
    ledger: str
    profile: Optional[str] = None
    subject: Optional[Entity] = None
    resource: Optional[Entity] = None
    action: Optional[Action] = None
    context: Optional[Dict[str, Any]] = None
    principal: Optional[Entity] = None
    partition_inputs: PartitionInputs = field(default_factory=dict)
    evaluations: List[Evaluation] = field(default_factory=list)
    options: Optional[EvaluationOptions] = None
    request_id: Optional[str] = None


@dataclass
class Reason:
    code: str
    message: str


@dataclass
class DecisionContext:
    id: Optional[str] = None
    reason_admin: Optional[Reason] = None
    reason_user: Optional[Reason] = None
    policies: List[str] = field(default_factory=list)
    absent_inputs: List[str] = field(default_factory=list)


@dataclass
class Decision:
    decision: bool
    request_id: Optional[str] = None
    context: Optional[DecisionContext] = None


@dataclass
class EvaluateResponse:
    decision: bool
    request_id: Optional[str] = None
    context: Optional[DecisionContext] = None
    evaluations: List[Decision] = field(default_factory=list)


@dataclass
class Endpoints:
    evaluation: str
    evaluations: str


@dataclass
class StoreScope:
    in_: str
    zone: str
    ledger: str
    profile: str


@dataclass
class Configuration:
    interface: str
    pdp: str
    endpoints: Endpoints
    capabilities: List[str]
    store_scope: StoreScope
