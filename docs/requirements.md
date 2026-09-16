# Requirements

## Overview

This document describes the functional and non-functional requirements for The BIG Library.

The requirements define the expected behaviour of the system and provide a foundation for implementation, testing, and future enhancements.

---

## System Scope

The BIG Library is a library management application that enables users to manage books, library members, and lending operations.

The system focuses on supporting core library processes while providing a maintainable and scalable architecture.

---

# Functional Requirements

## Book Management

### FR-001 Add Book

The system shall allow a user to add a new book to the library catalogue.

### FR-002 View Book Details

The system shall allow a user to view information about a selected book.

### FR-003 Search Books

The system shall allow a user to search for books using defined criteria.

### FR-004 Update Book Information

The system shall allow a user to update information about an existing book.

### FR-005 Remove Book

The system shall allow a user to remove a book from the catalogue.

### FR-006 Prevent Duplicate Books

The system shall prevent duplicate book records based on defined validation rules.

---

## User Management

### FR-007 Register User

The system shall allow a new library user to be registered.

### FR-008 View User Information

The system shall allow viewing details of a registered user.

### FR-009 Update User Information

The system shall allow modification of existing user information.

### FR-010 Remove User

The system shall allow removal of a user from the system.

### FR-011 Prevent Duplicate Users

The system shall prevent creation of duplicate user records.

---

## Loan Management

### FR-012 Borrow Book

The system shall allow a user to borrow an available book.

### FR-013 Return Book

The system shall allow a borrowed book to be returned.

### FR-014 Track Active Loans

The system shall maintain information about active loans.

### FR-015 Prevent Borrowing Unavailable Books

The system shall prevent borrowing books that are already loaned out.

### FR-016 View Loan History

The system shall provide access to historical loan records.

---

## Validation

### FR-017 Mandatory Fields Validation

The system shall validate that required fields are completed.

### FR-018 Invalid Input Validation

The system shall reject invalid user input.

### FR-019 Business Rule Validation

The system shall verify that all business rules are satisfied before processing requests.

---

## Data Management

### FR-020 Save Data

The system shall support data persistence.

### FR-021 Load Data

The system shall allow previously stored data to be loaded.

### FR-022 Maintain Data Integrity

The system shall ensure consistency of stored information.

---

# Non-Functional Requirements

## NFR-001 Maintainability

The application shall be implemented using a modular architecture to simplify maintenance and future development.

## NFR-002 Scalability

The architecture shall support future enhancements without major redesign.

## NFR-003 Testability

Application components shall be designed to support automated testing.

## NFR-004 Reliability

The application shall handle expected errors without unexpected termination.

## NFR-005 Usability

The application shall provide clear messages and predictable behaviour.

---

# Future Requirements

The following requirements are planned for future releases.

### FR-023 User Authentication

The system shall allow users to authenticate using credentials.

### FR-024 Reservation Management

The system shall allow users to reserve books.

### FR-025 REST API

The system shall expose selected functionality through REST endpoints.

### FR-026 Recommendation Engine

The system shall provide book recommendations based on user activity.

### FR-027 Container Deployment

The system shall support deployment using Docker.

---

# Requirement Traceability

The requirements defined in this document provide the basis for:

- Solution design
- Architecture decisions
- Test scenarios
- Automated tests
- Future development planning

Each implemented feature should be traceable to one or more documented requirements.
