from .reader import Reader


class Generator(Reader):

    def __init__(self, filename=None, resource=None, encoding="UTF-8"):
        """
        :param filename: If desired, a source text file can be used to generate words.
        :type filename: str
        :param resource: The internal resource, within the package, from which to read text.
        :type resource: str
        :param encoding: The encoding to use when reading the source file.
        :type encoding: str
        """
        super().__init__()
        self.filename = filename
        self.resource = resource
        self.encoding = encoding
        self.delimiter = {".", "?", "!"}

    def generate_words(self, count=100):
        """
        Generates the desired number of words from the desired source text.

        :param count: Number of words to generate
        :type count: int

        :return: A string containing one or more sentences made up of the desired number of words.
        :rtype: str
        """

        with self.open_text_data() as f:
            result = self.read_words(f, count=count)
        return result

    def generate_sentences(self, count=5):
        """
        Generates the desired number of sentences from the desired source text.

        :param count: Number of sentences to generate
        :type count: int

        :return: A string containing one or more sentences.
        :rtype: str
        """

        with self.open_text_data() as f:
            result = self.read_sentences(f, count=count)
        return result

    def generate_paragraphs(self, count=3):
        """
        Generates the desired number of paragraphs from the desired source text.

        :param count: Number of paragraphs to generate
        :type count: int

        :return: A string containing one or more sentences.
        :rtype: str
        """

        with self.open_text_data() as f:
            result = self.read_paragraphs(f, count=count)
        return result
