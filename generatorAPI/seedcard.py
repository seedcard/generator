import secrets
import hashlib
import random
import qrcode
import getpass
from PIL import Image
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39MnemonicValidator, Bip39WordsNum, Bip39MnemonicDecoder, Bip44, Bip44Coins, Bip44PublicKey
from mnemonic import Mnemonic
from wordlist import Wordlist
from checksum import checkSum
from figerprint import compute_fingerprint
from generate import generate_new_wallet

sparrow_same = []
def hex_to_decimal(hex_str):
    """
    Convert a hexadecimal string to a decimal number.

    Parameters:
    hex_str (str): The hexadecimal string (e.g., '1a', 'FF', '0x1A')

    Returns:
    int: The decimal representation of the hexadecimal string
    """
    try:
        # Remove '0x' prefix if present
        if hex_str.startswith('0x'):
            hex_str = hex_str[2:]
        
        # Convert hexadecimal to decimal
        decimal_number = int(hex_str, 16)
        return decimal_number
    except ValueError as e:
        print(f"Error: {e}")
        return None
    
def generate_random_number():
    print("Generating a random 128-bit number using a cryptographically secure method...")
    random_number = secrets.randbits(128)
    return random_number



def format_number(number):
    hex_format = hex(number)[2:]  # Convert to hex and strip the "0x" prefix
    bin_format = bin(number)[2:].zfill(128)  # Convert to binary and pad to 128 bits
    return hex_format, bin_format

def split_into_chunks(bin_number):
    print("Splitting the binary number into 11-bit chunks...")
    return [bin_number[i:i + 11] for i in range(0, len(bin_number), 11)]

def sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest(), bin(int(sha256.hexdigest(), 16))[2:].zfill(256)

mnemo = Mnemonic("english")

# def get_bip39_words(bin_chunks):
#     words = []
#     # Use Bip39MnemonicValidator to get the wordlist
#     # wordlist = Bip39WordsNum.Wordlist()
#     # print(wordlist)
#     for chunk in bin_chunks:    
#         index = int(chunk, 2)
#         print(index, chunk)
#         word = Wordlist[index]
#         words.append(word)
#     return words
def get_bip39_words(bin_chunks):
    words = []
    concatenated_indices = ""  # To hold the concatenated 4-digit indices
    
    for chunk in bin_chunks:
        index = int(chunk, 2)
        
        # Convert index to a 4-digit string with leading zeros if necessary
        index_str = f"{index:04d}"
        
        # Concatenate the 4-digit index
        concatenated_indices += index_str
        
        word = Wordlist[index]
        words.append(word)
    
    # Ensure the concatenated_indices string is a valid length
    if len(concatenated_indices) != 48:
        raise ValueError("Concatenated indices do not form a 48-digit string.")
    
    return words, concatenated_indices


# def generate_new_walletx(seed_words):
#     # seed_wordsmod = seed_words[:3] + sparrow_same + seed_words[9:12]
#     # print("seed_wordsmod", seed_wordsmod)
#     # Combine the binary representation of the seed words
#     combined_bin = ''.join([format(Wordlist.index(word), '011b') for word in seed_words])
    
#     # Generate the checksum word
    

#     # Convert combined binary to a 128-bit number
#     combined_number = int(combined_bin, 2)
    
#     # Generate new 128-bit seed from combined number
#     new_hex, new_bin = format_number(combined_number)
    
#     # Generate new BIP-39 words
#     new_words = get_bip39_words(split_into_chunks(new_bin))
    
#     # sparrow_same.extend(new_words[3:9])
#     # Return new wallet seed words
#     return new_words, new_hex

def generate_new_walletx(seed_words):
    # Combine the binary representation of the seed words
    combined_bin = ''.join([format(Wordlist.index(word), '011b') for word in seed_words])
    
    # Convert combined binary to a 128-bit number
    combined_number = int(combined_bin, 2)
    
    # Generate new 128-bit seed from combined number
    new_hex, new_bin = format_number(combined_number)
    
    # Generate new BIP-39 words
    new_words, concatenated_indices = get_bip39_words(split_into_chunks(new_bin))
    
    # Generate BIP44 account object for the new wallet
    seed_bytes, seed_phrase = mnemonic_to_seed(new_words)
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_acc = bip44_mst.Purpose().Coin().Account(0)

    concatenated_indices_old = concatenated_indices
    
    return new_words, new_hex

