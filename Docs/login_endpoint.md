# Add Person

Creates a new user in the application's database if they do not already exist. The endpoint authenticates the request using a Supabase access token and returns the user record.

## Endpoint

```http
POST /add-person
```

## Authentication

Requires a valid **Supabase Bearer Access Token**.

### Header

```http
Authorization: Bearer <supabase_access_token>
```

---

## Request

No request body is required.

---

## Behavior

1. Validates the provided Supabase access token.
2. Retrieves the authenticated user from Supabase.
3. Checks whether the user already exists in the local database.
4. If the user does not exist:
   - Creates a new user record.
   - Initializes a `UserUsage` record.
   - Assigns the default `subscription_id` of `1`.
5. Returns the user object.

---

## Response

### Success (200 OK)

```json
{
  "id": "9c1d8d86-4d58-4b40-8f08-2c98a6d9e4ab",
  "email": "john@example.com",
  "display_name": "John Doe",
  "avatar_url": "https://example.com/avatar.png",
  "subscription_id": 1
}
```

---

## Errors

### 404 Not Found

Returned when the provided access token is invalid or the authenticated user cannot be retrieved.

```json
{
  "detail": "Invalid token."
}
```

### 401 Unauthorized

Returned if the bearer token is missing or invalid (handled by the OAuth dependency).

Example:

```json
{
  "detail": "Not authenticated"
}
```

### 500 Internal Server Error

Returned when an unexpected server error occurs while creating or retrieving the user.

---

## User Creation

When a user signs in for the first time, the following records are created.

### User

| Field | Source |
|--------|--------|
| `id` | Supabase User ID |
| `email` | Supabase email |
| `display_name` | `user_metadata.full_name` |
| `avatar_url` | `user_metadata.avatar_url` |
| `subscription_id` | Default value: `1` |

### UserUsage

| Field | Initial Value |
|--------|---------------|
| `user_id` | Created user's ID |
| `products_created_today` | `0` |

---

## Example

### Request

```bash
curl -X POST https://api.example.com/add-person \
  -H "Authorization: Bearer eyJhbGciOi..."
```

### Response

```json
{
  "id": "9c1d8d86-4d58-4b40-8f08-2c98a6d9e4ab",
  "email": "john@example.com",
  "display_name": "John Doe",
  "avatar_url": "https://example.com/avatar.png",
  "subscription_id": 1
}
```

---

## Notes

- This endpoint is **idempotent**.
- Calling the endpoint multiple times with the same authenticated user will **not** create duplicate user records.
- User information is synchronized from the authenticated Supabase account only during the initial user creation.