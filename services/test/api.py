import sys
from typing import Any

from common.base.base_api import BaseApi
from common.base.remote_procedure_call.request_protocol import RPCRequest
from common.base.remote_procedure_call.response_protocol import RPCResultResponse, RPCErrorResponse
from settings import Settings


class TestApi(BaseApi):
    __slots__ = []

    settings = Settings()

    def __init__(self):
        super(TestApi, self).__init__(request_queue_uuid=self.settings.TEST_REQUEST_QUEUE)

    def ping(self, request: str) -> bool | RPCErrorResponse | None | Any:
        request_obj = RPCRequest(method=sys._getframe().f_code.co_name,
                                 params={'request': request})
        response_obj = self.send_message(request_obj=request_obj)

        if isinstance(response_obj, RPCResultResponse):
            result_obj = response_obj.result
            return result_obj
        return response_obj

    def test(self, n: int) -> list | RPCErrorResponse | None | Any:
        request_obj = RPCRequest(method=sys._getframe().f_code.co_name,
                                 params={'n': n})
        response_obj = self.send_message(request_obj=request_obj)

        if isinstance(response_obj, RPCResultResponse):
            result_obj = response_obj.result
            return result_obj
        return response_obj
