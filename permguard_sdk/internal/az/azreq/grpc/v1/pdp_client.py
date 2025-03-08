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

import grpc
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToJson

from permguard.az.azreq.model import AZRequest, AZResponse
from permguard.internal.az.azreq.grpc.v1 import pdp_pb2, pdp_pb2_grpc


def dict_to_struct(data: dict) -> Struct:
    """Convert a Python dictionary to a Protobuf Struct."""
    struct = Struct()
    struct.update(data)
    return struct


def map_az_request_to_grpc(az_request: AZRequest) -> pdp_pb2.AuthorizationCheckRequest:
    """Map AZRequest (Pydantic) to AuthorizationCheckRequest (gRPC Protobuf)."""
    
    if az_request is None:
        raise ValueError("Invalid AZRequest: input is None")


    # Authorization Model
    auth_model = None
    if az_request.authorization_model:
        policy_store = None
        if az_request.authorization_model.policy_store:
            policy_store = pdp_pb2.PolicyStore(
                Kind=az_request.authorization_model.policy_store.kind,
                ID=az_request.authorization_model.policy_store.id,
            )
            if policy_store.Kind is None or policy_store.Kind == '':
                policy_store.Kind = 'ledger'

        principal = None
        if az_request.authorization_model.principal:
            principal = pdp_pb2.Principal(
                Type=az_request.authorization_model.principal.type,
                ID=az_request.authorization_model.principal.id,
                Source=az_request.authorization_model.principal.source,
            )

        entities = None
        if az_request.authorization_model.entities:
            entities = pdp_pb2.Entities(
                Schema=az_request.authorization_model.entities.schema_name,
                Items=[dict_to_struct(item) for item in az_request.authorization_model.entities.items],
            )

        auth_model = pdp_pb2.AuthorizationModelRequest(
            ZoneID=az_request.authorization_model.zone_id,
            PolicyStore=policy_store,
            Principal=principal,
            Entities=entities,
        )

    # Subject
    subject = None
    if az_request.subject:
        subject = pdp_pb2.Subject(
            Type=az_request.subject.type,
            ID=az_request.subject.id,
            Source=az_request.subject.source,
            Properties=dict_to_struct(az_request.subject.properties) if az_request.subject.properties else Struct(),
        )

    # Resource
    resource = None
    if az_request.resource:
        resource = pdp_pb2.Resource(
            Type=az_request.resource.type,
            ID=az_request.resource.id,
            Properties=dict_to_struct(az_request.resource.properties) if az_request.resource.properties else Struct(),
        )

    # Action
    action = None
    if az_request.action:
        action = pdp_pb2.Action(
            Name=az_request.action.name,
            Properties=dict_to_struct(az_request.action.properties) if az_request.action.properties else Struct(),
        )

    # Context
    context = dict_to_struct(az_request.context) if az_request.context else Struct()

    # Evaluations
    evaluations = []
    if az_request.evaluations:
        for eval in az_request.evaluations:
            eval_subject = None
            if eval.subject:
                eval_subject = pdp_pb2.Subject(
                    Type=eval.subject.type,
                    ID=eval.subject.id,
                    Source=eval.subject.source,
                    Properties=dict_to_struct(eval.subject.properties) if eval.subject.properties else Struct(),
                )

            eval_resource = None
            if eval.resource:
                eval_resource = pdp_pb2.Resource(
                    Type=eval.resource.type,
                    ID=eval.resource.id,
                    Properties=dict_to_struct(eval.resource.properties) if eval.resource.properties else Struct(),
                )

            eval_action = None
            if eval.action:
                eval_action = pdp_pb2.Action(
                    Name=eval.action.name,
                    Properties=dict_to_struct(eval.action.properties) if eval.action.properties else Struct(),
                )

            eval_context = dict_to_struct(eval.context) if eval.context else Struct()

            evaluations.append(
                pdp_pb2.EvaluationRequest(
                    RequestID=eval.request_id,
                    Subject=eval_subject,
                    Resource=eval_resource,
                    Action=eval_action,
                    Context=eval_context,
                )
            )

    # Creazione della richiesta gRPC
    return pdp_pb2.AuthorizationCheckRequest(
        AuthorizationModel=auth_model,
        RequestID=az_request.request_id,
        Subject=subject,
        Resource=resource,
        Action=action,
        Context=context,
        Evaluations=evaluations,
    )


def authorization_check(endpoint: str, az_request: AZRequest) -> AZResponse:
    """Execute gRPC authorization check and return AZResponse."""
    if az_request is None:
        raise ValueError("PEP: Invalid request")


    with grpc.insecure_channel(endpoint) as channel:
        stub = pdp_pb2_grpc.V1PDPServiceStub(channel)

        grpc_request = map_az_request_to_grpc(az_request)
        print(MessageToJson(grpc_request))
        grpc_response = stub.AuthorizationCheck(grpc_request)

        reponse_json = MessageToJson(grpc_response)
        response = AZResponse.model_validate_json(reponse_json)
        return response
