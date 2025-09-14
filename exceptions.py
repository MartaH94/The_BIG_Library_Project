# Exceptions to ignore in the project.

# ------------------------------
# BASE EXCEPTION FOR THE ENTIRE PROJECT
# ------------------------------
class LibraryError(Exception):
    """Base exception for the entire library system."""
    pass



# ------------------------------
# BOOK-RELATED EXCEPTIONS (BookService)
# ------------------------------
class BookError(LibraryError):
    """Base exception for book operations."""
    pass

# CRUD operations
class InvalidBookDataError(BookError):
    """Raised when user tries to add a book with empty title or author."""
    def __init__(self, message="Field author and title canot be empty", book=None):
        super().__init__(message)
        self.book = book

class SearchValueError(BookError):
    """Raised when no search criteria is provided."""
    def __init__(self, message="At least one search criteria must be provided (title, author, year, or searched_term)"):
        super().__init__(message)

class BookNotFoundError(BookError):
    """Raised when book not found in the library."""
    def __init__(self, message="Book not found in the library", book=None):
        super().__init__(message)
        self.book = book
    

class BookAlreadyExistsError(BookError):
    """Book already exists in the library."""
    pass

# Availability
class BookNotAvailableError(BookError):
    """Book is currently unavailable (loaned or reserved)."""
    pass

# Categories
class CategoryNotFoundError(BookError):
    """Category not found."""
    pass

# Validation
class BookValidationError(BookError): 
    """Invalid book data."""
    def __init__(self, message="Invalid book data"):
        super().__init__(message)



# ------------------------------
# LOAN AND RESERVATION EXCEPTIONS (LoanService)
# ------------------------------
class LoanError(LibraryError):
    """Base exception for loans and reservations."""
    pass

class LoanNotFoundError(LoanError):
    """Loan record not found."""
    pass

class ReservationError(LoanError):
    """Error during book reservation."""
    pass

class AlreadyLoanedError(LoanError):
    """Book is already loaned to this user."""
    pass

class LoanValidationError(LoanError):
    """Invalid loan or reservation data."""
    pass


# ------------------------------
# USER AND AUTHENTICATION EXCEPTIONS (AuthService)
# ------------------------------
class UserError(LibraryError):
    """Base exception for user-related operations."""
    pass

class UserNotFoundError(UserError):
    """User not found."""
    pass

class AuthenticationError(UserError):
    """Authentication or login error."""
    pass

class PermissionError(UserError):
    """User does not have permission to perform this operation."""
    def __init__(self, message="User does not have permission to perform this operation"):
        super().__init__(message)
    pass

class UserValidationError(UserError):
    """Invalid user data."""
    pass

class UserInvalidRole(UserError):
    """Invalid user role."""
    pass


# ------------------------------
# GENERAL / UTILITY EXCEPTIONS
# ------------------------------
class ValidationError(LibraryError):
    """General validation error for input data."""
    pass

class DatabaseError(LibraryError):
    """Error related to database operations or data storage."""
    pass

class FileNotFound(LibraryError):
    """File not found in the folder."""
    def __init__(self, message="File doesn't exists in the catalogue."):
        super().__init__(message)

class FileError(LibraryError):
    """Error during file operations (JSON, CSV, etc.)."""
    pass

