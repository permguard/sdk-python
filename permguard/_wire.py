# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional

from google.protobuf import json_format, struct_pb2

from permguard.data.v1 import pdp_pb2
from permguard.models import (
    Action,
    Configuration,
    Decision,
    DecisionContext,
    Endpoints,
    Entity,
    EvaluateRequest,
    EvaluateResponse,
    Evaluation,
    EvaluationOptions,
    EvaluationsSemantic,
    PartitionInput,
    PartitionInputs,
    Reason,
    StoreScope,
)

MAX_EXACT_PROTO_INTEGER = (1 << 53) - 1


def request_to_dict(request: EvaluateRequest) -> Dict[str, Any]:
    """Render the canonical HTTP/JSON request without losing field presence."""

    payload: Dict[str, Any] = {'zone': request.zone, 'ledger': request.ledger}
    _put(payload, 'profile', request.profile)
    _put(payload, 'subject', _entity_to_dict(request.subject))
    _put(payload, 'resource', _entity_to_dict(request.resource))
    _put(payload, 'action', _action_to_dict(request.action))
    _put(payload, 'context', request.context)
    _put(payload, 'principal', _entity_to_dict(request.principal))
    if request.partition_inputs:
        payload['partition_inputs'] = _inputs_to_dict(request.partition_inputs)
    if request.evaluations:
        payload['evaluations'] = [_evaluation_to_dict(item) for item in request.evaluations]
    if request.options is not None:
        options = _options_to_dict(request.options)
        if options:
            payload['options'] = options
    _put(payload, 'request_id', request.request_id)
    return payload


def response_from_dict(payload: Mapping[str, Any]) -> EvaluateResponse:
    return EvaluateResponse(
        decision=bool(payload.get('decision', False)),
        request_id=_optional_text(payload.get('request_id')),
        context=_context_from_dict(payload.get('context')),
        evaluations=[_decision_from_dict(item) for item in payload.get('evaluations', [])],
    )


def configuration_from_dict(payload: Mapping[str, Any]) -> Configuration:
    endpoints = payload.get('endpoints') or {}
    scope = payload.get('store_scope') or {}
    return Configuration(
        interface=str(payload.get('interface', '')),
        pdp=str(payload.get('pdp', '')),
        endpoints=Endpoints(
            evaluation=str(endpoints.get('evaluation', '')),
            evaluations=str(endpoints.get('evaluations', '')),
        ),
        capabilities=[str(item) for item in payload.get('capabilities', [])],
        store_scope=StoreScope(
            in_=str(scope.get('in', '')),
            zone=str(scope.get('zone', '')),
            ledger=str(scope.get('ledger', '')),
            profile=str(scope.get('profile', '')),
        ),
    )


def request_to_proto(request: EvaluateRequest) -> pdp_pb2.EvaluateRequest:
    semantic = _semantic_to_proto(request.options)
    return pdp_pb2.EvaluateRequest(
        zone=request.zone,
        ledger=request.ledger,
        profile=request.profile or '',
        subject=_entity_to_proto(request.subject),
        resource=_entity_to_proto(request.resource),
        action=_action_to_proto(request.action),
        context=_struct_to_proto(request.context),
        principal=_entity_to_proto(request.principal),
        evaluations=[_evaluation_to_proto(item) for item in request.evaluations],
        evaluations_semantic=semantic,
        request_id=request.request_id or '',
        partition_inputs=_inputs_to_proto(request.partition_inputs),
    )


def response_from_proto(response: pdp_pb2.EvaluateResponse) -> EvaluateResponse:
    return EvaluateResponse(
        decision=response.decision,
        request_id=response.request_id or None,
        context=_context_from_proto(response.context) if response.HasField('context') else None,
        evaluations=[_decision_from_proto(item) for item in response.evaluations],
    )


def configuration_from_proto(response: pdp_pb2.GetConfigurationResponse) -> Configuration:
    endpoints = response.endpoints if response.HasField('endpoints') else pdp_pb2.Endpoints()
    scope = response.store_scope if response.HasField('store_scope') else pdp_pb2.StoreScope()
    return Configuration(
        interface=response.interface,
        pdp=response.pdp,
        endpoints=Endpoints(evaluation=endpoints.evaluation, evaluations=endpoints.evaluations),
        capabilities=list(response.capabilities),
        store_scope=StoreScope(
            in_=getattr(scope, 'in'),
            zone=scope.zone,
            ledger=scope.ledger,
            profile=scope.profile,
        ),
    )


