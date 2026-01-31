# JWT Token Handler Skill

## Overview
This skill provides comprehensive handling of JWT token operations in both Next.js and FastAPI applications. It streamlines authentication flows by managing token configuration, validation, and error handling across the full stack.

## Features
- Better Auth JWT plugin configuration
- Secure token attachment to API requests
- FastAPI middleware for token verification
- User data extraction from tokens
- Graceful error handling for token expiry

## When to Use
- Implementing authentication flows
- Creating API client functions
- Building protected endpoints
- Validating tokens before database operations
- Securing application routes

## Requirements
- Better Auth configured in Next.js application
- python-jose library in FastAPI application
- Proper secret key management
- HTTPS in production environments

## Setup
1. Ensure BETTER_AUTH_SECRET is configured in both frontend and backend
2. Install required dependencies (better-auth, python-jose)
3. Configure the JWT token handler in your authentication workflow
4. Implement the middleware in your FastAPI application

## Security Considerations
- Always validate tokens before database queries
- Return 401 responses for invalid/expired tokens
- Use secure cookie settings for token storage
- Implement proper token refresh mechanisms
- Monitor authentication failures

## Common Patterns
- Use Authorization Bearer headers for API requests
- Extract user_id and email from decoded tokens
- Implement middleware for route protection
- Handle token expiry with refresh mechanisms
- Maintain consistent error responses

## Error Responses
- 401 Unauthorized for invalid/expired tokens
- Consistent error messaging
- Secure logging of authentication failures