# def create_qr_code_flask(data, filename="qr_code.png"):
def create_qr_code_flask(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    # img.save(filename)
    return img


def create_qr_code(data, filename="qr_code.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    img.show()  # Display the QR code

def verify_password(saved_password):
    entered_password = getpass.getpass("Enter Password: ")
    return entered_password == saved_password

def mnemonic_to_seed(seed_words, passphrase=""):
    """Convert mnemonic phrase to seed."""
    mnemo = Mnemonic("english")
    seed_phrase = " ".join(seed_words)
    print(f"Seed Phrase: {seed_phrase}")  # Debug: Print seed phrase
    # if not mnemo.check(seed_phrase):
    #     raise ValueError("Invalid mnemonic phrase")
    return mnemo.to_seed(seed_phrase, passphrase), seed_phrase

def generate_xpub(seed_words):
    """Generate an xpub from a list of seed words."""
    # Convert the seed words to a seed

    # sparrow_same.extend(seed_words[3:9])
    seed_bytes, seed_phrase = mnemonic_to_seed(seed_words)
    # Generate BIP44 master key
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    
    # Derive the account xpub (m/44'/0'/0')
    bip44_acc = bip44_mst.Purpose().Coin().Account(0)
    xpub = bip44_acc.PublicKey().ToExtended()
    
    return xpub, bip44_acc, seed_phrase

def main():
    print("Welcome to the SEEDCARD BIP-39 Bitcoin Wallet Generator!\n")

    # Prompt user to set a password
    password = getpass.getpass("Set Password: ")
    confirm_password = getpass.getpass("Confirm your password: ")
    if password != confirm_password:
        print("Passwords do not match. Exiting...")
        return

    # Step 1: Generate or Input a Random 128-bit Number
    choice = input("Would you like to generate a random 128-bit number? (y/n): ").strip().lower()
    if choice == 'y':
        random_number = generate_random_number()
    else:
        number_input = input("Please enter a 128-bit number in hexadecimal format (without 0x prefix): ").strip()
        random_number = int(number_input, 16)

    hex_format, bin_format = format_number(random_number)
    print(f"Random Number in Hexadecimal: {hex_format}")
    print(f"Random Number in Binary: {bin_format}")

    # Step 2: Option to Split Binary Number into 11-bit Chunks
    choice = input("Would you like to represent this seed in binary and split it into 11-bit chunks? (y/n): ").strip().lower()
    if choice == 'y':
        bin_chunks = split_into_chunks(bin_format)
        print("11-bit Chunks:")
        for chunk in bin_chunks:
            print(chunk)

        # Step 3: SHA-256 Hash of the Seed
        hex_hash, bin_hash = sha256_hash(bin_format)
        print(f"\nSHA-256 Hash of the Seed in Hexadecimal: {hex_hash}")
        print(f"SHA-256 Hash of the Seed in Binary: {bin_hash}")

        # Step 4: Assign BIP-39 Mnemonic Words
        choice = input("Would you like to assign a BIP-39 word to each 11-bit chunk? (y/n): ").strip().lower()
        if choice == 'y':
            words, concatenated_indices = get_bip39_words(bin_chunks)
            print("Seed words assigned successfully.")
            print(words)

            
            # New Step: Generate xpub Key
            choice = input("Would you like to generate an xpub? (y/n): ").strip().lower()
            if choice == 'y':
                xpub, bip44_acc, seed_phrase = generate_xpub(words)
                print(f"\nxpub Key: {xpub}")
                # create_qr_code(xpub, filename="xpub_qr.png")

            else:
                print("xpub generation skipped.")

            
            # Step 5: Generate a New Wallet Using Seed Words 4 to 9
            choice = input("Would you like to generate a new wallet using seed words 4 to 9? (y/n): ").strip().lower()
            if choice == 'y':
                word_reserve = ["alpha", "between", "balance","balcony", "dog"]
                new_wallet_words, new_wallet_hex = generate_new_walletx(words)
                check_word_new_wallet = checkSum(new_wallet_words[:-1])
                new_wallet_words[-1] = check_word_new_wallet
                # Compute and display the fingerprint for the first new wallet
                new_wallet_fingerprint = compute_fingerprint(' '.join(new_wallet_words))
                print(f"First New Wallet Fingerprint: {new_wallet_fingerprint}")

                sparrow_same.extend(new_wallet_words[3:9])
                sparrow_words = word_reserve[:3] + sparrow_same + word_reserve[3:]
                # print(sparrow_words)
                check_word = checkSum(sparrow_words)
                sparrow_words.append(check_word)

                # new_wallet_words, bip44_acc, new_wallet_hex, concatenated_indices_old, seed_phrase = generate_new_walletx(sparrow_words)
                # print(f"New Wallet Seed Words (12 words): {' '.join(new_wallet_words)}")
                concatenated_indices = generate_new_wallet(sparrow_words)
                # decimal_number = hex_to_decimal(new_wallet_hex)
                # print(sparrow_words)
                print("\nNew Wallet Generated:")
                print(f"New Wallet Seed Words (12 words): {' '.join(sparrow_words)}")
                # print(f"New Wallet Seed Words (12 words): {seed_phrase}")
                print(f"New Wallet Decimal: {concatenated_indices}")
                # print(f"48 bits: {concatenated_indices}")
                
                # Create and display QR code
                # create_qr_code(concatenated_indices)

                # Compute and display the fingerprint for the new wallet
                new_wallet_fingerprint = compute_fingerprint(' '.join(sparrow_words))
                print(f"New Wallet Fingerprint: {new_wallet_fingerprint}")
            else:
                print("Generating a new wallet skipped.")

            # Step 6: Display BIP-39 Seed Words in Positions 4 to 9 with Password Protection
            choice = input("Would you like to display BIP-39 seed words in positions 4 to 9? (y/n): ").strip().lower()
            if choice == 'y':
                print("\nSeed Words in Positions 4 to 9:")
                for i in range(3, 9):  # Positions 4 to 9 (index 3 to 8)
                    print(f"Word {i + 1}: {words[i]}")
            else:
                print("Displaying words skipped.")

            # Step 7: Randomize the Remaining Hidden Words
            hidden_words = [words[i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
            original_positions = [1, 2, 3, 10, 11, 12]  # Their original positions
            # Create a map of hidden words to their original positions (1-based index)
            hidden_word_map = {words[i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
            choice = input("Would you like to randomize the six hidden words? (y/n): ").strip().lower()
            if choice == 'y':
                random.shuffle(hidden_words)
                print("\nHidden Words Randomized and Displayed in New Order:")
                for idx, word in enumerate(hidden_words, start=1):
                    print(f"New Position {idx}: {word}")

                # Saving the randomization pattern
                randomization_pattern = [hidden_word_map[word] for word in hidden_words]
                print("\nRandomization pattern saved for future use.")

                # Step 8: Display the Order Used to Randomize Hidden Words with Password Protection
                choice = input("Would you like to display the order used to randomize the hidden words? (y/n): ").strip().lower()
                if choice == 'y':
                    print("\nOrder of Hidden Words after Randomization:")
                    print(" / ".join(map(str, randomization_pattern)))
                else:
                    print("Displaying randomization order skipped.")
            else:
                print("Randomization of hidden words skipped.")

            # Step 9: Enter a Wallet Name
            wallet_name = None
            choice = input("Would you like to enter the wallet name? (y/n): ").strip().lower()
            if choice == 'y':
                while True:
                    wallet_name = input("Enter a 16-character wallet name: ").strip()
                    if len(wallet_name) == 16:
                        print(f"Wallet name '{wallet_name}' has been set.")
                        break
                    else:
                        print("Invalid input. The wallet name must be exactly 16 characters long.")
            else:
                print("Entering a wallet name skipped.")

            # Step 10: Display Wallet Name as a QR Code
            if wallet_name:
                choice = input("Would you like to display the wallet name as a QR code? (y/n): ").strip().lower()
                if choice == 'y':
                    create_qr_code(wallet_name, filename="wallet_name_qr.png")
                else:
                    print("Displaying wallet name as QR code skipped.")
        else:
            print("Mnemonic word assignment skipped.")
    else:
        print("Binary chunking and mnemonic generation skipped.")

if __name__ == "__main__":
    main()
