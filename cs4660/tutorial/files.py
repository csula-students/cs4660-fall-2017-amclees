"""Files tests simple file read related operations"""

from . import lists

class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""
    def __init__(self, file_path):
        """
        __init__  reads the file by path and parses content into a two
        dimension array (numbers)
        """
        open_file = open(file_path, 'r')
        self.numbers = []
        
        for line in open_file:
            self.numbers.append(list(map(int, line.split(' '))))

        open_file.close()

    def get_mean(self, line_number):
        """
        get_mean retrieves the mean value of the list by line_number (starts
        with zero)
        """
        return lists.get_avg(self.numbers[line_number])

    def get_max(self, line_number):
        """
        get_max retrieves the maximum value of the list by line_number (starts
        with zero)
        """
        return max(self.numbers[line_number])

    def get_min(self, line_number):
        """
        get_min retrieves the minimum value of the list by line_number (starts
        with zero)
        """
        return min(self.numbers[line_number])

    def get_sum(self, line_number):
        """
        get_sum retrieves the sumation of the list by line_number (starts with
        zero)
        """
        return lists.get_sum(self.numbers[line_number])
