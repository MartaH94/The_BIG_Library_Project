# Data Model

## Overview

The data model defines the core entities used by The BIG Library and describes how they interact with each other.

The model is designed to support library operations such as book management, user management, and loan processing while maintaining simplicity, readability, and scalability.

---

## Core Entities

The application is based on three primary entities:

- Book
- User
- Loan

These entities represent the core business objects of the system.

---

# Book

## Description

The Book entity represents a library item that can be searched, borrowed, and returned.

---

## Main Attributes

| Attribute | Description |
|------------|-------------|
| book_id | Unique identifier |
| title | Book title |
| author | Book author |
| category | Book category |
| publication_year | Year of publication |
| isbn | International Standard Book Number |
| availability_status | Indicates whether the book is available |

---

## Responsibilities

The Book entity is responsible for:

- Storing book information
- Providing book metadata
- Supporting search operations
- Supporting borrowing workflows

---

# User

## Description

The User entity represents a library member who can borrow books and manage borrowing activity.

---

## Main Attributes

| Attribute | Description |
|------------|-------------|
| user_id | Unique identifier |
| first_name | User first name |
| last_name | User last name |
| email | Contact email |
| registration_date | Date of registration |
| active_status | User account status |

---

## Responsibilities

The User entity is responsible for:

- Storing member information
- Supporting loan operations
- Tracking borrowing activity

---

# Loan

## Description

The Loan entity represents the borrowing transaction between a user and a book.

---

## Main Attributes

| Attribute | Description |
|------------|-------------|
| loan_id | Unique identifier |
| book_id | Borrowed book reference |
| user_id | Borrowing user reference |
| borrow_date | Date of borrowing |
| due_date | Expected return date |
| return_date | Actual return date |
| status | Active or completed |

---

## Responsibilities

The Loan entity is responsible for:

- Tracking active loans
- Tracking completed loans
- Supporting availability checks
- Maintaining borrowing history

---

# Entity Relationships

## Conceptual Relationship Model

```text
User
 │
 │ 1
 │
 ▼
Loan
 ▲
 │
 │ N
 │
Book
```

---

## Relationship Description

### User → Loan

A user may have multiple loans during the lifetime of the account.

Examples:

- One user can borrow multiple books.
- One user can have multiple historical loan records.

---

### Book → Loan

A book can appear in many loan records over time.

Examples:

- A book may be borrowed by different users.
- Historical borrowing activity is maintained.

---

### Loan → User

Each loan belongs to exactly one user.

---

### Loan → Book

Each loan is associated with exactly one book.

---

# Business Rules

## Book Availability

A book can only be borrowed when:

```text
availability_status = Available
```

If the book is already borrowed, the borrowing request must be rejected.

---

## Active Loan Constraint

A loan may only be active when:

- A valid user exists
- A valid book exists
- The book is available

---

## Return Processing

When a book is returned:

- Loan status changes to Completed
- Return date is recorded
- Book becomes available again

---

# Data Validation Rules

## Book Validation

The system validates:

- Required fields
- Valid publication year
- Duplicate records
- ISBN format

---

## User Validation

The system validates:

- Required fields
- Email format
- Duplicate accounts

---

## Loan Validation

The system validates:

- Existing user reference
- Existing book reference
- Book availability
- Loan status consistency

---

# Future Data Model Enhancements

Additional entities planned for future releases include:

## Reservation

Allows users to reserve unavailable books.

Possible attributes:

- reservation_id
- user_id
- book_id
- reservation_date
- status

---

## Review

Stores user feedback and ratings.

Possible attributes:

- review_id
- user_id
- book_id
- rating
- comment

---

## Recommendation

Supports future recommendation features.

Possible attributes:

- recommendation_id
- user_id
- book_id
- recommendation_score

---

# Design Principles

The data model follows several key principles:

- Simplicity
- Maintainability
- Scalability
- Data consistency
- Separation of concerns

The structure is intentionally simple to support learning objectives while providing a solid foundation for future enhancements such as SQL databases, REST APIs, and advanced recommendation capabilities.