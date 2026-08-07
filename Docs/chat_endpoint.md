# Chat Endpoint

This document describes the `app/api/chatbot.py` chat API surface in the SellBot application.

## Overview

The chat endpoint exposes two routes under the `/Chat` prefix:

- `POST /Chat/Luna` - intended for sending chat messages to the Luna chat flow.
- `GET /Chat/Load-Chat` - loads or initializes a chat session for a public user ID.

Both endpoints use the FastAPI router declared in `app/api/chatbot.py` and share common request context objects such as `Request`, `Response`, and a database session dependency.

## `POST /Chat/Luna`

### Purpose

This route is intended to accept a chat message payload and route it through the Luna chat service.

### Rate limiting

- Limited to `10/minute` via the application-level limiter.

### Inputs

- `chat` (body): expected to conform to the `ChatCreate` schema from `app/schemas/chat_schema.py`.
- `session_token` (cookie, optional): a cookie value named `session_token` that can be used to maintain or associate the chat session.
- `db` (dependency): a SQLAlchemy database session injected by `app.core.database.get_db`.

### Behavior

In the current implementation, the endpoint is defined but its body is not yet implemented. It currently acts as a placeholder for the Luna chat request handler.

### Notes

- The route is mounted at `/Chat/Luna`.
- The route uses FastAPI request and response objects, but it does not currently return a value.

## `GET /Chat/Load-Chat`

### Purpose

This route loads or initializes an existing chat session for a public user identifier.

### Rate limiting

- Limited to `5/minute` via the application-level limiter.

### Inputs

- `public_id` (query parameter): the public identifier of the user or chat session to load.
- `session_token` (cookie, optional): a cookie value named `session_token` that is forwarded to session initialization.
- `db` (dependency): a SQLAlchemy database session injected by `app.core.database.get_db`.

### Behavior

This endpoint calls `initialize_chat_session(public_id, response, session_token, db)` from `app.services.chat_service.chat_services` and returns its result.

The session initialization function is responsible for:

- validating or restoring an existing chat session,
- associating the session with the provided `public_id`,
- setting any necessary cookies on the response,
- returning the chat session state to the caller.

## Implementation details

- `app/api/chatbot.py` registers an `APIRouter` at the prefix `/Chat` with the tag `Chat`.
- `initialize_chat_session` is the service function used by `/Chat/Load-Chat`.
- `ChatCreate` is the request schema currently expected by `/Chat/Luna`.
- `session_token` is accepted as an optional cookie value for session continuity.

## Current status

- `/Chat/Load-Chat` is implemented and returns the result of `initialize_chat_session`.
- `/Chat/Luna` exists as a route definition and has rate limiting applied, but its internal logic still needs to be implemented.

## Usage example

### Load chat session

Request:

```http
GET /Chat/Load-Chat?public_id=<public_id>
Cookie: session_token=<token>
```

Response:

- JSON payload returned by `initialize_chat_session`
- may include chat history, session metadata, or updated cookies

### Send chat message (placeholder)

Request:

```http
POST /Chat/Luna
Content-Type: application/json
Cookie: session_token=<token>

{
  "message": "Hello Luna",
  "metadata": {...}
}
```

Response:

- not yet implemented in the current handler
