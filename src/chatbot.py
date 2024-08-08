
import yaml
from fastapi import FastAPI, HTTPException, UploadFile, File

app = FastAPI()

@app.post("/upload/")
async def uploadFile(file: UploadFile = File(...), chunk=False):
    # @todo: incorporate chunk reading of file
    try:
        contents = file.file.read()
        stream = open(file.filename, "wb")
    except Exception as error:
        raise HTTPException(status_code=404, detail=error)
    finally:
        file.file.close()
        stream.close()
    return {"fileName": file.filename, "fileContent": contents}

@app.get("/")
async def root():
    try:
        stream = open("../config.yaml", "r")
        data = yaml.safe_load(stream)
    except yaml.YAMLError as error:
        raise HTTPException(status_code=404, detail=error)
    except IOError:
        raise HTTPException(status_code=404, detail="Cannot load config.yaml")
    finally:
        stream.close()

    return {"message": data["debug"]}