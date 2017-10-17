import pkg_resources
import os
import os.path
from io import open

from .utils import Utils


class Reader:

    def __init__(self, filename=None, resource=None, encoding="UTF-8"):
        """
        :param filename: If desired, a source text file can be used to generate words.
        :type filename: str
        :param resource: The internal resource, within the package, from which to read text.
        :type resource: str
        :param encoding: The encoding to use when reading the source file.
        :type encoding: str
        """
        self.filename = filename
        self.resource = resource
        self.encoding = encoding
        self.delimiter = None

    def prep_string(self, string):
        """
        Preps and cleans up the string
        :param string:
        :type string: str
        :return:
        """

        # Pull global param
        delimiter = self.delimiter

        # Clear mutable default argument
        if delimiter is None:
            delimiter = [".", "?", "!"]

        if len(string) > 1:
            # Replace any double-spaces with single ones
            result = string.strip().replace("  ", " ")
            # Capitalise the first letter of the string
            result = ("{0}".format(result[0]).upper() + result[1:])
            # Ensure a delimiter at the end of the string
            if result[-1] not in delimiter:
                result = result[:-1] + delimiter[Utils.rand(len(delimiter))]
            return result

        # Nothing to do
        return string

    def open_text_data(self, random_para=True):
        """
        Opens the given file or resource for reading as a lipsum3 text data file.

        :param random_para: Open the file at a random paragraph? (default: True)
        :type random_para: bool

        :return: A file descriptor that can be used for reading the contents of the file.
        """

        r = ''
        fn = ''

        if self.filename is None and self.resource is None:
            r = "data/definibus.txt"

        if self.filename is None:
            fn = pkg_resources.resource_filename("lipsum3", r)

        file_size = os.path.getsize(fn)
        if file_size < 102400:
            raise IOError("Input file must be at least 100KB in size, but is {0}KB".format(file_size))

        f = open(fn, "rb")
        if random_para:
            self.seek_to_random_paragraph(f, file_size)

        return f

    def wrapped_readline(self, f):
        """
        Attempt to read a line of text from the given file and wraps back around to the beginning of
        the file when the end of the file has been reached.

        :param f:
        :type f:
        :return:
        """
        line = f.readline(1024).decode(self.encoding)

        # EOF?
        if len(line) == 0:
            f.seek(0, os.SEEK_SET)
            # Hope we find a line now
            line = f.readline(1024).decode(self.encoding)
        return line

    def seek_to_random_paragraph(self, f, file_size):
        """
        Randomly seek to a paragraph

        :param f:
        :param file_size:
        :return:
        """

        # Seeks to a random byte position in the file
        f.seek(Utils.rand(file_size), os.SEEK_SET)

        # Read lines until we find the begining of the next paragraph
        done = False
        last_line = ""

        while not done:
            line = self.wrapped_readline(f)

            # If we've encountered a line of text after one or more newlines, consider it the beginning of a new
            # paragraph
            if last_line == "\n" and len(line) > 1:
                # Seek backwards to the beginning of the line
                f.seek(-len(line), os.SEEK_CUR)
                done = True

            last_line = line

    def read_words(self, f, count=100):
        """
        Reads the given number of words from the specified open file.

        :param f:
        :param count:
        :return:
        """

        result = []
        while len(result) < count:
            line = self.wrapped_readline(f).strip()
            words = [w.strip() for w in line.split(" ")]
            # remove empty words
            words = [w for w in words if len(w) > 0]
            if len(result) + len(words) > count:
                result.extend(words[:count-len(result)])
            else:
                result.extend(words)

        return self.prep_string(" ".join(result))

    def read_sentences(self, f, count=5):
        """
        Reads the given number of sentences from the specified open file.

        :param f:
        :param count:
        :return:
        """
        result = []
        cur_sentence = ""
        while len(result) < count:
            line = self.wrapped_readline(f).strip()
            if len(line) > 0:
                for c in line:
                    cur_sentence += c
                    if c in self.delimiter:
                        result.append(self.prep_string(cur_sentence))
                        cur_sentence = ""
                        if len(result) >= count:
                            break

        return " ".join(result)

    def read_paragraphs(self, f, count=3):
        """
        Reads the given number of paragraphs of text from the specified open file.

        :param f:
        :param count:
        :return:
        """

        result = []
        cur_paragraph = ""
        last_line = ""
        while len(result) < count:
            line = self.wrapped_readline(f)
            # if we've hit the end of a paragraph
            if len(last_line) > 1 and line == "\n":
                result.append(self.prep_string(cur_paragraph))
                cur_paragraph = ""
            elif len(line) > 1:
                # if we're still building the current paragraph
                cur_paragraph += line

            last_line = line

        return "\n\n".join(result)
