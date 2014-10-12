import unittest
from Calendar import *
from Book import *
from Patron import *
from Library import *

class CalendarTest(unittest.TestCase):

    def test_calendar(self):
        cal = Calendar()
        self.assertEqual(0, cal.get_date())
        cal.advance()
        self.assertEqual(1, cal.get_date())

class BookTest(unittest.TestCase):

    def setUp(self):
    	global book
        book = Book("Contact", "Carl Sagan")

    def test_get_title(self):
        self.assertEqual("Contact", book.get_title())

    def test_get_author(self):
        self.assertEqual("Carl Sagan", book.get_author())

    def test_get_due_date(self):
        self.assertEqual(None, book.get_due_date())

    def test_check_out(self):
    	book.check_out(8)
    	self.assertEqual(8, book.get_due_date())

    def test_check_in(self):
    	book.check_in()
    	self.assertEqual(None, book.get_due_date())

class PatronTest(unittest.TestCase):

	def setUp(self):
		global patron
		patron = Patron("Amy Gutmann")
		book_list = []
		book1 = Book("Contact", "Carl Sagan")
		book2 = Book("Huckleberry Finn", "Mark Twain")
		book3 = Book("Exploring Python", "Thomas Jefferson")
		book_list.append(book1)
		book_list.append(book2)
		book_list.append(book3)
		patron.set_books(book_list)

	def test_get_name(self):
		self.assertEqual("Amy Gutmann", patron.get_name())

	def test_get_books(self):
		patrons_list = patron.get_books()
		title1 = patrons_list[0].get_title()
		title2 = patrons_list[1].get_title()
		title3 = patrons_list[2].get_title()
		self.assertEqual("Contact", title1)
		self.assertEqual("Huckleberry Finn", title2)
		self.assertEqual("Exploring Python", title3)

	def test_take(self):
		self.assertEqual(3, len(patron.get_books()))
		book4 = Book("Tom Sawyer", "Samuel Clemens")
		patron.take(book4)
		self.assertEqual(4, len(patron.get_books()))
		self.assertEqual("Tom Sawyer", patron.get_books()[3].get_title())

	def test_give_back(self):
		book_to_return = patron.get_books()[1]
		self.assertEqual(3, len(patron.get_books()))
		patron.give_back(book_to_return)
		self.assertEqual(2, len(patron.get_books()))


class LibraryTest(unittest.TestCase):

    def setUp(self):
    	global cal
    	cal = Calendar()
        global library
        library = Library()
        library.read_book_collection()
        patron1 = Patron("Amy Gutmann")
        patron2 = Patron("Ryan Smith")
        patron3 = Patron("Steve Schenkle")
        patron4 = Patron("Dr Dave")
        full_book_collection = library.get_collection()
        full_book_collection[0].check_out(1)
        full_book_collection[1].check_out(2)
        full_book_collection[2].check_out(2)
        full_book_collection[3].check_out(20)
        full_book_collection[4].check_out(20)
        full_book_collection[5].check_out(20)
        full_book_collection[6].check_out(1)
        full_book_collection[7].check_out(5)
        full_book_collection[8].check_out(4)
        patron1.set_books(full_book_collection[0:3])
        patron2.set_books(full_book_collection[3:6])
        patron3.set_books(full_book_collection[6:9])
        patron_set = [patron1, patron2, patron3, patron4]
        library.set_patrons(patron_set)
            

    def test_get_collection(self):
        self.assertEqual(1063, len(library.get_collection()))

  	def test_open(self):
  		self.assertEqual(False, library.get_is_open())
        library.open()
        self.assertEqual(True, library.get_is_open())

    def test_list_overdue_books(self):
    	library.open()
        library.response = ''
        library.list_overdue_books()
    	self.assertEqual("Hooray! No books are overdue.\n", library.response)

    def test_issue_card(self):
        library.open()
        library.response = ''
        library.issue_card("Greg Brown")
        self.assertEqual("Library card has been issued to Greg Brown.\nNow serving Greg Brown. You currently have:\n\n", library.response)
        library.response = ''
        library.issue_card("Amy Gutmann")
        self.assertEqual("Amy Gutmann already has a library card!\nNow serving Amy Gutmann. You currently have:\n1: 20,000 Leagues Under the Seas.\n2: 52 Pick-up.\n3: A Bend in the River.\n\n", library.response)

    def test_serve(self):
        library.open()
        library.serve("Ryan Smith")
        self.assertEqual("Ryan Smith", library.get_patron_being_served().get_name())
        library.response = ''
        library.serve("Ryan Smitt")
        self.assertEqual("Ryan Smitt does not have a library card.\n", library.response)
  		
    def test_check_in(self):
        library.open()
        library.serve("Ryan Smith")
        library.response = ''
        library.check_in(3)
        self.assertEqual("Ryan Smith has returned 1 books.\n", library.response)
        self.setUp()
        library.open()
        library.serve("Ryan Smith")
        library.response = ''
        library.check_in(3, 2)
        self.assertEqual("Ryan Smith has returned 2 books.\n", library.response)
        self.setUp()  
        library.open()
        library.serve("Ryan Smith")
        library.response = ''
        library.check_in(3, 2, 1)
        self.assertEqual("Ryan Smith has returned 3 books.\n", library.response)

    def test_search(self):
        library.open()
        library.response = ''
        library.search("Hemingway")
        self.assertEqual("1: A Farewell to Arms by Ernest Hemingway.\n2: For Whom the Bell Tolls by Ernest Hemingway.\n3: The Old Man and the Sea by Ernest Hemingway.\n\n", library.response)

    def test_check_out(self):
        library.open()
        library.serve("Dr Dave")
        library.search("the ")
        library.check_out(1, 4, 2)
        library.serve("Dr Dave")


    def test_close(self):
        library.response = ''
        library.close()
        self.assertEqual("The library is already closed.\n", library.response)
        library.response= ''
        library.open()
        self.assertTrue("The library is now open!\n", library.response)
        library.close()
        self.assertFalse(library.get_is_open())









unittest.main()