from fastapi.security import HTTPBearer

oauth2_scheme = HTTPBearer(auto_error=False)