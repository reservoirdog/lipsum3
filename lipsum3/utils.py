import os


class Utils:

    def __init__(self):
        self.delimiter = {".", "!", "?"}

    @staticmethod
    def count_words(string):
        """
        Count the number of words in a given string.

        :param string: Text string
        :type string: str
        :return: len(i)
        """

        chop = " ".join([p.strip() for p in string.split("\n")])

        return len(chop.split(" "))

    def count_sentences(self, string):
        """
        Counts the number of sentences in the given string.

        :param string: Text string
        :type string: str
        :return: count
        :rtype: int
        """

        count = 0
        chop = " ".join([p.strip() for p in string.split("\n")])
        for c in chop:
            if c in self.delimiter:
                count += 1

        return count

    @staticmethod
    def count_paragraphs(string):
        """
        Counts the number of sentences in the given string.

        :param string: Text string
        :type string: str
        :return: count
        :rtype: int
        """

        last_line = ""
        count = 0
        for line in string.split('\n'):
            if len(line) > 0 and (len(last_line) == 0 or last_line == "\n"):
                count += 1
            last_line = line

        return count

    @staticmethod
    def rand(*args):
        """
        Securely generates a random number according to the given constraints. If one parameter is given, it is
        assumed that an integer between 0 (inclusive) and max_val (exclusive) is to be generated. If two parameters are
        given, it is assumed that an integer between min_val (inclusive) and max_val (exclusive) is to be generated.

        :param args:
        :return:
        """

        if len(args) == 1:
            min_val, max_val = 0, args[0]
        elif len(args) > 1:
            min_val, max_val = args[0], args[1]
        else:
            raise ValueError("Missing argument(s) for rand()")

        temp_max_val = max_val - min_val

        bits_required = len(bin(temp_max_val)) - 2
        bytes_required = (bits_required // 8) + 1
        rand_val = 0
        cur_bitshift = (bytes_required - 1) * 8
        for b in bytearray(os.urandom(bytes_required)):
            rand_val += b << cur_bitshift
            cur_bitshift -= 8

        return min_val + (rand_val % temp_max_val)
