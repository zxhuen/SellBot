# Backend Improvements & Fixes

### 1. Fix the “Mark as Sold” Flow

DONE

### 2. Make Product List Responses Consistent

* Normalize the product-list response so both cache-hit and cache-miss paths return the **same response structure**.
* Cache hits currently return decoded JSON, while cache misses return ORM objects.
* Add tests covering:

  * Cache hit
  * Cache miss
  * Empty product list

### 3. Handle Redis Failures After Database Commits

* Product creation, deletion, and mark-as-sold operations currently commit to the database before deleting the Redis cache.
* If Redis fails after the database commit, the API may report a failure even though the database operation succeeded.
* This can cause clients to retry an operation that already succeeded.
* Decide on a cache strategy, such as **best-effort cache invalidation**, where Redis failures do not cause an otherwise successful database operation to fail.

### 4. Validate Product Input at the API Boundary

* Add Pydantic validation to `product_schema.py`.
* Validate:

  * Title length against the database's 255-character limit.
  * Description length.
  * Price range.
  * Price precision to two decimal places.
* Invalid input should return a useful **422 validation error** instead of reaching the database and producing a database error.

### 5. Define AI Failure Behavior During Product Creation

* Product creation currently depends on `revise_description`, an external AI call.
* Decide what should happen if the AI service fails:

  * **Block creation**, or
  * **Fall back to the original description**.
* Add an appropriate timeout and error handling around `revise_description`.
* Keep this failure policy within the product service layer.

### 6. Add Pagination to Product Lists

* `list_product_repo` currently loads every product belonging to a user.
* Add pagination before the number of products becomes large enough to make full-list queries expensive.
* Use either:

  * Limit/offset pagination, or
  * Cursor-based pagination.
* Add a stable sort order so pagination produces predictable results.

### 7. Clean Up the Product Service

After the behavioral changes and tests are complete:

* Remove duplicate imports.
* Remove unused imports.
* Fix the `"mesage"` typo in response keys.
* Perform general cleanup without changing behavior unnecessarily.

## Suggested Order

1. **Mark as Sold flow**
2. **Consistent product-list responses**
3. **Redis failure handling**
4. **Input validation**
5. **AI failure handling**
6. **Pagination**
7. **Final cleanup**
