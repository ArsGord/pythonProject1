from common.base.base_handler import BaseHandler
from services.test.model import Test
from settings import Settings


class TestHandler(BaseHandler):
    __slots__ = ['model']

    settings = Settings()

    async def handle_ping(self, params: dict) -> str:
        result_bool_obj: str = self.model.pong if params.get('request') == 'ping' else '****'
        return result_bool_obj

    async def handle_get_generate_list(self, params: dict) -> list:
        n: int = params.get('n', None)
        result_dict_obj: list = self.model.generate_list(n)
        return result_dict_obj

    def __init__(self) -> None:
        self.model = Test()

        super(TestHandler, self).__init__(request_queue_uuid=self.settings.TEST_REQUEST_QUEUE)
        self.method_handlers.update({
            'ping': self.handle_ping,
            'test': self.handle_get_generate_list,
        })
