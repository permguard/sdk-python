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
from permguard_sdk.az.azreq.model import AZRequest, AZResponse
from permguard_sdk.internal.az.azreq.grpc.v1 import pdp_pb2, pdp_pb2_grpc


def dict_to_struct(data: dict) -> Struct:
    """Convert a Python dictionary to a Protobuf Struct."""
    struct = Struct()
    struct.update(data)
    return struct


def map_az_request_to_grpc(az_request: AZRequest) -> pdp_pb2.AuthorizationCheckRequest:
    """Map AZRequest (Pydantic) to AuthorizationCheckRequest (gRPC Protobuf)."""
    
    if az_request is None:
        raise ValueError("Invalid AZRequest: input is None")

    auth_model = None
    if az_request.authorization_model:
        auth_model = pdp_pb2.AuthorizationModelRequest(
            ZoneID=az_request.authorization_model.zone_id,
            PolicyStore=pdp_pb2.PolicyStore(
                Kind=az_request.authorization_model.policy_store.kind if az_request.authorization_model.policy_store else "",
                ID=az_request.authorization_model.policy_store.id if az_request.authorization_model.policy_store else "",
            ),
            Principal=pdp_pb2.Principal(
                Type=az_request.authorization_model.principal.type if az_request.authorization_model.principal else "",
                ID=az_request.authorization_model.principal.id if az_request.authorization_model.principal else "",
                Source=az_request.authorization_model.principal.source if az_request.authorization_model.principal else "",
            ),
            Entities=pdp_pb2.Entities(
                Schema=az_request.authorization_model.entities.schema_name if az_request.authorization_model.entities else "",
                Items=[dict_to_struct(item) for item in az_request.authorization_model.entities.items] if az_request.authorization_model.entities else [],
            ),
        )

    subject = None
    if az_request.subject:
        subject = pdp_pb2.Subject(
            Type=az_request.subject.type,
            ID=az_request.subject.id,
            Source=az_request.subject.source,
            Properties=dict_to_struct(az_request.subject.properties) if az_request.subject.properties else Struct(),
        )

    resource = None
    if az_request.resource:
        resource = pdp_pb2.Resource(
            Type=az_request.resource.type,
            ID=az_request.resource.id,
            Properties=dict_to_struct(az_request.resource.properties) if az_request.resource.properties else Struct(),
        )

    action = None
    if az_request.action:
        action = pdp_pb2.Action(
            Name=az_request.action.name,
            Properties=dict_to_struct(az_request.action.properties) if az_request.action.properties else Struct(),
        )

    context = dict_to_struct(az_request.context) if az_request.context else Struct()

    evaluations = []
    if az_request.evaluations:
        evaluations = [
            pdp_pb2.EvaluationRequest(
                RequestID=eval.request_id,
                Subject=pdp_pb2.Subject(
                    Type=eval.subject.type if eval.subject else "",
                    ID=eval.subject.id if eval.subject else "",
                    Source=eval.subject.source if eval.subject else "",
                    Properties=dict_to_struct(eval.subject.properties) if eval.subject and eval.subject.properties else Struct(),
                ),
                Resource=pdp_pb2.Resource(
                    Type=eval.resource.type if eval.resource else "",
                    ID=eval.resource.id if eval.resource else "",
                    Properties=dict_to_struct(eval.resource.properties) if eval.resource and eval.resource.properties else Struct(),
                ),
                Action=pdp_pb2.Action(
                    Name=eval.action.name if eval.action else "",
                    Properties=dict_to_struct(eval.action.properties) if eval.action and eval.action.properties else Struct(),
                ),
                Context=dict_to_struct(eval.context) if eval.context else Struct(),
            )
            for eval in az_request.evaluations
        ]

    # Creazione della richiesta gRPC
    return pdp_pb2.AuthorizationCheckRequest(
        AuthorizationModel=auth_model,
        RequestID=az_request.request_id if az_request.request_id else "",
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
        grpc_response = stub.AuthorizationCheck(grpc_request)

        reponse_json = MessageToJson(grpc_response)
        response = AZResponse.model_validate_json(reponse_json)
        return response
