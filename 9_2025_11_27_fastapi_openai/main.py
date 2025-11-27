from fastapi import FastAPI
from selector import ModelSelector, TaskType
from services import InferenceService
from pydantic import BaseModel

app = FastAPI()

selector = ModelSelector()
service = InferenceService(selector)

class RequestBody(BaseModel):
    task: TaskType
    prompt: str

@app.post("/inference")
async def inference(req: RequestBody):
    return await service.run(req.task, req.prompt)
