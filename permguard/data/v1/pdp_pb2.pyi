# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from google.protobuf import struct_pb2 as _struct_pb2
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
EVALUATIONS_SEMANTIC_UNSPECIFIED: EvaluationsSemantic
EVALUATIONS_SEMANTIC_EXECUTE_ALL: EvaluationsSemantic
EVALUATIONS_SEMANTIC_DENY_ON_FIRST_DENY: EvaluationsSemantic
EVALUATIONS_SEMANTIC_PERMIT_ON_FIRST_PERMIT: EvaluationsSemantic

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
    __slots__ = ("zone", "ledger", "profile", "subject", "resource", "action", "context", "principal", "evaluations", "evaluations_semantic", "request_id", "partition_inputs")
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
    def __init__(self, zone: _Optional[str] = ..., ledger: _Optional[str] = ..., profile: _Optional[str] = ..., subject: _Optional[_Union[Entity, _Mapping]] = ..., resource: _Optional[_Union[Entity, _Mapping]] = ..., action: _Optional[_Union[Action, _Mapping]] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., principal: _Optional[_Union[Entity, _Mapping]] = ..., evaluations: _Optional[_Iterable[_Union[Evaluation, _Mapping]]] = ..., evaluations_semantic: _Optional[_Union[EvaluationsSemantic, str]] = ..., request_id: _Optional[str] = ..., partition_inputs: _Optional[_Mapping[str, PartitionInput]] = ...) -> None: ...

class Reason(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class DecisionContext(_message.Message):
    __slots__ = ("id", "reason_admin", "reason_user", "policies", "absent_inputs")
    ID_FIELD_NUMBER: _ClassVar[int]
    REASON_ADMIN_FIELD_NUMBER: _ClassVar[int]
    REASON_USER_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    ABSENT_INPUTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    reason_admin: Reason
    reason_user: Reason
    policies: _containers.RepeatedScalarFieldContainer[str]
    absent_inputs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., reason_admin: _Optional[_Union[Reason, _Mapping]] = ..., reason_user: _Optional[_Union[Reason, _Mapping]] = ..., policies: _Optional[_Iterable[str]] = ..., absent_inputs: _Optional[_Iterable[str]] = ...) -> None: ...

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
    __slots__ = ("decision", "request_id", "context", "evaluations")
    DECISION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    decision: bool
    request_id: str
    context: DecisionContext
    evaluations: _containers.RepeatedCompositeFieldContainer[Decision]
    def __init__(self, decision: bool = ..., request_id: _Optional[str] = ..., context: _Optional[_Union[DecisionContext, _Mapping]] = ..., evaluations: _Optional[_Iterable[_Union[Decision, _Mapping]]] = ...) -> None: ...

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
    __slots__ = ("interface", "pdp", "endpoints", "capabilities", "store_scope")
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    PDP_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    STORE_SCOPE_FIELD_NUMBER: _ClassVar[int]
    interface: str
    pdp: str
    endpoints: Endpoints
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    store_scope: StoreScope
    def __init__(self, interface: _Optional[str] = ..., pdp: _Optional[str] = ..., endpoints: _Optional[_Union[Endpoints, _Mapping]] = ..., capabilities: _Optional[_Iterable[str]] = ..., store_scope: _Optional[_Union[StoreScope, _Mapping]] = ...) -> None: ...
