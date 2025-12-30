from syllabifier.syllable_tokenizer import SyllableTokenizer

def main():
    print("--- Nepali Syllabifier (Type 'exit' to quit) ---")
    
    while True:
        # Get input from user
        word_text = input("\nEnter text: ")
        
        if word_text.lower() == 'exit':
            break
            
        # Process
        boundaries = SyllableTokenizer.find_all_boundaries(word_text)
        
        # Print results
        print(f"Original: {word_text}")
        print(f"Syllables: {boundaries}")

if __name__ == "__main__":
    main()