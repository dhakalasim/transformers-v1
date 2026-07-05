from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .registry import NoAutobotAvailable, OptimusPrime

app = FastAPI(title="Transformers-v1 API", description="Autobots, transform!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

prime = OptimusPrime()


class BotInfo(BaseModel):
    name: str
    conversions: list[list[str]]


class TransformRequest(BaseModel):
    content: str
    from_format: str
    to_format: str


class TransformResponse(BaseModel):
    bot_name: str
    result: str


@app.get("/api/bots", response_model=list[BotInfo])
def list_bots() -> list[BotInfo]:
    return [
        BotInfo(name=bot.name, conversions=sorted([list(pair) for pair in bot.conversions]))
        for bot in prime.bots
    ]


@app.post("/api/transform", response_model=TransformResponse)
def transform(request: TransformRequest) -> TransformResponse:
    try:
        bot = prime.find_bot(request.from_format, request.to_format)
    except NoAutobotAvailable as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    try:
        result = bot.transform(request.content, request.from_format, request.to_format)
    except (ValueError, LookupError, SyntaxError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TransformResponse(bot_name=bot.name, result=result)


_frontend_dist = Path(__file__).resolve().parent / "static"
if _frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")
