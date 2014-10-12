
class Calendar(object):
    """Keeps track of the durrent date (as an integer)."""
    def __init__(self):
        """Creates the initial calendar."""
        self.day = 0

    def get_date(self):
        """Returns (as a positive integer) the current date."""
        return self.day

    def advance(self):
        """Advances this calendar to the next date."""
        self.day += 1