def _put(target: Dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        target[key] = value


def _entity_to_dict(entity: Optional[Entity]) -> Optional[Dict[str, Any]]:
    if entity is None:
        return None
    value: Dict[str, Any] = {'type': entity.type, 'id': entity.id}
    if entity.properties:
        value['properties'] = entity.properties
    return value


def _action_to_dict(action: Optional[Action]) -> Optional[Dict[str, Any]]:
    if action is None:
        return None
    value: Dict[str, Any] = {'name': action.name}
    if action.properties:
        value['properties'] = action.properties
    return value


def _input_to_dict(value: PartitionInput) -> Dict[str, Any]:
    result: Dict[str, Any] = {'type': value.type}
    _put(result, 'data', value.data)
    return result


def _inputs_to_dict(inputs: PartitionInputs) -> Dict[str, Any]:
    return {name: _input_to_dict(value) for name, value in inputs.items()}


def _evaluation_to_dict(evaluation: Evaluation) -> Dict[str, Any]:
    value: Dict[str, Any] = {}
    _put(value, 'subject', _entity_to_dict(evaluation.subject))
    _put(value, 'resource', _entity_to_dict(evaluation.resource))
    _put(value, 'action', _action_to_dict(evaluation.action))
    _put(value, 'context', evaluation.context)
    if evaluation.partition_inputs is not None:
        value['partition_inputs'] = _inputs_to_dict(evaluation.partition_inputs)
    _put(value, 'request_id', evaluation.request_id)
    return value


def _options_to_dict(options: EvaluationOptions) -> Dict[str, Any]:
    if options.evaluations_semantic is None:
        return {}
    return {'evaluations_semantic': options.evaluations_semantic.value}


def _entity_to_proto(entity: Optional[Entity]) -> Optional[pdp_pb2.Entity]:
    if entity is None:
        return None
    return pdp_pb2.Entity(type=entity.type, id=entity.id, properties=_struct_to_proto(entity.properties))


def _action_to_proto(action: Optional[Action]) -> Optional[pdp_pb2.Action]:
    if action is None:
        return None
    return pdp_pb2.Action(name=action.name, properties=_struct_to_proto(action.properties))


def _struct_to_proto(value: Optional[Mapping[str, Any]]) -> Optional[struct_pb2.Struct]:
    if value is None:
        return None
    _check_proto_numbers(value)
    return json_format.ParseDict(dict(value), struct_pb2.Struct())


def _value_to_proto(value: Any) -> Optional[struct_pb2.Value]:
    if value is None:
        return None
    _check_proto_numbers(value)
    return json_format.ParseDict(value, struct_pb2.Value())


def _inputs_to_proto(inputs: PartitionInputs) -> Dict[str, pdp_pb2.PartitionInput]:
    return {
        name: pdp_pb2.PartitionInput(type=value.type, data=_value_to_proto(value.data))
        for name, value in inputs.items()
    }


def _evaluation_to_proto(evaluation: Evaluation) -> pdp_pb2.Evaluation:
    result = pdp_pb2.Evaluation(
        subject=_entity_to_proto(evaluation.subject),
        resource=_entity_to_proto(evaluation.resource),
        action=_action_to_proto(evaluation.action),
        context=_struct_to_proto(evaluation.context),
        request_id=evaluation.request_id or '',
    )
    if evaluation.partition_inputs is not None:
        result.partition_inputs.CopyFrom(pdp_pb2.PartitionInputs(inputs=_inputs_to_proto(evaluation.partition_inputs)))
    return result


def _semantic_to_proto(options: Optional[EvaluationOptions]) -> pdp_pb2.EvaluationsSemantic:
    if options is None or options.evaluations_semantic is None:
        return pdp_pb2.EVALUATIONS_SEMANTIC_UNSPECIFIED
    values = {
        EvaluationsSemantic.EXECUTE_ALL: pdp_pb2.EVALUATIONS_SEMANTIC_EXECUTE_ALL,
        EvaluationsSemantic.DENY_ON_FIRST_DENY: pdp_pb2.EVALUATIONS_SEMANTIC_DENY_ON_FIRST_DENY,
        EvaluationsSemantic.PERMIT_ON_FIRST_PERMIT: pdp_pb2.EVALUATIONS_SEMANTIC_PERMIT_ON_FIRST_PERMIT,
    }
    try:
        return values[options.evaluations_semantic]
    except KeyError as error:
        raise ValueError(f'unknown evaluations semantic {options.evaluations_semantic!r}') from error


def _decision_from_dict(payload: Mapping[str, Any]) -> Decision:
    return Decision(
        decision=bool(payload.get('decision', False)),
        request_id=_optional_text(payload.get('request_id')),
        context=_context_from_dict(payload.get('context')),
    )


def _context_from_dict(payload: Any) -> Optional[DecisionContext]:
    if not isinstance(payload, Mapping):
        return None
    return DecisionContext(
        id=_optional_text(payload.get('id')),
        reason_admin=_reason_from_dict(payload.get('reason_admin')),
        reason_user=_reason_from_dict(payload.get('reason_user')),
        policies=[str(item) for item in payload.get('policies', [])],
        absent_inputs=[str(item) for item in payload.get('absent_inputs', [])],
    )


def _reason_from_dict(payload: Any) -> Optional[Reason]:
    if not isinstance(payload, Mapping):
        return None
    return Reason(code=str(payload.get('code', '')), message=str(payload.get('message', '')))


def _decision_from_proto(decision: pdp_pb2.Decision) -> Decision:
    return Decision(
        decision=decision.decision,
        request_id=decision.request_id or None,
        context=_context_from_proto(decision.context) if decision.HasField('context') else None,
    )


def _context_from_proto(context: pdp_pb2.DecisionContext) -> DecisionContext:
    return DecisionContext(
        id=context.id or None,
        reason_admin=_reason_from_proto(context.reason_admin) if context.HasField('reason_admin') else None,
        reason_user=_reason_from_proto(context.reason_user) if context.HasField('reason_user') else None,
        policies=list(context.policies),
        absent_inputs=list(context.absent_inputs),
    )


def _reason_from_proto(reason: pdp_pb2.Reason) -> Reason:
    return Reason(code=reason.code, message=reason.message)


def _optional_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value)
    return text or None


def _check_proto_numbers(value: Any) -> None:
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, int):
        if value > MAX_EXACT_PROTO_INTEGER or value < -MAX_EXACT_PROTO_INTEGER:
            raise ValueError(f'integer {value} is not exactly representable by protobuf Value')
        return
    if isinstance(value, Mapping):
        for held in value.values():
            _check_proto_numbers(held)
        return
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray)):
        for held in value:
            _check_proto_numbers(held)
