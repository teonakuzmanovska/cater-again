import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import (
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)

from app.settings import (
    KEYCLOAK_CLIENT_ID,
    KEYCLOAK_ISSUER,
    KEYCLOAK_JWKS_URL,
)


bearer_scheme = HTTPBearer()
jwks_client = jwt.PyJWKClient(KEYCLOAK_JWKS_URL, timeout=5)


def get_company_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    token = credentials.credentials

    try:
        public_key = jwks_client.get_signing_key_from_jwt(token).key
        claims = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            audience=KEYCLOAK_CLIENT_ID,
            options={"require": ["exp"]},
        )
    except PyJWKClientConnectionError as exc:
        raise HTTPException(503, "Keycloak signing keys are unavailable") from exc
    except (InvalidTokenError, PyJWKClientError) as exc:
        raise HTTPException(
            401,
            "Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    company_id = claims.get("company_id")
    if (
        not isinstance(company_id, str)
        or not company_id.strip()
        or len(company_id) > 64
    ):
        raise HTTPException(403, "Valid company ID required")

    return company_id