from typing import Annotated

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.connection_managers import ConnectionManager
from app.services.utils_websocket import get_cookie_or_token
from app.tasks.task_websocket_v1 import chat_websocket

router = APIRouter(prefix="/api/v10/web_socket", tags=["WebSockets V10"])

templates = Jinja2Templates(directory="src/app/template")

manager = ConnectionManager()


@router.get("/", response_class=HTMLResponse)
async def get_main_v1(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await chat_websocket(websocket, item_id, cookie_or_token, q)


@router.get("/chat", response_class=HTMLResponse)
async def get_main_v2(request: Request):
    return templates.TemplateResponse("chatv2.html", {"request": request})


@router.websocket("/ws/{client_id}")
async def websocket_endpoint_v2(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
