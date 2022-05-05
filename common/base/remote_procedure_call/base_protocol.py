from pydantic import Field, BaseModel, constr

from settings import Settings

settings = Settings()


class RPCBase(BaseModel):
    jsonrpc: constr(min_length=1, max_length=255) = Field(default=settings.JSON_RPC, const=True)
