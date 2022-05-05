import json

import redis

from common.base.remote_procedure_call.error_protocol import RPCErrorsList
from common.base.remote_procedure_call.request_protocol import RPCRequest, RPCNotification
from common.base.remote_procedure_call.response_protocol import RPCResultResponse, RPCErrorResponse
from settings import Settings


class BaseHandler:
    __slots__ = ['connection', 'request_queue_uuid', 'method_handlers']

    settings = Settings()
    rpc_errors_list = RPCErrorsList()

    def __init__(self, request_queue_uuid: str) -> None:
        self.connection = redis.Redis(host=self.settings.REDIS_HOST, port=self.settings.REDIS_PORT,
                                      decode_responses=True)
        try:
            self.connection.delete(request_queue_uuid)
        except Exception as e:  # TODO: add and log specific exceptions
            print(e)

        self.request_queue_uuid: str = request_queue_uuid

        self.method_handlers: dict = {}

    def register_method_handlers(self, handlers: dict) -> None:
        self.method_handlers.update(handlers)

    async def receive_messages(self) -> None:
        while True:
            try:
                request_dict_obj: dict = json.loads(self.connection.brpop(keys=self.request_queue_uuid)[1])
            except Exception as e:  # TODO: add and log specific exceptions
                print(e)
                continue

            if await self.validate_request_dict_obj(request_dict_obj=request_dict_obj):
                request_obj = await self.request_json_obj_handler(request_dict_obj=request_dict_obj)
                method_handler = self.method_handlers.get(request_obj.method, None)
                if method_handler is not None:
                    await self.request_obj_handler(method_handler=method_handler, request_obj=request_obj)
                elif isinstance(request_obj, RPCRequest):
                    response = await self.create_error_obj(error_obj=self.rpc_errors_list.method_not_found(),
                                                           uuid=request_obj.uuid)
                    await self.send_response(response=response)

    @staticmethod
    async def request_json_obj_handler(request_dict_obj: dict) -> RPCRequest | RPCNotification:
        if isinstance(request_dict_obj.get('uuid', None), str):
            request_obj = RPCRequest(**request_dict_obj)
        else:
            request_obj = RPCNotification(**request_dict_obj)
        return request_obj

    async def request_obj_handler(self, method_handler, request_obj: RPCRequest | RPCNotification) -> None:
        result_obj = await method_handler(params=request_obj.params)
        if isinstance(request_obj, RPCRequest):
            if await self.validate_error_obj(error_obj=result_obj):
                response = await self.create_error_obj(error_obj=result_obj, uuid=request_obj.uuid)
            else:
                response = await self.create_response_obj(result_obj=result_obj, uuid=request_obj.uuid)
            await self.send_response(response=response)

    async def validate_request_dict_obj(self, request_dict_obj: dict) -> bool:
        if isinstance(request_dict_obj, dict):
            jsonrpc: str = request_dict_obj.get('jsonrpc', None)
            method: str = request_dict_obj.get('method', None)
            params: dict | list = request_dict_obj.get('params', None)
            if jsonrpc == self.settings.JSON_RPC and isinstance(method, str) and isinstance(params, (dict, list)):
                return True
        return False

    @staticmethod
    async def validate_error_obj(error_obj: dict) -> bool:
        if isinstance(error_obj, dict):
            code: int = error_obj.get('code', None)
            message: str = error_obj.get('message', None)
            data: str = error_obj.get('data', None)
            if isinstance(code, int) and isinstance(message, str) and isinstance(data, str):
                return True
        return False

    @staticmethod
    def create_result_obj(result: bool) -> dict:
        return {'detail': result}

    @staticmethod
    async def create_response_obj(result_obj, uuid: str) -> RPCResultResponse:
        response_obj = RPCResultResponse(result=result_obj, uuid=uuid)
        return response_obj

    @staticmethod
    async def create_error_obj(error_obj: dict, uuid: str) -> RPCErrorResponse:
        error_obj = RPCErrorResponse(error=error_obj, uuid=uuid)
        return error_obj

    async def send_response(self, response: RPCResultResponse | RPCErrorResponse) -> None:
        self.connection.rpush(response.uuid, response.json())
        self.connection.expire(name=response.uuid, time=5)
