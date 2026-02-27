from fastapi import APIRouter, Depends

from app.core.auth import auth0

router = APIRouter(prefix="/api/v10/security_auth0_jwt", tags=["SECURITY V10"])


# Public route - no authentication required
@router.get("/public")
async def public():
    return {
        "message": "Hello from a public endpoint! You don't need to be authenticated to see this."
    }


# Protected route - requires authentication
@router.get("/private")
async def private(claims: dict = Depends(auth0.require_auth())):  # noqa: B008
    return {
        "message": "Hello from a private endpoint! You need to be authenticated to see this.",
        "user_id": claims.get("sub"),
    }


# Scoped route - requires specific permission
@router.get("/private-scoped")
async def private_scoped(
    claims: dict = Depends(auth0.require_auth(scopes="read:messages")),  # noqa: B008
):  # noqa: B008
    return {
        "message": "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.",
        "user_id": claims.get("sub"),
    }
