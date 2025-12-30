from enum import Enum
from .tokenizer_data import TokenizerData
from .token_names import TokenNames
from .utils import StringUtils
from .constants import Global

class State(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    UNICODE_FINAL_STATE = 8

class GroupToken:
    def __init__(self, type_str, name, type_list=None):
        self.type = type_str
        self.name = name
        self.type_list = type_list if type_list is not None else []

    @staticmethod
    def empty():
        return GroupToken(Global.EMPTY_STRING, Global.EMPTY_STRING)

    def is_empty(self):
        return not self.type or not self.name

    def non_empty(self):
        return not self.is_empty()

    def get_type(self):
        return self.type

    def set_type(self, type_str):
        self.type = type_str

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def is_started_with(self, token_prefix):
        return self.name.startswith(token_prefix)

    def is_ended_with(self, token_suffix):
        return self.name.endswith(token_suffix)

    def is_type_started_with(self, type_prefix):
        return self.type.startswith(type_prefix)

    def is_type_ended_with(self, type_suffix):
        return self.type.endswith(type_suffix)

    def has_token_type(self, token_str):
        return token_str in self.type

    def get_token_index(self, type_str):
        try:
            return self.type_list.index(type_str)
        except ValueError:
            return -1

    def get_last_token_index(self, type_str):
        try:
            return len(self.type_list) - 1 - self.type_list[::-1].index(type_str)
        except ValueError:
            return -1

    def index_of_token_type(self, type_index):
        try:
            return str(self.type_list[type_index])
        except IndexError:
            return Global.EMPTY_STRING

    def remove_type(self, type_str):
        if len(type_str) < len(self.get_type()):
            return self.get_type()[len(type_str) + 1:]
        else:
            return Global.EMPTY_STRING

    def remove_type_upto(self, n):
        idx = StringUtils.ordinal_index_of(self.type, TokenNames.CONNECTOR, n)
        return self.type[idx + 1:]

    def get_type_upto(self, n):
        idx = StringUtils.ordinal_index_of(self.type, TokenNames.CONNECTOR, n)
        return self.type[:idx]

    def remove_last_type(self, type_str):
        if len(self.get_type()) > len(type_str):
            return self.get_type()[:len(self.get_type()) - (len(type_str) + 1)]
        return Global.EMPTY_STRING

    def previous_token(self, rhf_position):
        try:
            return str(self.type_list[rhf_position - 1])
        except IndexError:
            return Global.EMPTY_STRING

    def move_nth_token_type_to_last(self, tok_position):
        tmp_type_list = list(self.type_list)
        type_str = str(tmp_type_list[tok_position])
        del tmp_type_list[tok_position]
        tmp_type_list.append(type_str)
        return TokenNames.CONNECTOR.join(tmp_type_list)

    def get_next_position(self, index):
        try:
            if self.type_list[index + 1] == TokenNames.RV:
                try:
                    if self.type_list[index + 2] == TokenNames.TV:
                        return 2 + index
                except IndexError:
                    return 1 + index
            return index
        except IndexError:
            return index

    def __lt__(self, other):
        return self.type < other.type

    def __str__(self):
        return f"{self.name}{{{self.type}}}"

    def __eq__(self, other):
        if other is None:
            return False
        return self.type == other.type

class UnicodeTokenizer:
    TOKENIZER_DATA = TokenizerData()

    def __init__(self, source_text):
        self.source_text = source_text
        self.tokens_list = []
        self.tokenize()

    def get_grouped_characters(self):
        return self.tokens_list

    def tokenize(self):
        self.initialize_tokenizer()
        token = self.get_next_token()
        while token is not None:
            self.tokens_list.append(token)
            token = self.get_next_token()

    def initialize_tokenizer(self):
        self.source_index = 0

    def get_next_token(self):
        if self.source_index >= len(self.source_text):
            return None

        self.current_token_str = ""
        self.current_state = State.ONE
        self.token_type = TokenNames.ELSE

        while self.source_index < len(self.source_text):
            ch_str = self.get_next_char()
            
            if self.current_state == State.ONE:
                if self.TOKENIZER_DATA.is_whole_vowel(ch_str):
                    self.token_type = TokenNames.WV
                    self.current_state = State.SIX
                elif self.TOKENIZER_DATA.is_whole_consonant(ch_str):
                    self.token_type = TokenNames.WC
                    self.current_state = State.TWO
                elif self.TOKENIZER_DATA.is_devanagari_number(ch_str):
                    self.token_type = TokenNames.NUM
                    self.current_state = State.FIVE
                elif self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.token_type = TokenNames.PCN
                    self.current_state = State.SEVEN
                elif self.TOKENIZER_DATA.is_special_symbol(ch_str):
                    self.token_type = TokenNames.SPS
                    self.current_state = State.UNICODE_FINAL_STATE
                else:
                    self.current_state = State.UNICODE_FINAL_STATE
                self.current_token_str += ch_str

            elif self.current_state == State.TWO:
                if self.TOKENIZER_DATA.is_joinable_symbol(ch_str):
                    self.current_token_str += ch_str
                    self.token_type += TokenNames.CONNECTOR + TokenNames.JS
                    self.current_state = State.UNICODE_FINAL_STATE
                elif self.TOKENIZER_DATA.is_halanta(ch_str):
                    self.current_token_str += ch_str
                    self.token_type += TokenNames.CONNECTOR + TokenNames.HLN
                    self.current_state = State.THREE
                elif self.TOKENIZER_DATA.is_dependent_vowel(ch_str):
                    self.current_token_str += ch_str
                    self.token_type += TokenNames.CONNECTOR + TokenNames.DV
                    self.current_state = State.FOUR
                elif self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.un_get_current_char()
                    self.current_state = State.SEVEN
                else:
                    self.current_state = State.UNICODE_FINAL_STATE
                    self.un_get_current_char()

            elif self.current_state == State.THREE:
                if self.TOKENIZER_DATA.is_whole_consonant(ch_str):
                    self.current_token_str += ch_str
                    self.token_type += TokenNames.CONNECTOR + TokenNames.WC
                    self.current_state = State.TWO
                elif self.TOKENIZER_DATA.is_zwnj(ch_str):
                    self.current_token_str += ch_str
                    self.current_state = State.UNICODE_FINAL_STATE
                    self.token_type += TokenNames.CONNECTOR + TokenNames.ZWNJ
                elif self.TOKENIZER_DATA.is_zwj(ch_str):
                    self.current_token_str += ch_str
                    self.current_state = State.UNICODE_FINAL_STATE
                    self.token_type += TokenNames.CONNECTOR + TokenNames.ZWJ
                elif self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.un_get_current_char()
                    self.current_state = State.SEVEN
                else:
                    self.current_state = State.UNICODE_FINAL_STATE
                    self.un_get_current_char()

            elif self.current_state == State.FOUR:
                if self.TOKENIZER_DATA.is_joinable_symbol(ch_str):
                    self.token_type += TokenNames.CONNECTOR + TokenNames.JS
                    self.current_token_str += ch_str
                elif self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.un_get_current_char()
                    self.current_state = State.SEVEN
                else:
                    self.un_get_current_char()
                self.current_state = State.UNICODE_FINAL_STATE

            elif self.current_state == State.FIVE:
                if self.TOKENIZER_DATA.is_devanagari_number(ch_str):
                    self.current_state = State.FIVE
                    self.current_token_str += ch_str
                elif self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.current_state = State.SEVEN
                    self.un_get_current_char()
                else:
                    self.current_state = State.UNICODE_FINAL_STATE
                    self.un_get_current_char()

            elif self.current_state == State.SIX:
                if self.TOKENIZER_DATA.is_joinable_symbol(ch_str):
                    self.token_type += TokenNames.CONNECTOR + TokenNames.JS
                    self.current_token_str += ch_str
                elif self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.un_get_current_char()
                    self.current_state = State.SEVEN
                else:
                    self.un_get_current_char()
                self.current_state = State.UNICODE_FINAL_STATE

            elif self.current_state == State.SEVEN:
                if self.TOKENIZER_DATA.is_punctuation_mark(ch_str):
                    self.current_token_str += ch_str
                    self.token_type += TokenNames.CONNECTOR + TokenNames.PCN
                    self.current_state = State.SEVEN
                else:
                    self.un_get_current_char()
            
            else:
                self.current_state = State.UNICODE_FINAL_STATE
                self.token_type += TokenNames.ELSE
                self.current_token_str += ch_str

            if self.current_state == State.UNICODE_FINAL_STATE or self.current_state == State.SEVEN:
                break
        
        return GroupToken(self.token_type, self.current_token_str) if self.current_token_str else None

    def get_next_char(self):
        ch = self.source_text[self.source_index]
        self.source_index += 1
        return ch

    def un_get_current_char(self):
        self.source_index -= 1

class SyllableTokenizer:
    @staticmethod
    def find_all_boundaries(word_text):
        tokenizer = UnicodeTokenizer(word_text)
        return [token.get_name() for token in tokenizer.get_grouped_characters()]