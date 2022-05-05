from typing import Any

from pydantic import constr

from common.base.remote_procedure_call.base_protocol import RPCBase


class RPCReceive(RPCBase):
    uuid: constr(min_length=1, max_length=255)


class RPCResultResponse(RPCReceive):
    result: Any = None


class RPCErrorResponse(RPCReceive):
    error: dict = None
