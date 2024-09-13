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

def get_bip39_words(bin_chunks):
    concatenated_indices = ""  # To hold the concatenated 4-digit indices
    
    for chunk in bin_chunks:
        index = int(chunk, 2)
        
        # Convert index to a 4-digit string with leading zeros if necessary
        index_str = f"{index:04d}"
        
        # Concatenate the 4-digit index
        concatenated_indices += index_str
    
    # Ensure the concatenated_indices string is a valid length
    if len(concatenated_indices) != 48:
        raise ValueError("Concatenated indices do not form a 48-digit string.")
    
    return concatenated_indices

def generate_new_wallet(seed_words):
    # Combine the binary representation of the seed words
    combined_bin = ''.join([format(Wordlist.index(word), '011b') for word in seed_words])
    
    # Split combined binary into 11-bit chunks
    bin_chunks = split_into_chunks(combined_bin)
    
    # Return the concatenated indices of the original seed words
    concatenated_indices = get_bip39_words(bin_chunks)
    
    return concatenated_indices

def split_into_chunks(bin_number):
    return [bin_number[i:i + 11] for i in range(0, len(bin_number), 11)]

