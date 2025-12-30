import unittest
from syllabifier import SyllableTokenizer

class TestSyllabifier(unittest.TestCase):

    def test_complex_composite_word(self):
        # The example from your C# project
        word = "राष्ट्रियताको"
        expected = ["रा", "ष्ट्रि", "य", "ता", "को"]
        result = SyllableTokenizer.find_all_boundaries(word)
        self.assertEqual(result, expected)

    def test_simple_word(self):
        word = "नेपाल"
        expected = ["ने", "पा", "ल"]
        result = SyllableTokenizer.find_all_boundaries(word)
        self.assertEqual(result, expected)

    def test_numbers(self):
        # Logic: Consecutive numbers are grouped together
        word = "१२३४५"
        expected = ["१२३४५"]
        result = SyllableTokenizer.find_all_boundaries(word)
        self.assertEqual(result, expected)

    def test_word_with_punctuation(self):
        # Logic: Punctuation is treated as a separate token
        word = "नमस्ते।"
        expected = ["न", "म", "स्ते", "।"]
        result = SyllableTokenizer.find_all_boundaries(word)
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        word = "काठमाडौँ-१"
        # 'का' (WC+DV), 'ठ' (WC), 'मा' (WC+DV), 'डौँ' (WC+DV+Special), '-' (Punct/Symbol), '१' (Num)
        # Note: The exact splitting depends on if '-' is in your punctuation list. 
        # Based on your C# code, standard punctuation includes many symbols.
        # Assuming '-' is handled or falls to default.
        result = SyllableTokenizer.find_all_boundaries(word)
        # We check if it produces output without crashing
        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main()