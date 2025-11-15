

userSchema = {"id": int, "name": str, "email": "str", "role": str}
bookSchema = {"id": int, "title": str, "author": str, "year": int, "isbn": str, "available": bool}
loanSchema = {"id": int, "user_id": int, "book_id": int, "loan_date": str, "return_date": str, "returned": bool}
reservationSchema = {"id": int, "user_id": int, "book_id": int, "reservation_date": str, "fulfilled": bool}
backupSchema = {"file_name": str, "backup_date": str, "size": int}
backupFileSchema = {"file_name": str, "backup_date": str, "size": int}

