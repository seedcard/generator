from mnemonic import Mnemonic

def get_bip39_words_list():
    """Load the BIP-39 word list."""
    with open('./english.txt') as file:
        lines = [line.rstrip() for line in file]
    assert len(lines) == 2048
    return lines

def words_to_binary(words, bip39_words_list):
    """Convert a list of BIP-39 words to a binary string."""
    binary_str = ""
    for word in words:
        index = bip39_words_list.index(word)
        binary_str += f'{index:011b}'  # Convert to 11-bit binary
    return binary_str

def binary_to_decimal(binary_str):
    """Convert a binary string to a decimal number."""
    return int(binary_str, 2)

def main():
    # Load BIP-39 words list
    bip39_words_list = get_bip39_words_list()
    
    # Example seed words (replace with your actual 12 words)
    seed_words = ["abandon", "ability", "able", "about", "above", "absent", "academy", "account", "accuse", "action", "adapt", "addict"]
    
    # Convert words to binary string
    binary_str = words_to_binary(seed_words, bip39_words_list)
    
    # Convert binary string to decimal number
    decimal_number = binary_to_decimal(binary_str)
    
    # Ensure the decimal number is 48 digits long
    decimal_str = str(decimal_number).zfill(48)
    
    print(f'Binary representation: {binary_str}')
    print(f'Decimal representation: {decimal_str}')
    print(f'Decimal number length: {len(decimal_str)} digits')

if __name__ == "__main__":
    main()
