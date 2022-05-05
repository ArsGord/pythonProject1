import json

import redis

from common.base.remote_procedure_call.error_protocol import RPCErrorsList
from common.base.remote_procedure_call.request_protocol import RPCRequest, RPCNotification
from common.base.remote_procedure_call.response_protocol import RPCResultResponse, RPCErrorResponse
from settings import Settings


class BaseApi:
    __slots__ = ['request_queue_uuid', 'connection']

    settings = Settings()
    rpc_errors_list = RPCErrorsList()

    def __init__(self, request_queue_uuid: str) -> None:
        self.request_queue_uuid = request_queue_uuid
        self.connection = redis.Redis(host=self.settings.REDIS_HOST, port=self.settings.REDIS_PORT,
                                      decode_responses=True)

    def send_message(self, request_obj: RPCRequest | RPCNotification,
                     timeout: int = 5) -> RPCResultResponse | RPCErrorResponse | None:
        if timeout <= 0:
            error = RPCErrorResponse(uuid=request_obj.uuid, error=self.rpc_errors_list.timeout_error())
            return error

        try:
            self.connection.lpush(self.request_queue_uuid, request_obj.json())
        except Exception as e:  # TODO: add and log specific exceptions
            print(e)
            error = RPCErrorResponse(uuid=request_obj.uuid, error=self.rpc_errors_list.server_error())
            return error

        if isinstance(request_obj, RPCRequest):
            try:
                response_dict_obj: dict = json.loads(self.connection.brpop(keys=request_obj.uuid, timeout=timeout)[1])
                self.connection.delete(request_obj.uuid)
            except Exception as e:  # TODO: add and log specific exceptions
                print(e)
                error = RPCErrorResponse(uuid=request_obj.uuid, error=self.rpc_errors_list.server_error())
                return error

            if self.validate_response_dict_obj(response_dict_obj=response_dict_obj):
                if response_dict_obj.get('result', None) is not None:
                    response = RPCResultResponse(**response_dict_obj)
                    return response
                elif response_dict_obj.get('error', None) is not None:
                    error = RPCErrorResponse(**response_dict_obj)
                    return error
            error = RPCErrorResponse(uuid=request_obj.uuid, error=self.rpc_errors_list.server_error())
            return error
        return None

    def validate_response_dict_obj(self, response_dict_obj: dict) -> bool:
        if isinstance(response_dict_obj, dict):
            jsonrpc: str = response_dict_obj.get('jsonrpc', None)
            uuid: str = response_dict_obj.get('uuid', None)
            if jsonrpc == self.settings.JSON_RPC and isinstance(uuid, str):
                return True
        return False
