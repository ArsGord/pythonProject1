import uuid

from pydantic import Field, constr

from common.base.remote_procedure_call.base_protocol import RPCBase


class RPCNotification(RPCBase):
    method: constr(min_length=1, max_length=255)
    params: dict | list = {}


class RPCRequest(RPCNotification):
    uuid: str = Field(default=str(uuid.uuid4()))
