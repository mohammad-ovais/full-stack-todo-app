# JWT Token Handler Skill

This skill handles JWT token operations in both Next.js and FastAPI applications. It knows how to configure Better Auth JWT plugin, attach tokens to API requests using Authorization headers, verify token signatures in FastAPI middleware using python-jose library, extract user_id and email from decoded tokens, and handle token expiry errors gracefully.

## Usage Context

Use this skill whenever implementing authentication flow, API client functions, or protected endpoints. Always validate tokens before database queries and return 401 if token is invalid or expired.

## Capabilities

### Next.js Frontend Operations
- Configure Better Auth JWT plugin for Next.js applications
- Attach JWT tokens to API requests using Authorization headers
- Handle token storage in cookies or localStorage
- Manage token refresh mechanisms
- Handle token expiry and re-authentication flows

### FastAPI Backend Operations
- Verify token signatures in FastAPI middleware using python-jose library
- Extract user_id and email from decoded tokens
- Validate token expiration times
- Return appropriate 401 responses for invalid/expired tokens
- Integrate with database queries to enforce user permissions

## Implementation Patterns

### Better Auth Configuration (Next.js)
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
      expiresIn: "1h"
    })
  ]
});
```

### API Request with Authorization Header (Next.js)
```typescript
const response = await fetch('/api/protected-endpoint', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json'
  }
});
```

### FastAPI Middleware for Token Verification
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Dict, Optional

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE
        )
        # Validate expiration
        if datetime.fromtimestamp(payload.get("exp")) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@app.get("/protected-endpoint")
async def protected_route(user_data: dict = Depends(verify_token)):
    user_id = user_data.get("user_id")
    email = user_data.get("email")
    # Process request with validated user data
```

## Best Practices

1. **Always validate tokens before database queries**
   - Verify JWT signature
   - Check expiration time
   - Confirm user permissions

2. **Return 401 for invalid/expired tokens**
   - Use consistent error messages
   - Log authentication failures for monitoring

3. **Secure token storage**
   - Use httpOnly cookies when possible
   - Set appropriate SameSite attributes
   - Implement CSRF protection

4. **Handle token expiry gracefully**
   - Implement automatic refresh when possible
   - Redirect to login when refresh fails
   - Preserve user state during re-authentication

## Error Handling

- Invalid token signature → 401 Unauthorized
- Expired token → 401 Unauthorized
- Missing token → 401 Unauthorized
- Malformed token → 401 Unauthorized
- Insufficient permissions → 403 Forbidden

## Integration Points

This skill integrates with:
- Better Auth for JWT generation and management
- Next.js App Router for frontend authentication
- FastAPI for backend token validation
- PostgreSQL databases for user permission enforcement
- python-jose library for secure token operations