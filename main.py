import configparser
import os
import requests
import sys

from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, Response, Body

app = FastAPI()

sys.path.append("./models/")

from models import ProtobufFactory

# Initialize the ConfigParser
config = configparser.ConfigParser()
config_file_path = 'config.ini'

# Load the configuration from the config.ini file
if os.path.exists(config_file_path):
    config.read(config_file_path)
else:
    raise Exception("Configuration file not found!")

# Global variable to store the client URL and port
settings = {
    "client_url": config.get("Settings", "client_url"),
    "client_port": config.getint("Settings", "client_port")
}

class ConfigUpdate(BaseModel):
    client_url: str
    client_port: int

@app.post("/update_config/")
async def update_config(update: ConfigUpdate):
    global settings
    
    # Update the global settings
    settings["client_url"] = update.client_url
    settings["client_port"] = update.client_port
    
    # Update the config.ini file
    config["Settings"]["client_url"] = update.client_url
    config["Settings"]["client_port"] = str(update.client_port)

    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

    return {"message": "Configuration updated", "config": settings}

@app.post("/items/{item_id}")
async def send_model(item_id: int, request: Request):
    try:
        item_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    factory = ProtobufFactory(item_data.get("payload"))
    model = factory.load_config_from_json(item_id)

    try:
        serialized_model = model.SerializeToString()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to serialize model")

    try:
        response = requests.post(f"http://{item_data.get('destination_url')}/get_area?id={item_id}", data=serialized_model, headers={"Content-Type": "application/octet-stream"})
        print(serialized_model.decode('utf-8'))
        response.raise_for_status()  # Raise an error for bad responses
    except requests.HTTPError as http_error:
        raise HTTPException(status_code=response.status_code, detail=str(http_error))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to transmit model")

    return Response(content=serialized_model, media_type="application/octet-stream")

@app.post("/items/{item_id}")
async def send_model(item_id: int, request: Request):
    try:
        item_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    factory = ProtobufFactory(item_data.get("payload"))
    model = factory.load_config_from_json(item_id)

    try:
        serialized_model = model.SerializeToString()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to serialize model")

    try:
        response = requests.post(f"http://{item_data.get('destination_url')}/get_area?id={item_id}", data=serialized_model, headers={"Content-Type": "application/octet-stream"})
        print(serialized_model.decode('utf-8'))
        response.raise_for_status()  # Raise an error for bad responses
    except requests.HTTPError as http_error:
        raise HTTPException(status_code=response.status_code, detail=str(http_error))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to transmit model")

    return Response(content=serialized_model, media_type="application/octet-stream")
   
    
    
# # Update an item
# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: int, updated_item: Item):
#     for index, item in enumerate(items):
#         if item.id == item_id:
#             items[index] = updated_item
#             return updated_item
#     return {"error": "Item not found"}

# # Delete an item
# @app.delete("/items/{item_id}", response_model=Item)
# def delete_item(item_id: int):
#     for index, item in enumerate(items):
#         if item.id == item_id:
#             return items.pop(index)
#     return {"error": "Item not found"}
