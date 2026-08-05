# Database Design

## Overview

SellBot follows a relational database design centered around a simple SaaS architecture where sellers create AI-powered product assistants that customers can access through a public URL.

The schema separates authentication, subscriptions, usage tracking, products, and conversations into independent entities. This separation of concerns keeps the application maintainable while allowing new features to be introduced without major schema changes.

---

# Entity Relationship

```text
Subscription
      │
      │ 1
      ▼
User
 ├──────────────┐
 │              │
 │1             │1
 ▼              ▼
UserUsage     Product
                 │
                 │1
                 ▼
           ChatSession
                 │
                 │1
                 ▼
              Message
```

---

# Tables

## User

Represents a registered seller within the platform.

Each user belongs to a subscription plan, owns products, and has an associated usage record used to enforce application limits.

| Column          | Description                 |
| --------------- | --------------------------- |
| id              | Internal UUID primary key   |
| email           | User email address          |
| display_name    | User display name           |
| avatar_url      | Profile picture URL         |
| subscription_id | Current subscription plan   |
| created_at      | Account creation timestamp  |
| updated_at      | Last modification timestamp |

### Relationships

* Belongs to one Subscription
* Owns one UserUsage
* Owns many Products

---

## Subscription

Defines the available pricing plans and platform limitations.

Application limits are data-driven, allowing subscription plans to be modified without changing business logic.

| Column              | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| id                  | Primary key                                                  |
| name                | Subscription name                                            |
| price               | Monthly subscription price                                   |
| max_products        | Maximum number of products a user can own                    |
| daily_product_limit | Maximum products that may be created within a 24-hour period |
| created_at          | Creation timestamp                                           |
| updated_at          | Last modification timestamp                                  |

### Relationships

* Has many Users

---

## UserUsage

Tracks usage information required to enforce subscription limits.

This table allows usage statistics to be reset independently while keeping user information separate from operational data.

| Column                 | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| id                     | Internal UUID primary key                                    |
| user_id                | Associated user                                              |
| products_created_today | Number of products created within the current 24-hour period |
| last_reset_at          | Timestamp of the last usage reset                            |
| created_at             | Creation timestamp                                           |
| updated_at             | Last modification timestamp                                  |

### Relationships

* Belongs to one User

---

## Product

Represents an AI-powered product assistant.

Each product contains the information required for the language model to answer customer questions.

| Column      | Description                              |
| ----------- | ---------------------------------------- |
| id          | Internal UUID primary key                |
| owner_id    | Product owner                            |
| title       | Product title                            |
| description | Product description used as LLM context  |
| price       | Product price                            |
| public_id   | Public identifier used in shareable URLs |
| status      | Current product status                   |
| created_at  | Creation timestamp                       |
| updated_at  | Last modification timestamp              |

### Relationships

* Belongs to one User
* Has many Chat Sessions

---

## ChatSession

Represents a single customer conversation.

Each visitor receives an independent conversation, allowing multiple customers to interact with the same product simultaneously without sharing message history.

| Column          | Description                          |
| --------------- | ------------------------------------ |
| id              | Internal UUID primary key            |
| product_id      | Associated product                   |
| session_token   | Anonymous customer identifier        |
| created_at      | Session creation timestamp           |
| last_message_at | Timestamp of the most recent message |

### Relationships

* Belongs to one Product
* Has many Messages

---

## Message

Stores every message exchanged between the customer and the AI assistant.

Persisting conversation history allows future requests to include previous messages as conversational context.

| Column          | Description                            |
| --------------- | -------------------------------------- |
| id              | Internal UUID primary key              |
| chat_session_id | Associated chat session                |
| role            | Message sender (`user` or `assistant`) |
| content         | Message content                        |
| created_at      | Message creation timestamp             |

### Relationships

* Belongs to one Chat Session

---

# Design Decisions

## UUID Primary Keys

All entities use UUIDs as internal identifiers.

### Benefits

* Difficult to enumerate or guess
* Suitable for distributed systems
* Stable across deployments
* Independent of insertion order

---

## Public Product IDs

Products expose a dedicated `public_id` instead of the internal UUID.

Example:

```text
https://sellbot.com/chat/aB9xK2LmPq
```

The backend resolves the public identifier to the corresponding internal product before processing requests.

### Benefits

* Clean, shareable URLs
* Internal database identifiers remain private
* Public identifiers can be regenerated independently if required

---

## Subscription-Based Usage Tracking

Daily usage limits are managed through the **UserUsage** table rather than storing counters directly on the User entity.

This separation keeps authentication data independent from frequently updated operational data.

The backend automatically:

* Resets daily usage after 24 hours
* Enforces daily product creation limits
* Enforces maximum product ownership based on the user's subscription

---

## Anonymous Customer Conversations

Customers are not required to register.

Each visitor receives a unique session token that identifies their conversation while keeping the platform authentication-free for buyers.

This design allows customers to continue conversations without exposing seller information.

---

## Persistent Conversation History

Every customer and AI message is stored.

Conversation history enables the application to:

* Maintain conversational context
* Resume previous conversations
* Support future analytics
* Improve customer experience

---

## Lightweight AI Context

Unlike Retrieval-Augmented Generation (RAG) systems that retrieve information from document embeddings, SellBot stores product knowledge directly within each product record.

Before every AI request, the backend injects the product description into the system prompt, allowing the language model to answer product-related questions without requiring vector search.

This approach keeps the architecture lightweight while remaining effective for structured product information.
