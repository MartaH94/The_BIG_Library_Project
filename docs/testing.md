# Testing

## Testing Strategy

Testing is a core part of The BIG Library project.

The goal of testing is to verify that business requirements are implemented correctly, application behaviour remains predictable, and future changes do not introduce regressions.

The testing approach combines development and quality assurance practices to promote reliability, maintainability, and confidence in the solution.

---

## Testing Objectives

The project aims to verify:

- Functional correctness
- Business rule validation
- Data integrity
- Input validation
- Error handling
- Edge case behaviour
- Regression prevention

---

## Testing Scope

The following areas are covered by testing activities:

### Book Management

- Add a book
- Update book details
- Remove a book
- Search for books
- Validate duplicate records

### User Management

- Create a user
- Update user information
- Remove a user
- Validate user data

### Loan Management

- Borrow a book
- Return a book
- Prevent borrowing unavailable books
- Validate loan status changes

---

## Test Levels

### Unit Testing

Unit tests validate individual components independently from the rest of the application.

Examples:

- Book creation
- User creation
- Loan creation
- Validation logic
- Service methods

Benefits:

- Early defect detection
- Faster troubleshooting
- Improved code quality

---

### Integration Testing

Integration testing validates interactions between multiple components.

Examples:

- Services communicating with the database layer
- Data persistence operations
- Loan processing workflows
- Data retrieval and updates

Benefits:

- Verifies component collaboration
- Detects interface issues
- Confirms data consistency

---

## Example Test Scenarios

### Add a New Book

**Given**

A valid book record

**When**

The user adds the book to the library

**Then**

The book should be successfully stored and visible in the catalogue

---

### Borrow a Book

**Given**

An available book exists in the library

**When**

A user borrows the book

**Then**

A loan record should be created and the book should no longer be available

---

### Return a Book

**Given**

An active loan exists

**When**

The user returns the book

**Then**

The loan should be closed and the book should become available again

---

### Search for a Book

**Given**

Books exist in the catalogue

**When**

The user searches using valid criteria

**Then**

Matching books should be returned

---

## Validation Testing

Validation testing ensures that incorrect inputs are handled properly.

Examples:

- Missing mandatory fields
- Empty values
- Duplicate records
- Invalid identifiers
- Unsupported operations

Expected behaviour:

- Validation errors should be displayed clearly
- Invalid data should not be stored

---

## Edge Cases

Special attention is given to boundary and exceptional scenarios.

Examples:

- Empty library catalogue
- Empty user database
- Duplicate books
- Duplicate users
- Borrowing already borrowed books
- Returning books that are not currently borrowed
- Deleting non-existing records

---

## Error Handling

The application should handle errors consistently and predictably.

Examples:

- Missing records
- Invalid user actions
- Data access failures
- Unexpected runtime errors

Expected behaviour:

- Meaningful error messages
- No application crashes
- Data integrity maintained

---

## Automated Testing

Automated tests are used to validate key business logic and reduce manual verification effort.

Benefits include:

- Faster feedback
- Regression protection
- Improved reliability
- Easier refactoring

Automated tests are executed during development whenever new functionality is introduced or existing functionality is modified.

---

## Quality Assurance Approach

The project applies quality-focused development practices:

- Requirements review
- Code review
- Test design
- Automated testing
- Defect investigation
- Continuous improvement

This approach reflects software testing practices used in professional projects and supports long-term maintainability.

---

## Future Improvements

Planned testing enhancements include:

- Increased test coverage
- Test reporting
- CI/CD integration
- Performance testing
- API testing after FastAPI implementation
- Automated quality gates

---

## Quality Focus

Testing is treated as an integral part of development rather than a separate activity.

The objective is to build a reliable, maintainable, and scalable application while continuously improving both development and testing practices.