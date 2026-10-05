# Backend Improvements & Fixes

### 1. Fix the “Mark as Sold” Flow

DONE

### 2. Make Product List Responses Consistent

DONE

### 3. Handle Redis Failures After Database Commits

DONE

### 4. Validate Product Input at the API Boundary

DONE

### 5. Define AI Failure Behavior During Product Creation

DONE

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
