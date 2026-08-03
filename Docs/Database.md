# Database Design

## Overview

The database is designed around a simple SaaS architecture where sellers create AI-powered product assistants that customers can interact with through a public URL.

The schema separates users, subscriptions, products, and conversations to keep responsibilities clear and allow future expansion.

---

# Entity Relationship

```text
Subscription
      │
      │ 1
      │
      ▼
User
      │
      │ 1
      │
      ▼
Product
      │
      │ 1
      │
      ▼
ChatSession
      │
      │ 1
      │
      ▼
Message
```

---

# Tables

## User

Represents a registered seller.

Each user owns one subscription plan and can create multiple AI product assistants.

| Column | Description |
|---------|-------------|
| id | Internal UUID primary key |
| email | User email address |
| display_name | Display name shown inside the application |
| avatar_url | Profile picture URL |
| subscription_id | Current subscription plan |
| created_at | Account creation timestamp |
| updated_at | Last update timestamp |

### Relationships

- Belongs to one Subscription
- Owns many Products

---

## Subscription

Defines the pricing plans and application limits.

This table allows subscription plans to be managed without changing application logic.

| Column | Description |
|---------|-------------|
| id | Primary key |
| name | Subscription name |
| price | Monthly subscription price |
| max_products | Maximum products a user can own |
| daily_product_limit | Maximum products that can be created per day |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

### Relationships

- Has many Users

---

## Product

Represents an AI-powered product listing.

Instead of customers contacting the seller directly, they interact with the AI assistant associated with this product.

| Column | Description |
|---------|-------------|
| id | Internal UUID primary key |
| owner_id | Owner of the product |
| title | Product title |
| description | Product information used as LLM context |
| price | Product price |
| public_id | Public identifier used in shareable URLs |
| status | Current product status |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

### Relationships

- Belongs to one User
- Has many Chat Sessions

---

## ChatSession

Represents one customer conversation.

Each visitor receives a separate chat session to preserve conversation history independently from other customers.

| Column | Description |
|---------|-------------|
| id | Internal UUID primary key |
| product_id | Associated product |
| session_token | Anonymous customer identifier |
| created_at | Session creation time |
| last_message_at | Timestamp of latest activity |

### Relationships

- Belongs to one Product
- Has many Messages

---

## Message

Stores every message exchanged between the customer and the AI.

Conversation history is persisted to provide context for future LLM requests.

| Column | Description |
|---------|-------------|
| id | Internal UUID primary key |
| chat_session_id | Associated chat session |
| role | Sender role (`user` or `assistant`) |
| content | Message content |
| created_at | Message timestamp |

### Relationships

- Belongs to one Chat Session

---

# Design Decisions

## UUID Primary Keys

All entities use UUIDs as internal identifiers.

Benefits:

- Difficult to guess
- Suitable for distributed systems
- Stable identifiers
- Independent of insertion order

---

## Public IDs

Products expose a separate `public_id` instead of their internal UUID.

Example:

```
https://sellbot.com/chat/aB9xK2LmPq
```

Benefits:

- Cleaner URLs
- Safer to expose publicly
- Internal database structure remains hidden

---

## Anonymous Customers

Customers are not required to register.

Each visitor receives a unique chat session, allowing conversation history without requiring authentication.

---

## Conversation History

Every user and assistant message is stored.

This allows the application to:

- Maintain conversation context
- Resume conversations
- Improve customer experience
- Analyze future chat metrics

---

## Lightweight AI Context

Unlike document-based RAG systems, each product stores its information in a single description field.

The backend injects this description directly into the system prompt before sending requests to the LLM.

This architecture keeps the application lightweight while providing sufficient context for product-related conversations.

---
