from pydantic import BaseModel

class ConfigUpdate(BaseModel):
    client_url: str
    client_port: int