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

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class PolicyStore(BaseModel):
    kind: Optional[str] = None
    id: Optional[str] = None


class Entities(BaseModel):
    schema_name: Optional[str] = Field(alias="schema")  
    items: List[Dict[str, Any]] = []


class Principal(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    source: Optional[str] = None


class Subject(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    source: Optional[str] = None
    properties: Dict[str, Any] = {}


class Resource(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    properties: Dict[str, Any] = {}


class Action(BaseModel):
    name: Optional[str] = None
    properties: Dict[str, Any] = {}


class Evaluation(BaseModel):
    request_id: Optional[str] = None
    subject: Optional[Subject] = None
    resource: Optional[Resource] = None
    action: Optional[Action] = None
    context: Dict[str, Any] = {}


class AZModel(BaseModel):
    zone_id: int
    principal: Optional[Principal] = None
    policy_store: Optional[PolicyStore] = None
    entities: Optional[Entities] = None


class AZRequest(BaseModel):
    authorization_model: Optional[AZModel] = None
    request_id: Optional[str] = None
    subject: Optional[Subject] = None
    resource: Optional[Resource] = None
    action: Optional[Action] = None
    context: Dict[str, Any] = {}
    evaluations: List[Evaluation] = []


class ReasonResponse(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None


class ContextResponse(BaseModel):
    id: Optional[str] = None
    reason_admin: Optional[ReasonResponse] = None
    reason_user: Optional[ReasonResponse] = None


class EvaluationResponse(BaseModel):
    request_id: str
    decision: Optional[bool] = None
    context: Optional[ContextResponse] = None


class AZResponse(BaseModel):
    request_id: Optional[str] = None
    decision: bool
    context: Optional[ContextResponse] = None
    evaluations: List[EvaluationResponse] = []
