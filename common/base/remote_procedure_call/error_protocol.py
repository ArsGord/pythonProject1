import pathlib
from typing import List

from pydantic import BaseModel, conint, constr
from pydantic import parse_file_as


class RPCError(BaseModel):
    code: conint() = None
    message: constr(min_length=1) = None
    data: constr(min_length=1) = None


class RPCErrorsList:
    __slots__ = []

    errors_list = parse_file_as(List[RPCError], f'{pathlib.Path(__file__).parent.resolve()}/errors_list.json')

    def parse_error(self) -> dict:
        return self.errors_list[0].dict()

    def invalid_request(self) -> dict:
        return self.errors_list[1].dict()

    def method_not_found(self) -> dict:
        return self.errors_list[2].dict()

    def invalid_params(self) -> dict:
        return self.errors_list[3].dict()

    def internal_error(self) -> dict:
        return self.errors_list[4].dict()

    def server_error(self) -> dict:
        return self.errors_list[5].dict()

    def timeout_error(self) -> dict:
        return self.errors_list[6].dict()
