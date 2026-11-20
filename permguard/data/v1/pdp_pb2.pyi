# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EvaluationsSemantic(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVALUATIONS_SEMANTIC_UNSPECIFIED: _ClassVar[EvaluationsSemantic]
    EVALUATIONS_SEMANTIC_EXECUTE_ALL: _ClassVar[EvaluationsSemantic]
    EVALUATIONS_SEMANTIC_DENY_ON_FIRST_DENY: _ClassVar[EvaluationsSemantic]
    EVALUATIONS_SEMANTIC_PERMIT_ON_FIRST_PERMIT: _ClassVar[EvaluationsSemantic]

class SubmitOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBMIT_OUTCOME_UNSPECIFIED: _ClassVar[SubmitOutcome]
    SUBMIT_OUTCOME_DECIDED: _ClassVar[SubmitOutcome]
    SUBMIT_OUTCOME_ACCEPTED: _ClassVar[SubmitOutcome]
    SUBMIT_OUTCOME_INDETERMINATE: _ClassVar[SubmitOutcome]
EVALUATIONS_SEMANTIC_UNSPECIFIED: EvaluationsSemantic
EVALUATIONS_SEMANTIC_EXECUTE_ALL: EvaluationsSemantic
EVALUATIONS_SEMANTIC_DENY_ON_FIRST_DENY: EvaluationsSemantic
EVALUATIONS_SEMANTIC_PERMIT_ON_FIRST_PERMIT: EvaluationsSemantic
SUBMIT_OUTCOME_UNSPECIFIED: SubmitOutcome
SUBMIT_OUTCOME_DECIDED: SubmitOutcome
SUBMIT_OUTCOME_ACCEPTED: SubmitOutcome
SUBMIT_OUTCOME_INDETERMINATE: SubmitOutcome

class Entity(_message.Message):
    __slots__ = ("type", "id", "properties")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    type: str
    id: str
    properties: _struct_pb2.Struct
    def __init__(self, type: _Optional[str] = ..., id: _Optional[str] = ..., properties: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Action(_message.Message):
    __slots__ = ("name", "properties")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    properties: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., properties: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class PartitionInput(_message.Message):
    __slots__ = ("type", "data")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    type: str
    data: _struct_pb2.Value
    def __init__(self, type: _Optional[str] = ..., data: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class PartitionInputs(_message.Message):
    __slots__ = ("inputs",)
    class InputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PartitionInput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PartitionInput, _Mapping]] = ...) -> None: ...
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.MessageMap[str, PartitionInput]
    def __init__(self, inputs: _Optional[_Mapping[str, PartitionInput]] = ...) -> None: ...

class Evaluation(_message.Message):
    __slots__ = ("subject", "resource", "action", "context", "request_id", "partition_inputs")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PARTITION_INPUTS_FIELD_NUMBER: _ClassVar[int]
    subject: Entity
    resource: Entity
    action: Action
    context: _struct_pb2.Struct
    request_id: str
    partition_inputs: PartitionInputs
    def __init__(self, subject: _Optional[_Union[Entity, _Mapping]] = ..., resource: _Optional[_Union[Entity, _Mapping]] = ..., action: _Optional[_Union[Action, _Mapping]] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., request_id: _Optional[str] = ..., partition_inputs: _Optional[_Union[PartitionInputs, _Mapping]] = ...) -> None: ...

class EvaluateRequest(_message.Message):
    __slots__ = ("zone", "ledger", "profile", "subject", "resource", "action", "context", "principal", "evaluations", "evaluations_semantic", "request_id", "partition_inputs", "request_nonce")
    class PartitionInputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PartitionInput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PartitionInput, _Mapping]] = ...) -> None: ...
    ZONE_FIELD_NUMBER: _ClassVar[int]
    LEDGER_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONS_SEMANTIC_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PARTITION_INPUTS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_NONCE_FIELD_NUMBER: _ClassVar[int]
    zone: str
    ledger: str
    profile: str
    subject: Entity
    resource: Entity
    action: Action
    context: _struct_pb2.Struct
    principal: Entity
    evaluations: _containers.RepeatedCompositeFieldContainer[Evaluation]
    evaluations_semantic: EvaluationsSemantic
    request_id: str
    partition_inputs: _containers.MessageMap[str, PartitionInput]
    request_nonce: str
    def __init__(self, zone: _Optional[str] = ..., ledger: _Optional[str] = ..., profile: _Optional[str] = ..., subject: _Optional[_Union[Entity, _Mapping]] = ..., resource: _Optional[_Union[Entity, _Mapping]] = ..., action: _Optional[_Union[Action, _Mapping]] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., principal: _Optional[_Union[Entity, _Mapping]] = ..., evaluations: _Optional[_Iterable[_Union[Evaluation, _Mapping]]] = ..., evaluations_semantic: _Optional[_Union[EvaluationsSemantic, str]] = ..., request_id: _Optional[str] = ..., partition_inputs: _Optional[_Mapping[str, PartitionInput]] = ..., request_nonce: _Optional[str] = ...) -> None: ...

