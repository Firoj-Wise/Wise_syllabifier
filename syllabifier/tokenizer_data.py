class UnicodeTokenizerProperties:
    # Consonant
    DevanagariConsonants = [
        '\u0915', '\u0916', '\u0917', '\u0918', '\u0919', '\u091a', '\u091b', '\u091c', '\u091d', '\u091e', '\u091f', '\u0920',
        '\u0921', '\u0922', '\u0923', '\u0924', '\u0925', '\u0926', '\u0927', '\u0928', '\u0929', '\u092a', '\u092b', '\u092c',
        '\u092d', '\u092e', '\u092f', '\u0930', '\u0931', '\u0932', '\u0933', '\u0934', '\u0935', '\u0936', '\u0937', '\u0938',
        '\u0939', '\u0958', '\u0959', '\u095a', '\u095b', '\u095c', '\u095d', '\u095e', '\u095f'
    ]

    # Independent Vowels
    DevanagariVowels = [
        '\u0905', '\u0906', '\u0907', '\u0908', '\u0909', '\u090a', '\u090b', '\u0960', '\u090c', '\u0961', '\u090f', '\u0910',
        '\u0913', '\u0914', '\u090d', '\u090e', '\u0911', '\u0912'
    ]

    # Dependent Vowels
    DevanagariDependentVowels = [
        '\u093e', '\u093f', '\u0940', '\u0941', '\u0942', '\u0943', '\u0944', '\u0945', '\u0946', '\u0947', '\u0948', '\u0949', '\u094a', '\u094b', '\u094c', '\u0962', '\u0963'
    ]

    # Numbers
    DevanagariNumbers = [
        '\u0966', '\u0967', '\u0968', '\u0969', '\u096a', '\u096b', '\u096c', '\u096d', '\u096e', '\u096f'
    ]

    # Special Joining Symbols
    SpecialJoiningSymbols = [
        '\u0901', '\u0902', '\u0903', '\u093c', '\u093d', '\u0970', '\u0971', '\u0953', '\u0954', '\u0951'
    ]

    # Special Symbols
    SpecialSymbols = ['\u0950', '\u25cc', '\u2219', '\u2212', '\u0964', '\u0952', '\u0965']

    # Halanta
    Halanta = ['\u094d']

    # Zero with Non Joining Character
    NonJoinChar = ['\u200C']

    # Zero with Joiner Character
    JoinChar = ['\u200D']

    @staticmethod
    def get_whole_consonants():
        return UnicodeTokenizerProperties.DevanagariConsonants

    @staticmethod
    def get_whole_vowels():
        return UnicodeTokenizerProperties.DevanagariVowels

    @staticmethod
    def get_dependent_vowels():
        return UnicodeTokenizerProperties.DevanagariDependentVowels

    @staticmethod
    def get_devanagari_numbers():
        return UnicodeTokenizerProperties.DevanagariNumbers

    @staticmethod
    def get_joining_symbols():
        return UnicodeTokenizerProperties.SpecialJoiningSymbols

    @staticmethod
    def get_special_symbols():
        return UnicodeTokenizerProperties.SpecialSymbols

    @staticmethod
    def get_halanta():
        return UnicodeTokenizerProperties.Halanta[0]

    @staticmethod
    def get_non_joining_character():
        return UnicodeTokenizerProperties.NonJoinChar[0]

    @staticmethod
    def get_joining_character():
        return UnicodeTokenizerProperties.JoinChar[0]


class TokenizerData:
    def __init__(self):
        self.WHOLE_CONSONANTS = set(UnicodeTokenizerProperties.get_whole_consonants())
        self.WHOLE_VOWELS = set(UnicodeTokenizerProperties.get_whole_vowels())
        self.DEPENDENT_VOWELS = set(UnicodeTokenizerProperties.get_dependent_vowels())
        self.DEVANAGARI_NUMBERS = set(UnicodeTokenizerProperties.get_devanagari_numbers())
        self.JOINING_SYMBOLS = set(UnicodeTokenizerProperties.get_joining_symbols())
        self.SPECIAL_SYMBOLS = set(UnicodeTokenizerProperties.get_special_symbols())
        self.PUNCTUATION_MARKS = set()
        self.HALANTA_SYMBOL = UnicodeTokenizerProperties.get_halanta()
        self.NON_JOINING_CHAR = UnicodeTokenizerProperties.get_non_joining_character()
        self.JOINING_CHAR = UnicodeTokenizerProperties.get_joining_character()

    def is_whole_consonant(self, ch_str):
        return ch_str in self.WHOLE_CONSONANTS

    def is_whole_vowel(self, ch_str):
        return ch_str in self.WHOLE_VOWELS

    def is_dependent_vowel(self, ch_str):
        return ch_str in self.DEPENDENT_VOWELS

    def is_devanagari_number(self, ch_str):
        return ch_str in self.DEVANAGARI_NUMBERS

    def is_joinable_symbol(self, ch_str):
        return ch_str in self.JOINING_SYMBOLS

    def is_special_symbol(self, ch_str):
        return ch_str in self.SPECIAL_SYMBOLS

    def is_halanta(self, ch_str):
        return self.HALANTA_SYMBOL == ch_str

    def is_zwnj(self, ch_str):
        return self.NON_JOINING_CHAR == ch_str

    def is_zwj(self, ch_str):
        return self.JOINING_CHAR == ch_str

    def is_punctuation_mark(self, ch_str):
        return ch_str in self.PUNCTUATION_MARKS