# Products API

Endpoints for creating and retrieving products owned by the authenticated user.

## Base URL

```text
/Products
```

## Authentication

All endpoints require a valid **Supabase Bearer Access Token**.

### Header

```http
Authorization: Bearer <supabase_access_token>
```

---

# Create Product

Creates a new product for the authenticated user. Before saving, the product description is enhanced using AI.

## Endpoint

```http
POST /Products/add-product
```

## Rate Limit

- **4 requests per minute** per client.

---

## Request Body

```json
{
  "title": "Wireless Mouse",
  "description": "Wireless mouse with ergonomic design.",
  "price": 29.99
}
```

### Fields

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `title` | string | Yes | Product title. |
| `description` | string | Yes | Initial product description. This will be improved using AI before being stored. |
| `price` | number | Yes | Product price. |

---

## Processing Flow

1. Authenticates the user.
2. Validates the user's product creation usage/quota.
3. Sends the provided description to the AI service.
4. Receives an enhanced product description.
5. Creates a new product with:
   - Generated UUID
   - Authenticated user as the owner
   - AI-enhanced description
   - Random 12-character `public_id`
6. Increments the user's daily product creation count.
7. Saves the product to the database.
8. Returns the created product.

---

## Success Response

**200 OK**

```json
{
  "id": "b63b4a3f-6c2e-4fa1-a95e-31f52ef6d7c4",
  "owner_id": "9c1d8d86-4d58-4b40-8f08-2c98a6d9e4ab",
  "title": "Wireless Mouse",
  "description": "Experience smooth and precise navigation with this ergonomic wireless mouse, designed for comfort and long-lasting productivity.",
  "price": 29.99,
  "public_id": "f3ab91d27c81"
}
```

---

## Possible Errors

### 401 Unauthorized

Returned when the user is not authenticated.

```json
{
  "detail": "Not authenticated"
}
```

---

### 429 Too Many Requests

Returned when the rate limit has been exceeded.

```json
{
  "detail": "Rate limit exceeded."
}
```

---

### 500 Internal Server Error

Returned if the product could not be saved.

```json
{
  "detail": "Failed to create product."
}
```

---

# List Products

Returns all products belonging to the authenticated user.

## Endpoint

```http
GET /Products/list-product
```

---

## Request

No request body is required.

---

## Success Response

**200 OK**

```json
[
  {
    "id": "b63b4a3f-6c2e-4fa1-a95e-31f52ef6d7c4",
    "owner_id": "9c1d8d86-4d58-4b40-8f08-2c98a6d9e4ab",
    "title": "Wireless Mouse",
    "description": "Experience smooth and precise navigation with this ergonomic wireless mouse.",
    "price": 29.99,
    "public_id": "f3ab91d27c81"
  },
  {
    "id": "9d4fd83c-4d1e-40fc-8ea8-f5d1123efae1",
    "owner_id": "9c1d8d86-4d58-4b40-8f08-2c98a6d9e4ab",
    "title": "Mechanical Keyboard",
    "description": "Premium mechanical keyboard with RGB lighting.",
    "price": 89.99,
    "public_id": "2ef61cb84a11"
  }
]
```

---

## Possible Errors

### 401 Unauthorized

Returned when authentication fails or no products are found.

```json
{
  "detail": "No products found."
}
```

> **Note:** In the current implementation, the service raises a `401` when no products are found. A `404 Not Found` would generally be a more conventional status code for this scenario.

---

## Notes

- Every created product is automatically associated with the authenticated user.
- Product descriptions are enhanced using an AI model before being stored.
- Each product receives a unique 12-character `public_id`.
- The user's daily product creation counter is incremented after a successful product creation.
- Product creation is limited to **4 requests per minute** by the API rate limiter.

---

# Delete Product

Deletes a product owned by the authenticated user.

## Endpoint

```http
DELETE /Products/delete-product?id=<product_uuid>
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | UUID | Yes | The UUID of the product to delete. Must belong to the authenticated user. |

## Success Response

**200 OK**

```json
{
  "message": "Product deleted successfully"
}
```

## Possible Errors

### 401 Unauthorized

Returned when the request is not authenticated.

```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found

Returned when the requested product does not exist or is not owned by the authenticated user.

```json
{
  "detail": "no products found"
}
```

---

# Get Product by Public ID

Returns public product details using the product's `public_id`. This endpoint does not require authentication.

## Endpoint

```http
GET /Products/get-product-public-id?public_id=<public_id>
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `public_id` | string | Yes | The public identifier for the product. |

## Success Response

**200 OK**

```json
{
  "title": "Wireless Mouse",
  "description": "Experience smooth and precise navigation with this ergonomic wireless mouse.",
  "price": 29.99
}
```

## Possible Errors

### 404 Not Found

Returned when no product exists with the provided `public_id`.

```json
{
  "detail": "no products found"
}
```

---

# Mark Product as Sold

Marks a product owned by the authenticated user as sold.

## Endpoint

```http
GET /Products/mark-as-sold?id=<product_uuid>
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | UUID | Yes | The UUID of the product to mark as sold. Must belong to the authenticated user. |

## Success Response

**200 OK**

```json
{
  "mesage": "product is already set as sold"
}
```

> Note: The current implementation returns the same success payload even when the product is updated to sold. There is a typo in the key (`mesage`).

## Possible Errors

### 401 Unauthorized

Returned when the request is not authenticated.

```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found

Returned when the product does not exist, is not owned by the authenticated user, or is already sold.

```json
{
  "detail": "Product not found"
}
```

```json
{
  "detail": "Product is already sold"
}
```
```