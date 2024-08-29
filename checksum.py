from hashlib import sha256
import binascii

def get_bip39_words_list():
    """Load the BIP-39 word list."""
    with open('./english.txt') as file:
        lines = [line.rstrip() for line in file]
    assert len(lines) == 2048
    return lines

def find_first_suggestion(seed_list, bip39_words_list):
    """Find the first suggested word to complete the mnemonic."""
    # Convert seed list to binary string
    bits_string = ''
    for word in seed_list:
        decimal_index = bip39_words_list.index(word)
        binary_index = bin(decimal_index)[2:].zfill(11)
        bits_string += binary_index

    # Determine the number of bits to add based on seed length
    if len(seed_list) == 11:
        bits_to_add = 7
        chars_for_checksum = 1
    elif len(seed_list) == 23:
        bits_to_add = 3
        chars_for_checksum = 2
    else:
        raise ValueError("Seed list must be 11 or 23 words long")

    # Create the candidate with the smallest binary addition
    combo = '0' * bits_to_add
    entropy = f'{bits_string}{combo}'
    hexstr = "{0:0>4X}".format(int(entropy, 2)).zfill(len(entropy) // 4)
    data = binascii.a2b_hex(hexstr)
    hs = sha256(data).hexdigest()
    last_bits = ''.join([str(bin(int(hs[i], 16))[2:].zfill(4)) for i in range(chars_for_checksum)])
    last_word_bin = f'{combo}{last_bits}'
    last_word_index = int(last_word_bin, 2)
    
    return bip39_words_list[last_word_index]

def checkSum(seed_list):
    bip39_words_list = get_bip39_words_list()

    seed_list = [word for word in seed_list if word]

    if len(seed_list) != 11 and len(seed_list) != 23:
        print(f'\nERROR: {len(seed_list)} words inserted\n')
        return

    # Check if all words are in bip39 list
    if not all(word in bip39_words_list for word in seed_list):
        for word in seed_list:
            if word not in bip39_words_list:
                print(f'\nERROR: word {word} not in bip39 words list\n')
        return

    # Find and print the first suggested word
    first_suggestion = find_first_suggestion(seed_list, bip39_words_list)
    return first_suggestion

# print(checkSum(["alpha", "between", "balance", "vacuum", "bullet", "panel", "kitchen", "concert", "toast", "balcony", "dog"]))
# )
# from hashlib import sha256
# import binascii
# import itertools


# def get_bip39_words_list():
#     lines = None
#     # downloaded from https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt
#     with open('./english.txt') as file:
#         lines = [line.rstrip() for line in file]
#     assert(len(lines) == 2048)
#     return lines


# def main():
#     bip39_words_list = get_bip39_words_list()

#     while True:
#         # try:
#         #     seed_string = input('Insert your first 11 or 23 words and press enter:\n').lower()
#         # except KeyboardInterrupt:
#         #     return

#         # convert string to list
#         # seed_list = seed_string.split(' ')
#         seed_list = ["alpha", "between", "balance", "cabin", "jelly", "sunny", "horror", "inhale", "diesel", "balcony", "dog"]
#         # remove eventual whitespaces in list
#         seed_list = [word for word in seed_list if word]

#         # check if all words are in bip39 list
#         all_words_in_bip39_list = True
#         for word in seed_list:
#             if word not in bip39_words_list:
#                 all_words_in_bip39_list = False
#                 print('\nERROR: word {} not in bip39 words list\n'.format(word))
        
#         # prevent going ahead if not all words in bip39 list
#         if not all_words_in_bip39_list:
#             continue

#         # check that words inserted must be 11 or 23
#         if len(seed_list) != 11 and len(seed_list) != 23:
#             print('\nERROR: {} words inserted\n'.format(len(seed_list)))
#             continue

#         break


#     bits_string = ''
#     for word in seed_list:
#         decimal_index = bip39_words_list.index(word)
#         binary_index = bin(decimal_index)[2:].zfill(11)
#         bits_string += binary_index

#     bits_to_add = None
#     chars_for_checksum = None
#     if len(seed_list) == 11:
#         bits_to_add = 7
#         chars_for_checksum = 1
#     elif len(seed_list) == 23:
#         bits_to_add = 3
#         chars_for_checksum = 2
    
#     combos = itertools.product(['0', '1'], repeat=bits_to_add)
#     combos = [ ''.join(list(i)) for i in combos]
#     combos = sorted(combos, key=lambda x: int(x, 2))
    
#     candidates = '\n\nMISSING BITS - WORD:\n'
#     for combo in combos:
#         entropy = '{}{}'.format(bits_string, combo)
#         hexstr = "{0:0>4X}".format(int(entropy,2)).zfill(int(len(entropy)/4))
#         data = binascii.a2b_hex(hexstr)
#         hs = sha256(data).hexdigest()
#         last_bits = ''.join([ str(bin(int(hs[i], 16))[2:].zfill(4)) for i in range(0, chars_for_checksum) ])
#         last_word_bin = '{}{}'.format(combo, last_bits)
#         candidates += '{} - {}\n'.format(combo, bip39_words_list[int(last_word_bin, 2)])

#     print(candidates)

# if __name__ == "__main__":
#     main()
