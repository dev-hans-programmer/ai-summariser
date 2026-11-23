from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from openai import AsyncOpenAI
from pydantic import BaseModel

from summariser.core.config import get_settings
from summariser.services.summariser import summarise_ticket


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.openai = AsyncOpenAI(api_key=get_settings().openai_key)
    yield
    await app.state.openai.close()

app = FastAPI(title="AI Summariser", lifespan=lifespan)

def get_openai_client(request: Request):
    return request.app.state.openai


class SummariserCreate(BaseModel):
    input: str


@app.get('/')
async def root():
    return {"message":"Welcome to AI Summariser"}


@app.post('/summarise')
async def summarise(payload: SummariserCreate, client: Annotated[AsyncOpenAI, Depends(get_openai_client)]):
    summary = await summarise_ticket(payload.input, client=client)
    return {"summary":summary}


