import requests

from fastapi import APIRouter, Request, HTTPException, Response, Query

from models import ProtobufFactory
from config import ConfigManager

router = APIRouter()

# THIS SHOULDN'T BE HERE!
config_path = "../../config.ini"

router = APIRouter()

@router.post("/memory_area/{item_id}")
async def write_memory_area(item_id: int, request: Request):
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
        response.raise_for_status() 
    except requests.HTTPError as http_error:
        raise HTTPException(status_code=response.status_code, detail=str(http_error))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to transmit model")

    return Response(content=serialized_model, media_type="application/octet-stream")

@router.get("/memory_area/{item_id}")
async def read_memory_area(item_id: int, url: str = Query(None), port: str = Query(None)):   
    serialized_data = None
    try:
        response = requests.get(f"http://{url}/get_area?id={item_id}", headers={"Content-Type": "application/octet-stream"})
        response.raise_for_status()  # Raise an error for bad responses
        serialized_data = response.text

    except requests.HTTPError as http_error:
        raise HTTPException(status_code=response.status_code, detail=str(http_error))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to transmit model")

    factory = ProtobufFactory()
    model = factory.load_config_from_json(item_id)
    model.ParseFromString(serialized_data.encode("utf-8"))
    
    print(model)

    # return Response(content=serialized_model, media_type="application/octet-stream")
   
    
    

    # factory = ProtobufFactory(item_data.get("payload"))
    # model = factory.load_config_from_json(item_id)

    # try:
    #     serialized_model = model.SerializeToString()
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Failed to serialize model")