class Reason(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class DecisionContext(_message.Message):
    __slots__ = ("id", "reason_admin", "reason_user", "policies", "absent_inputs", "evidence")
    ID_FIELD_NUMBER: _ClassVar[int]
    REASON_ADMIN_FIELD_NUMBER: _ClassVar[int]
    REASON_USER_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    ABSENT_INPUTS_FIELD_NUMBER: _ClassVar[int]
    EVIDENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    reason_admin: Reason
    reason_user: Reason
    policies: _containers.RepeatedScalarFieldContainer[str]
    absent_inputs: _containers.RepeatedScalarFieldContainer[str]
    evidence: Evidence
    def __init__(self, id: _Optional[str] = ..., reason_admin: _Optional[_Union[Reason, _Mapping]] = ..., reason_user: _Optional[_Union[Reason, _Mapping]] = ..., policies: _Optional[_Iterable[str]] = ..., absent_inputs: _Optional[_Iterable[str]] = ..., evidence: _Optional[_Union[Evidence, _Mapping]] = ...) -> None: ...

class Evidence(_message.Message):
    __slots__ = ("mode", "status", "record_id", "position")
    MODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    mode: str
    status: str
    record_id: str
    position: EvidencePosition
    def __init__(self, mode: _Optional[str] = ..., status: _Optional[str] = ..., record_id: _Optional[str] = ..., position: _Optional[_Union[EvidencePosition, _Mapping]] = ...) -> None: ...

class EvidencePosition(_message.Message):
    __slots__ = ("host_id", "run", "sequence")
    HOST_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    host_id: str
    run: str
    sequence: str
    def __init__(self, host_id: _Optional[str] = ..., run: _Optional[str] = ..., sequence: _Optional[str] = ...) -> None: ...

class Decision(_message.Message):
    __slots__ = ("decision", "request_id", "context")
    DECISION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    decision: bool
    request_id: str
    context: DecisionContext
    def __init__(self, decision: bool = ..., request_id: _Optional[str] = ..., context: _Optional[_Union[DecisionContext, _Mapping]] = ...) -> None: ...

class EvaluateResponse(_message.Message):
    __slots__ = ("decision", "request_id", "context", "evaluations", "attestation")
    DECISION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    decision: bool
    request_id: str
    context: DecisionContext
    evaluations: _containers.RepeatedCompositeFieldContainer[Decision]
    attestation: Attestation
    def __init__(self, decision: bool = ..., request_id: _Optional[str] = ..., context: _Optional[_Union[DecisionContext, _Mapping]] = ..., evaluations: _Optional[_Iterable[_Union[Decision, _Mapping]]] = ..., attestation: _Optional[_Union[Attestation, _Mapping]] = ...) -> None: ...

class Attestation(_message.Message):
    __slots__ = ("protected", "payload", "signature")
    PROTECTED_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    protected: str
    payload: str
    signature: str
    def __init__(self, protected: _Optional[str] = ..., payload: _Optional[str] = ..., signature: _Optional[str] = ...) -> None: ...

class GetConfigurationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Endpoints(_message.Message):
    __slots__ = ("evaluation", "evaluations")
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    evaluation: str
    evaluations: str
    def __init__(self, evaluation: _Optional[str] = ..., evaluations: _Optional[str] = ...) -> None: ...

class StoreScope(_message.Message):
    __slots__ = ("zone", "ledger", "profile")
    IN_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    LEDGER_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    zone: str
    ledger: str
    profile: str
    def __init__(self, zone: _Optional[str] = ..., ledger: _Optional[str] = ..., profile: _Optional[str] = ..., **kwargs) -> None: ...

class GetConfigurationResponse(_message.Message):
    __slots__ = ("interface", "pdp", "endpoints", "capabilities", "store_scope", "version", "component", "state", "stage", "sunset", "limits", "response_signing")
    class LimitsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    PDP_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    STORE_SCOPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    SUNSET_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_SIGNING_FIELD_NUMBER: _ClassVar[int]
    interface: str
    pdp: str
    endpoints: Endpoints
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    store_scope: StoreScope
    version: str
    component: str
    state: str
    stage: str
    sunset: str
    limits: _containers.ScalarMap[str, int]
    response_signing: ResponseSigning
    def __init__(self, interface: _Optional[str] = ..., pdp: _Optional[str] = ..., endpoints: _Optional[_Union[Endpoints, _Mapping]] = ..., capabilities: _Optional[_Iterable[str]] = ..., store_scope: _Optional[_Union[StoreScope, _Mapping]] = ..., version: _Optional[str] = ..., component: _Optional[str] = ..., state: _Optional[str] = ..., stage: _Optional[str] = ..., sunset: _Optional[str] = ..., limits: _Optional[_Mapping[str, int]] = ..., response_signing: _Optional[_Union[ResponseSigning, _Mapping]] = ...) -> None: ...

class ResponseSigning(_message.Message):
    __slots__ = ("state", "validity_seconds", "clock_skew_seconds")
    STATE_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CLOCK_SKEW_SECONDS_FIELD_NUMBER: _ClassVar[int]
    state: str
    validity_seconds: int
    clock_skew_seconds: int
    def __init__(self, state: _Optional[str] = ..., validity_seconds: _Optional[int] = ..., clock_skew_seconds: _Optional[int] = ...) -> None: ...

class GetTemporalSignersRequest(_message.Message):
    __slots__ = ("zone", "ledger", "from_seq", "until_seq")
    ZONE_FIELD_NUMBER: _ClassVar[int]
    LEDGER_FIELD_NUMBER: _ClassVar[int]
    FROM_SEQ_FIELD_NUMBER: _ClassVar[int]
    UNTIL_SEQ_FIELD_NUMBER: _ClassVar[int]
    zone: str
    ledger: str
    from_seq: int
    until_seq: int
    def __init__(self, zone: _Optional[str] = ..., ledger: _Optional[str] = ..., from_seq: _Optional[int] = ..., until_seq: _Optional[int] = ...) -> None: ...

class TemporalSignerSpan(_message.Message):
    __slots__ = ("from_seq", "kid", "jwk")
    FROM_SEQ_FIELD_NUMBER: _ClassVar[int]
    KID_FIELD_NUMBER: _ClassVar[int]
    JWK_FIELD_NUMBER: _ClassVar[int]
    from_seq: int
    kid: str
    jwk: bytes
    def __init__(self, from_seq: _Optional[int] = ..., kid: _Optional[str] = ..., jwk: _Optional[bytes] = ...) -> None: ...

class GetTemporalSignersResponse(_message.Message):
    __slots__ = ("producer_class", "producer", "instance", "durable_through", "signed_through", "acked_through", "spans")
    PRODUCER_CLASS_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    DURABLE_THROUGH_FIELD_NUMBER: _ClassVar[int]
    SIGNED_THROUGH_FIELD_NUMBER: _ClassVar[int]
    ACKED_THROUGH_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    producer_class: str
    producer: str
    instance: str
    durable_through: int
    signed_through: int
    acked_through: int
    spans: _containers.RepeatedCompositeFieldContainer[TemporalSignerSpan]
    def __init__(self, producer_class: _Optional[str] = ..., producer: _Optional[str] = ..., instance: _Optional[str] = ..., durable_through: _Optional[int] = ..., signed_through: _Optional[int] = ..., acked_through: _Optional[int] = ..., spans: _Optional[_Iterable[_Union[TemporalSignerSpan, _Mapping]]] = ...) -> None: ...

class EventStore(_message.Message):
    __slots__ = ("zone", "ledger", "profile")
    ZONE_FIELD_NUMBER: _ClassVar[int]
    LEDGER_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    zone: str
    ledger: str
    profile: str
    def __init__(self, zone: _Optional[str] = ..., ledger: _Optional[str] = ..., profile: _Optional[str] = ...) -> None: ...

class TypedEvent(_message.Message):
    __slots__ = ("type", "data")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    type: str
    data: _struct_pb2.Struct
    def __init__(self, type: _Optional[str] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SubmitEventRequest(_message.Message):
    __slots__ = ("store", "event")
    STORE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    store: EventStore
    event: TypedEvent
    def __init__(self, store: _Optional[_Union[EventStore, _Mapping]] = ..., event: _Optional[_Union[TypedEvent, _Mapping]] = ...) -> None: ...

class EventWatermark(_message.Message):
    __slots__ = ("instance", "sequence", "history")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    instance: str
    sequence: int
    history: str
    def __init__(self, instance: _Optional[str] = ..., sequence: _Optional[int] = ..., history: _Optional[str] = ...) -> None: ...

class SubmitEventResponse(_message.Message):
    __slots__ = ("outcome", "event_id", "watermark", "decision", "decision_id", "policies", "reason", "history", "evaluations")
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    DECISION_ID_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    outcome: SubmitOutcome
    event_id: str
    watermark: EventWatermark
    decision: _wrappers_pb2.BoolValue
    decision_id: str
    policies: _containers.RepeatedScalarFieldContainer[str]
    reason: Reason
    history: DecisionHistory
    evaluations: _containers.RepeatedCompositeFieldContainer[TemporalPartitionEvaluation]
    def __init__(self, outcome: _Optional[_Union[SubmitOutcome, str]] = ..., event_id: _Optional[str] = ..., watermark: _Optional[_Union[EventWatermark, _Mapping]] = ..., decision: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., decision_id: _Optional[str] = ..., policies: _Optional[_Iterable[str]] = ..., reason: _Optional[_Union[Reason, _Mapping]] = ..., history: _Optional[_Union[DecisionHistory, _Mapping]] = ..., evaluations: _Optional[_Iterable[_Union[TemporalPartitionEvaluation, _Mapping]]] = ...) -> None: ...

class TemporalPartitionEvaluation(_message.Message):
    __slots__ = ("partition", "decision", "policies", "reason")
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    partition: str
    decision: bool
    policies: _containers.RepeatedScalarFieldContainer[str]
    reason: Reason
    def __init__(self, partition: _Optional[str] = ..., decision: bool = ..., policies: _Optional[_Iterable[str]] = ..., reason: _Optional[_Union[Reason, _Mapping]] = ...) -> None: ...

class DecisionHistory(_message.Message):
    __slots__ = ("mode", "watermark", "staleness_seconds", "gaps", "frontier", "origin_set_revision", "max_staleness_seconds", "degraded", "time", "quarantined")
    MODE_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    STALENESS_SECONDS_FIELD_NUMBER: _ClassVar[int]
    GAPS_FIELD_NUMBER: _ClassVar[int]
    FRONTIER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SET_REVISION_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    QUARANTINED_FIELD_NUMBER: _ClassVar[int]
    mode: str
    watermark: str
    staleness_seconds: int
    gaps: int
    frontier: _containers.RepeatedCompositeFieldContainer[FrontierRun]
    origin_set_revision: str
    max_staleness_seconds: int
    degraded: _containers.RepeatedScalarFieldContainer[str]
    time: str
    quarantined: int
    def __init__(self, mode: _Optional[str] = ..., watermark: _Optional[str] = ..., staleness_seconds: _Optional[int] = ..., gaps: _Optional[int] = ..., frontier: _Optional[_Iterable[_Union[FrontierRun, _Mapping]]] = ..., origin_set_revision: _Optional[str] = ..., max_staleness_seconds: _Optional[int] = ..., degraded: _Optional[_Iterable[str]] = ..., time: _Optional[str] = ..., quarantined: _Optional[int] = ...) -> None: ...

class FrontierRun(_message.Message):
    __slots__ = ("origin", "run", "covered_through", "low_watermark", "gaps")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    COVERED_THROUGH_FIELD_NUMBER: _ClassVar[int]
    LOW_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    GAPS_FIELD_NUMBER: _ClassVar[int]
    origin: str
    run: str
    covered_through: int
    low_watermark: int
    gaps: _containers.RepeatedCompositeFieldContainer[FrontierGap]
    def __init__(self, origin: _Optional[str] = ..., run: _Optional[str] = ..., covered_through: _Optional[int] = ..., low_watermark: _Optional[int] = ..., gaps: _Optional[_Iterable[_Union[FrontierGap, _Mapping]]] = ...) -> None: ...

class FrontierGap(_message.Message):
    __slots__ = ("through",)
    FROM_FIELD_NUMBER: _ClassVar[int]
    THROUGH_FIELD_NUMBER: _ClassVar[int]
    through: int
    def __init__(self, through: _Optional[int] = ..., **kwargs) -> None: ...

class GetTemporalConfigurationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TemporalEndpoints(_message.Message):
    __slots__ = ("submission",)
    SUBMISSION_FIELD_NUMBER: _ClassVar[int]
    submission: str
    def __init__(self, submission: _Optional[str] = ...) -> None: ...

class GetTemporalConfigurationResponse(_message.Message):
    __slots__ = ("interface", "pdp", "endpoints", "event_types", "capabilities", "store_scope", "version", "component", "state", "stage", "sunset", "limits")
    class LimitsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    PDP_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    STORE_SCOPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    SUNSET_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    interface: str
    pdp: str
    endpoints: TemporalEndpoints
    event_types: _containers.RepeatedScalarFieldContainer[str]
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    store_scope: StoreScope
    version: str
    component: str
    state: str
    stage: str
    sunset: str
    limits: _containers.ScalarMap[str, int]
    def __init__(self, interface: _Optional[str] = ..., pdp: _Optional[str] = ..., endpoints: _Optional[_Union[TemporalEndpoints, _Mapping]] = ..., event_types: _Optional[_Iterable[str]] = ..., capabilities: _Optional[_Iterable[str]] = ..., store_scope: _Optional[_Union[StoreScope, _Mapping]] = ..., version: _Optional[str] = ..., component: _Optional[str] = ..., state: _Optional[str] = ..., stage: _Optional[str] = ..., sunset: _Optional[str] = ..., limits: _Optional[_Mapping[str, int]] = ...) -> None: ...
