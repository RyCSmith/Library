
class Patron(object):
    """Represents a patron of the library. A patron has:
         * A name
         * A set of books checked out"""

    def __init__(self, name):
        """Constructs a new patron, with no books checked out yet."""
        self.name = name
        self.books = []

    def get_name(self):
        """Returns this patron's name."""
        return self.name

    def get_books(self):
        """Returns the set of books checked out to this patron."""
        return self.books

    def set_books(self, books):
        """This allows the user to set the book list for the patron. This will only
        be used in unittesting."""
        self.books = books

    def take(self, book):
        """Adds a book to the set of books checked out to this patron."""
        self.books.append(book)

    def give_back(self, book):
        """Removes a book from the set of books checked out to this patron."""
        self.books.remove(book)

    def __str__(self):
        """Returns the name of this patron."""
        return self.name

