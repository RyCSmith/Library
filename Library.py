# Written by Ryan Smith and Steven Schenkel
from Book import *
from Patron import *
from Calendar import *
from Custom_Exceptions import *

class Library(object):
    """Provides operations available to the librarian."""
    
    def __init__(self):
        """Constructs a library, which involves reading in a
           list of books that are in this library's collection."""
        
        # Create a global calendar, to be used by many classes
        global calendar
        calendar = Calendar()
        
        # Initialize some instance variables for _this_ library
        self.is_open = False            # Is library open?
        self.collection = []            # List of all Books
        self.patrons = []             # Set of all Patrons
        self.patron_being_served = None # Current patron
        self.response = ''              # Accumulated messages to print
        self.found_books = []          #This will be used for current book offerings

    def get_patron_being_served(self):
        """Returns the patron_being_served variable."""
        return self.patron_being_served

    def get_found_books(self):
        """Returns the found_books variable."""
        return self.found_books
    
    def read_book_collection(self):# Read in the book collection
        """Creates the library's book collection."""
        file = open('collection.txt')
        for line in file:
            if len(line) > 1:
                tuple = eval(line.strip())
                self.collection.append(Book(tuple[0], tuple[1]))
        file.close()

    def open(self):
        """Opens this library for business at the start of a new day."""
        try:
            if self.is_open:
                raise ClosedError, 'Library Already Open'
            else:
                self.is_open = True
                calendar.advance()
                self.talk("The library is now open!")
        except ClosedError, e:
            self.talk("The library is already open!")

    def list_overdue_books(self):
        """Returns a nicely formatted, multiline string, listing the 
        names of patrons who have overdue books, and for each such patron, 
        the books that are overdue. Or, it returns the string "No books are overdue."."""
        global calendar
        try:
            if self.is_open == False:
                raise ClosedError, 'Library not open.'
            builder_string = ''
            add_person = False 
            for person in self.patrons:
                book_list = person.get_books()
                for item in book_list:
                    if item.get_due_date() < calendar.get_date():
                        builder_string = "OVERDUE: " + item.get_title() + " was due on: " + str(item.get_due_date()) + ".\n" + builder_string
                        add_person = True
                if add_person:
                    builder_string = person.get_name() + ":\n" + builder_string
                    add_person = False
            if len(builder_string) > 0:
                self.talk(builder_string + "Today is " + str(calendar.get_date()))
            else:
                self.talk("Hooray! No books are overdue.")
        except ClosedError, e:
            self.talk("The library is closed.")

    def has_library_card(self, name_of_patron):
        """Tests if name_of_patron has a library card"""
        for person in self.patrons:
            if name_of_patron.lower() == person.get_name().lower():
                return True
        return False
    
    def issue_card(self, name_of_patron):
        """Allows the named person the use of this library. For
           convenience, immediately begins serving the new patron."""
        try:
            if self.is_open == False:
                raise ClosedError, 'Library not open.'
            if self.has_library_card(name_of_patron):
                self.talk(name_of_patron + " already has a library card!")
            else:
                p = Patron(name_of_patron)
                self.patrons.append(p)
                self.talk("Library card has been issued to " + name_of_patron + ".")
                
            self.serve(name_of_patron)
        except ClosedError, e:
            self.talk("The library is closed.")
        except AttributeError, x:
            self.talk(AttributeError)

    def serve(self, name_of_patron):
        """Saves the given patron in an instance variable. Subsequent
           check_in and check_out operations will refer to this patron,
           so that the patron's name need not be entered many times.
           If the librarian attempts to serve a person who does not have 
           a card any value in patron_being_served will be reset to None
           in order to avoid possible confusion."""
        try:
            if self.is_open == False:
                raise ClosedError, 'Library not open'
            if not self.has_library_card(name_of_patron):
                self.patron_being_served = None
                self.talk(name_of_patron + " does not have a library card.")
            else:
                for person in self.patrons:
                    if name_of_patron.lower() == person.get_name().lower():
                        self.patron_being_served = person
                        self.found_books = []
                        borrowed_books = person.get_books()
                        books_string = ''
                        i = 1
                        for current_book in borrowed_books:
                            books_string += str(i) + ": " + current_book.get_title() + ".\n"
                            self.found_books.append(current_book)
                            i += 1
                        self.talk("Now serving " + person.get_name() + ". You currently have:\n" + books_string)
        except ClosedError, e:
            self.talk("The library is closed.")

    def sort_checkout_list(self, book_numbers):
        """Sorts the patron's check_out tuple in ascending order.
           Returns an ordered list."""
        sorted_book_numbers = []
        book_numbers = set(book_numbers)
        book_numbers_list = list(book_numbers)
        for i in range(len(book_numbers_list)):
            sorted_book_numbers.append(min(book_numbers_list))
            book_numbers_list.remove(sorted_book_numbers[i])
        return sorted_book_numbers
    
    def check_in(self, *book_numbers):
        """Accepts books being returned by the patron being served,
           and puts them back "on the shelf"."""
        try:
            if self.is_open == False:
                raise ClosedError, 'Library not open'
            if self.patron_being_served == None:
                raise NoCurrentPatronError, 'No patron'
            if len(book_numbers) == 0:
                raise IndexError, 'No book numbers'

            """this converts tuple to list and sorts in order from min to max"""
            tally = 0
            sorted_book_numbers = self.sort_checkout_list(book_numbers)
            
            """this counts down from max index to min and removes due dates from
            book in collection and removes the book itself from the Patron's account"""
            for i in range(len(sorted_book_numbers)-1, -1, -1):
                search_list_index = sorted_book_numbers[i] - 1
                for current_book in self.collection:
                    if current_book.get_title() == self.found_books[search_list_index].get_title():
                        current_book.check_in()
                        tally +=1
                        person = self.get_patron_being_served()
                        for borrowed_book in person.get_books():
                            if borrowed_book.get_title() == self.found_books[search_list_index].get_title():
                                person.give_back(borrowed_book)
                        #Break to prevent "checking in" multiple copies of the same book
                        break
            self.talk(self.patron_being_served.get_name() + " has returned " + str(tally) + " books.")

        except IndexError, e:
            self.talk("No book number provided.")
        except ClosedError, x:
            self.talk("The library is closed.")
        except NoCurrentPatronError, z:
            self.talk("No patron currently being served.")

    def is_found_already(self, book):
        """Finds out if 'book' is already inside of the found_books_list"""
        for current_found_book in self.get_found_books():
            if current_found_book.get_title().lower() == book.get_title().lower():
                return True
        return False
    
    def search(self, string):
        """Looks for books with the given string in either the
           title or the author's name, and creates a globally
           available numbered list in self.found_books."""
        try:
            if self.is_open == False:
                raise ClosedError, 'Library not open'
            if len(string) < 4:
                raise TooShortError, 'String not at least 4 characters'
            string = string.lower()
            self.found_books = []

            for current_library_book in self.collection:
                if current_library_book.get_title().lower().find(string) != -1 or \
                   current_library_book.get_author().lower().find(string) != -1:
                    if current_library_book.get_due_date() == None \
                       and not self.is_found_already(current_library_book):
                            if len(self.found_books) < 10:
                                self.found_books.append(current_library_book)
                            else:
                                break

            if len(self.found_books) == 0:
                self.talk("No books found.")
            else:
                i = 1
                builder_string = ''
                for book in self.found_books:
                    builder_string += str(i) + ": " + book.get_title() + " by " + book.get_author() + ".\n"
                    i += 1
                self.talk(builder_string)

        except ClosedError, e:
            self.talk("The library is closed.")
        except TooShortError, z:
            self.talk("Search strings must be at least 4 characters long.")

    def check_out(self, *book_numbers):
        """Checks books out to the patron currently being served.
           Books will be due seven days from "today".
           Patron must have a library card, and may have not more
           than three books checked out at a time."""
        try:
            if self.is_open == False:
                raise ClosedError, 'Library not open'
            if self.patron_being_served == None:
                raise NoCurrentPatronError, 'No patron'
            if len(book_numbers) == 0:
                raise IndexError, 'No book numbers'
            if len(self.patron_being_served.get_books()) + len(book_numbers) > 3:
                raise MaxBooksError, 'Too many books'

            """this converts tuple to list and sorts in order from min to max"""
            tally = 0
            sorted_book_numbers = self.sort_checkout_list(book_numbers)
     
            for i in range(len(sorted_book_numbers)-1, -1, -1):
                search_list_index = sorted_book_numbers[i] - 1
                for current_book in self.collection:
                    if current_book.get_title() == self.found_books[search_list_index].get_title():
                        self.found_books[search_list_index].check_out(calendar.get_date() + 7)
                        tally += 1
                        person = self.get_patron_being_served()
                        person.take(self.found_books[search_list_index])
                        #Break the loop to avoid adding multiples of the same book
                        break
            self.talk(self.patron_being_served.get_name() + " has checked out " + str(tally) + " books.")

        except IndexError, e:
            self.talk("No book number provided.")
        except ClosedError, x:
            self.talk("The library is closed.")
        except NoCurrentPatronError, z:
            self.talk("No patron currently being served.")
        except MaxBooksError, w:
            self.talk("No patron can take out more than 3 books at a time.")
        except :
            self.talk("Please use the book number from the search list to check out a book/books.")

    def close(self):
        """Closes the library for the day."""
        try:
            if self.is_open == False:
                raise ClosedError, "Library already closed"
            else:
                self.is_open = False
                self.patron_being_served = None
                self.found_books = []
                self.talk("The library is now closed for the day.")
        except ClosedError, e:
            self.talk("The library is already closed.")

        

    def quit(self):
        pass

    def get_collection(self):
        """This returns the collection of books and is only used for unit testing."""
        return self.collection

    def get_is_open(self):
        """This returns the value of is_open and is only used for unit testing."""
        return self.is_open

    def set_patrons(self, patrons):
        """This accepts a set to set the set of patrons and is only used for unit testing."""
        self.patrons = patrons
    
    def get_patrons(self):
        """This returns the list of patrons and is only used for unit testing."""
        return self.patrons

    def help(self):
        self.talk("""
help()
     Repeat this list of commands.
open()
     Opens the library for business; do this once each morning.
     
list_overdue_books()
     Prints out information about books due yesterday.
     
issue_card("name_of_patron")
     Allows the named person the use of the library.
     
serve("name_of_patron")
     Sets this patron to be the current patron being served.
     
search("string")
     Searches for any book or author containing this string
     and displays a numbered list of results.
     
check_out(books...)
     Checks out books (by number) to the current patron.
     
check_in(books...)
     Accepts returned books (by number) from the current patron.
     
close()
     Closes the library at the end of the day.

quit()
     Closes the library for good. Hope you never have to use this!""")

    # ----- Assorted helper methods (of Library) -----

    def talk(self, message):
        """Accumulates messages for later printing. A newline is
           appended after each message."""
        self.response += message + '\n'

    # Feel free to add any more helper methods you would like
