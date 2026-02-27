from fastapi_plugin.fast_api_client import Auth0FastAPI

from app.core.config import settings

auth0 = Auth0FastAPI(domain=settings.AUTH0_DOMAIN, audience=settings.AUTH0_AUDIENCE)
