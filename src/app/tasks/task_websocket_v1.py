from fastapi import WebSocket


async def chat_websocket(
    websocket: WebSocket, item_id: str, cookie_or_token: str, q: int | None = None
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is_ {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
