from typing import Annotated

from fastapi import APIRouter, Depends

from models import ConfigUpdate
from config import ConfigManager

# THIS SHOULDN'T BE HERE!
config_path = "../../config.ini"

router = APIRouter()

@router.post("/update_config/")
def update_config(new_config: ConfigUpdate):
    config_manager = ConfigManager(config_path)
    config_manager.write_config(new_config)
    return {"message": "Config updated successfully"}