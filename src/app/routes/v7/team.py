from fastapi import APIRouter, status

from app.models.team import Team
from app.routes.deps import SessionDep
from app.schemas.v6.team import TeamWithHeroesScheme
from app.services.team_service import read_team_service

router = APIRouter(prefix="/api/v7/database", tags=["Team V7"])


@router.get(
    "/team/{team_id}",
    response_model=TeamWithHeroesScheme,
    status_code=status.HTTP_200_OK,
)
async def read_team(
    team_id: int,
    session: SessionDep,
):
    team_data = read_team_service(model_type=Team, session=session, team_id=team_id)

    return team_data
