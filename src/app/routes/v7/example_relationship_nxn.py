from fastapi import APIRouter, status

from app.models.event import Event
from app.routes.deps import SessionDep
from app.schemas.v6.event import EventCreate, EventScheme, EventWithEmojiScheme
from app.services.event_service import create_event_service, read_event_service

router = APIRouter(prefix="/api/v7/relationships", tags=["Event_Emoji V7"])


@router.post("/event/", response_model=EventScheme, status_code=status.HTTP_201_CREATED)
async def create_new_event(event: EventCreate, session: SessionDep):
    db_event = create_event_service(model_type=Event, event_data=event, session=session)
    return db_event


@router.get(
    "/event/{event_id}",
    response_model=EventWithEmojiScheme,
    status_code=status.HTTP_200_OK,
)
async def read_team(
    event_id: int,
    session: SessionDep,
):
    return read_event_service(model_type=Event, session=session, event_id=event_id)
