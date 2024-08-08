
import yaml
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/test")
async def root():
    return {"message": "test World"}

@app.get("/")
async def root():
    try:
        stream = open("../config.yaml")
        data = yaml.safe_load(stream)
    except yaml.YAMLError as error:
        raise HTTPException(status_code=404, detail=error)
    except IOError:
        raise HTTPException(status_code=404, detail="Cannot load config.yaml")
    stream.close()

    return {"message": data["chatbot"]["temperature"]}