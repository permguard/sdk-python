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
from permguard_sdk.internal.az.azreq.grpc.v1 import pdp_pb2
from permguard_sdk.internal.az.azreq.grpc.v1 import pdp_pb2_grpc
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToJson

def run():
    channel = grpc.insecure_channel('localhost:9094')
    stub = pdp_pb2_grpc.V1PDPServiceStub(channel)

    entities_item = Struct()
    entities_item.update({
        "uid": {
            "type": "MagicFarmacia::Platform::BranchInfo",
            "id": "subscription"
        },
        "attrs": {
            "active": True
        },
        "parents": []
    })

    subject_properties = Struct()
    subject_properties.update({"isSuperUser": True})

    context_struct = Struct()
    context_struct.update({
        "time": "2025-01-23T16:17:46+00:00",
        "isSubscriptionActive": True
    })

    resource_properties = Struct()
    resource_properties.update({"isEnabled": True})

    action_properties_enabled = Struct()
    action_properties_enabled.update({"isEnabled": True})

    action_properties_disabled = Struct()
    action_properties_disabled.update({"isEnabled": False})

    auth_model = pdp_pb2.AuthorizationModelRequest(
        ZoneID=895741663247,
        PolicyStore=pdp_pb2.PolicyStore(
            Kind="ledger",
            ID="809257ed202e40cab7e958218eecad20"
        ),
        Principal=pdp_pb2.Principal(
            Type="user",
            ID="amy.smith@acmecorp.com",
            Source="keycloak"
        ),
        Entities=pdp_pb2.Entities(
            Schema="cedar",
            Items=[entities_item]
        )
    )

    eval_request1 = pdp_pb2.EvaluationRequest(
        RequestID="exz1",
        Resource=pdp_pb2.Resource(
            Type="MagicFarmacia::Platform::Subscription",
            ID="e3a786fd07e24bfa95ba4341d3695ae8",
            Properties=resource_properties
        ),
        Action=pdp_pb2.Action(
            Name="MagicFarmacia::Platform::Action::create",
            Properties=action_properties_enabled
        )
    )

    eval_request2 = pdp_pb2.EvaluationRequest(
        RequestID="exz2",
        Resource=pdp_pb2.Resource(
            Type="MagicFarmacia::Platform::Subscription",
            ID="e3a786fd07e24bfa95ba4341d3695ae8",
            Properties=resource_properties
        ),
        Action=pdp_pb2.Action(
            Name="MagicFarmacia::Platform::Action::create",
            Properties=action_properties_disabled
        )
    )

    request = pdp_pb2.AuthorizationCheckRequest(
        AuthorizationModel=auth_model,
        RequestID="abc1",
        Subject=pdp_pb2.Subject(
            Type="role-actor",
            ID="platform-creator",
            Source="keycloak",
            Properties=subject_properties
        ),
        Context=context_struct,
        Evaluations=[eval_request1, eval_request2]
    )

    try:
        response = stub.AuthorizationCheck(request)
        # print(f"Decision: {response.Decision}")
        # print(f"RequestID: {response.RequestID}")
        # for eval in response.Evaluations:
        #     print(f"Evaluation RequestID: {eval.RequestID}, Decision: {eval.Decision}")
        json_string = MessageToJson(response, indent=2)
        print(json_string)
    except grpc.RpcError as e:
        print(f"Error: {e.code()} - {e.details()}")
    finally:
        channel.close()

if __name__ == "__main__":
    run()