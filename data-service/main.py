from fastapi import FastAPI
import uvicorn

import backend

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                log_level="info")
