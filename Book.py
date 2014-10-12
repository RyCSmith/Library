
class Book(object):
    """Represents one copy of a book. There may be many copies
       of a book with the same title and author.
       Each book has:
         * An id (a unique integer)
         * A title
         * An author (one string, even if many authors)
         * A due date (or None if the book is not checked out.)."""
    
    def __init__(self, title, author):
        """Creates a book, not checked out to anyone."""
        self.title = title
        self.author = author
        self.due_date = None
        
    def get_title(self):
        """Returns the title of this book."""
        return self.title

    def get_author(self):
        """Returns the author(s) of this book, as a single string."""
        return self.author

    def get_due_date(self):
        """If this book is checked out, returns the date on
           which it is due, else returns None."""
        return self.due_date

    def check_out(self, due_date):
        """Sets the due date for this book."""
        self.due_date = due_date

    def check_in(self):
        """Clears the due date for this book (sets it to None)."""
        self.due_date = None

    def __str__(self):
        """Returns a string representation of this book,
        of the form: title, by author"""
        return self.title + ', by ' + self.author

    def __eq__(self, other):
        """Tests if this book equals the given parameter. Not
        required by assignment, but fairly important."""
        return self.title == other.title and self.author == other.author

