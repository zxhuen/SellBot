# Chat Endpoint

This document describes the chat API in the SellBot application, centered on the routes defined in [app/api/chatbot.py](../app/api/chatbot.py).

## Overview

The chat router is mounted under the `/Chat` prefix and exposes these endpoints:

- `POST /Chat/Luna` - sends a user message to the Luna chat flow and returns the assistant response.
- `GET /Chat/Load-Chat` - loads or initializes a chat session for a given product/public identifier.

## Shared behavior

Both routes are protected by the application rate limiter:

- `POST /Chat/Luna` is limited to `10/minute`
- `GET /Chat/Load-Chat` is limited to `5/minute`

They also rely on the same core dependencies:

- `public_id` as a required query parameter
- `visitor_token` as an optional cookie value
- a database session injected through the app database dependency

## `POST /Chat/Luna`

### Purpose

This endpoint accepts a user message, finds or creates the related chat session, stores the message, generates a response through the chat generation service, and returns the assistant reply.

### Request

#### Body

The request body must match the `ChatCreate` schema:

```json
{
  "message": "Hello Luna"
}
```

#### Query parameters

- `public_id` (required): the public identifier of the product associated with the chat session.

#### Cookies

- `visitor_token` (optional): used to locate the existing chat session. If it is missing, the server creates a new visitor cookie automatically.

### Response

The endpoint returns the generated assistant response as a plain string.

### Backend flow

When the request arrives, the service:

1. looks up the chat session using the visitor token and `public_id`
2. validates that a session exists
3. stores the user message
4. builds a memory-aware prompt
5. calls the LLM chat generation service
6. stores the assistant reply and returns it

### Example

```http
POST /Chat/Luna?public_id=product-123
Content-Type: application/json
Cookie: visitor_token=abc123

{
  "message": "What is this product about?"
}
```

## `GET /Chat/Load-Chat`

### Purpose

This endpoint loads an existing chat session or creates a new one if none exists for the supplied public identifier.

### Request

#### Query parameters

- `public_id` (required): the public identifier for the product chat session.

#### Cookies

- `visitor_token` (optional): reused if the user already has a session. If missing, the server creates one and stores it in the response cookie.

### Response

The endpoint returns the loaded chat history/messages for the session.

### Backend flow

When the request arrives, the service:

1. creates or reuses a visitor cookie if needed
2. resolves the chat session for the provided `public_id`
3. creates a new session when none exists
4. inserts an initial assistant welcome message for new sessions
5. returns the chat history

### Example

```http
GET /Chat/Load-Chat?public_id=product-123
Cookie: visitor_token=abc123
```

## Notes

- The chat routes are implemented through the service layer in [app/services/chat_service/chat_services.py](../app/services/chat_service/chat_services.py).
- The request payload schema is defined in [app/schemas/chat_schema.py](../app/schemas/chat_schema.py).
- The initial assistant greeting is created automatically for brand-new sessions.
- If a chat session cannot be found for `POST /Chat/Luna`, the endpoint raises a `404` error with the message `No chat session found`.
