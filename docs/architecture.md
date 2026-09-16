# Architecture

## Overview

The BIG Library is a modular library management application developed in Python.

The project follows a layered architecture to separate responsibilities and improve maintainability, readability, and testability of the codebase.

The application is organized into independent modules responsible for business logic, data management, and user interactions.

---

## Architecture Principles

The project is based on the following principles:

- Separation of concerns
- Object-Oriented Programming (OOP)
- Modular design
- Maintainable code
- Testable code
- Clear responsibility ownership

---

## High-Level Architecture

```text
User
 │
 ▼
Services Layer
 │
 ├── Book Management
 ├── User Management
 ├── Loan Management
 │
 ▼
Database Layer
 │
 ▼
Data Storage
```

---

## Main Components

### Models

Models represent the core business entities of the application.

Examples:

- Book
- User
- Loan

Responsibilities:

- store business data
- define entity attributes
- support business operations

---

### Services

Services contain the business logic of the application.

Examples:

- BookService
- UserService
- LoanService

Responsibilities:

- process user requests
- validate business rules
- coordinate interactions between components

---

### Database Layer

The database layer is responsible for data persistence.

Responsibilities:

- save data
- load data
- manage storage operations

The layer is isolated from business logic to simplify future database migrations and support scalability.

---

### Utilities

Utility modules provide reusable helper functions.

Examples:

- logging
- validation
- configuration handling
- data formatting

---

### Tests

The project includes automated tests designed to validate business logic, verify expected behaviour, and support regression testing.

The testing approach reflects software testing practices used in real-world projects and helps ensure application quality as the codebase grows.

---

## Project Structure

```text
The_BIG_Library/
│
├── src/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── utils/
│
├── tests/
│
├── docs/
│
└── README.md
```

---

## Design Decisions

### Why Python?

Python was selected because of its readability, extensive ecosystem, and suitability for learning software design and application development.

### Why OOP?

Object-Oriented Programming enables better organization of business entities and supports scalability as the project grows.

### Why Layered Architecture?

Separating business logic from data management improves maintainability, testability, and future extensibility.

---

## Future Architecture Improvements

The current architecture was intentionally designed to support future enhancements.

Planned areas of development include:

- SQL database integration
- REST API built with FastAPI
- Docker containerization
- Authentication and authorization
- Recommendation engine
- CI/CD integration
- Extended automated testing

These improvements will allow the project to evolve from a learning application into a more complete production-style solution.