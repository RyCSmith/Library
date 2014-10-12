from Library import *
from Book import *
from Patron import *
from Calendar import *
from Custom_Exceptions import *

def main():
    library = Library()
    library.read_book_collection()
    print len(library.collection), 'books in collection.'
    print "Ready for input. Type 'help()' for a list of commands.\n"
    command = '\0'
    while command != 'quit()':
        try:
            command = raw_input('Library command: ').strip()
            if len(command) == 0:
                print "What? Speak up!\n"
            else:
                eval('library.' + command)
                print library.response
                library.response = ''
        except AttributeError, e:
            print "Sorry, I didn't understand:", command
            print "Type 'help()' for a list of the things I do understand.\n"
        except Exception, e:
            print "Unexpected error:", e            
    
if __name__ == '__main__':
    main()