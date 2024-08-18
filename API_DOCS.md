
### `API_DOCS.md`

```markdown
Category Service API Documentation

Overview
API documentation for the Category Service, which manages categories and related user data.

Version: 1.0.0
API Specification: OpenAPI 3.1

Endpoints

Category Management Endpoints

Create New Category
- URL: /categories/
- Method: POST
- Summary: Create a new product category.
- Request Body:
  {
    "$ref": "#/components/schemas/CategoryCreate"
  }
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

List Categories
- URL: /categories/
- Method: GET
- Summary: Retrieve a list of all categories.
- Parameters:
  - skip (integer): Number of categories to skip (default: 0).
  - limit (integer): Maximum number of categories to return (default: 10).
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/CategoryResponse"
      }
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Read Category
- URL: /categories/categories/{category_id}
- Method: GET
- Summary: Retrieve details of a specific category by its ID, including subcategories.
- Parameters:
  - category_id (integer): The ID of the category.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryWithSubcategories"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Update Category
- URL: /categories/{category_id}
- Method: PUT
- Summary: Update the details of an existing category.
- Parameters:
  - category_id (integer): The ID of the category to update.
- Request Body:
  {
    "$ref": "#/components/schemas/CategoryUpdate"
  }
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Delete Existing Category
- URL: /categories/{category_id}
- Method: DELETE
- Summary: Remove a category from the system by its ID.
- Parameters:
  - category_id (integer): The ID of the category to delete.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Category
- URL: /categories/{category_id}
- Method: GET
- Summary: Retrieve details of a specific category by its ID.
- Parameters:
  - category_id (integer): The ID of the category.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Category With Subcategories
- URL: /categories/{category_id}/subcategories
- Method: GET
- Summary: Retrieve a category along with its subcategories.
- Parameters:
  - category_id (integer): The ID of the category.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Move Category
- URL: /categories/{category_id}/move
- Method: PUT
- Summary: Move a category to a new parent category.
- Parameters:
  - category_id (integer): The ID of the category to move.
- Request Body:
  {
    "$ref": "#/components/schemas/MoveCategoryRequest"
  }
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Category Tree
- URL: /categories/tree/{category_id}
- Method: GET
- Summary: Retrieve the hierarchical structure of a category tree.
- Parameters:
  - category_id (integer): The ID of the category.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Get Category By Slug
- URL: /categories/slug/{slug}
- Method: GET
- Summary: Retrieve a category by its slug.
- Parameters:
  - slug (string): The slug of the category.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategoryResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Suggest Category
- URL: /categories/suggest/
- Method: POST
- Summary: Handle user suggestions for new categories.
- Request Body:
  {
    "$ref": "#/components/schemas/UserDataCreate"
  }
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/CategorySuggestionResponse"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Validate Category
- URL: /categories/validate/{id}
- Method: POST
- Summary: Validate a category based on user input.
- Parameters:
  - id (integer): The ID of the category to validate.
  - validation_status (boolean): The validation status.
- Response:
  - 200 Successful Response
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

User Data Management Endpoints

Create Dummy User Data
- URL: /create_dummy_user_data/
- Method: POST
- Summary: Create dummy user data for testing purposes.
- Response:
  - 200 Successful Response
    {}
