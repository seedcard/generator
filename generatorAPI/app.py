from flask import Flask, request, jsonify, abort
from generatorAPI.seedcard import generate_random_number,sparrow_same, compute_fingerprint, checkSum, generate_new_walletx, format_number, split_into_chunks, sha256_hash, get_bip39_words, generate_xpub, create_qr_code_flask
import base64
from io import BytesIO
from PIL import Image
import random
from flask_cors import CORS, cross_origin
from flask import Response
from generatorAPI.generate import generate_new_wallet

app = Flask(__name__)
CORS(app)

def pil_image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# def check_authentication():
#     auth = request.headers.get("Authorization")
#     if auth is None or auth == "":
#         abort(401, description="Unauthorized Access")

# Declaring middleware before proceeding in an application
# @app.before_request
# def before_request():
#     headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
#     if request.method == 'OPTIONS' or request.method == 'options': return jsonify(headers), 200
#     if request.endpoint != "login":
#         check_authentication()

# Defining an API endpoint
@app.route("/xpub", methods=["GET", 'OPTIONS', 'options'])
@cross_origin()
def xpub_request():
    random_number = generate_random_number()
    hex_format, bin_format = format_number(random_number)
    bin_chunks = split_into_chunks(bin_format)
    hex_hash, bin_hash = sha256_hash(bin_format)
    wordsx, concatenated_indices = get_bip39_words(bin_chunks)
    xpub, bip44_acc, seed_phrase = generate_xpub(wordsx)
    img = create_qr_code_flask(xpub, filename="xpub_qr.png")

    # Convert image to base64 string
    img_base64 = pil_image_to_base64(img)
    return jsonify({"img_xpub": img_base64, "words": wordsx})

# Generate a new wallet
@app.route("/generatewallet", methods=['POST', 'OPTIONS'])
def generate_wallet():
    if request.method == 'OPTIONS':
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        words = data["words"]
        print({"words": words})
        word_reserve = ["alpha", "between", "balance","balcony", "dog"]
        new_wallet_words, new_wallet_hex = generate_new_walletx(words)
        check_word_new_wallet = checkSum(new_wallet_words[:-1])
        new_wallet_words[-1] = check_word_new_wallet
        # Compute and display the fingerprint for the first new wallet
        new_wallet_fingerprint1 = compute_fingerprint(' '.join(new_wallet_words))
        sparrow_same.extend(new_wallet_words[3:9])
        sparrow_words = word_reserve[:3] + sparrow_same + word_reserve[3:]
        sparrow_same.clear()
        # print(sparrow_words)
        check_word = checkSum(sparrow_words)
        sparrow_words.append(check_word)
        print({"sparroe words": sparrow_words})
        concatenated_indices = generate_new_wallet(sparrow_words)

        img = create_qr_code_flask(concatenated_indices)
        # Compute and display the fingerprint for the new wallet
        new_wallet_fingerprint2 = compute_fingerprint(' '.join(sparrow_words))
        
        # Convert image to base64 string
        img_base64 = pil_image_to_base64(img)
        return jsonify({"img_newallet": img_base64, "fingerprint1": new_wallet_fingerprint1, "fingerprint2": new_wallet_fingerprint2})

def _build_cors_prelight_response():
    response = jsonify({'message': 'CORS preflight successful'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
    return response
# RANDOMISATION 
@app.route("/randomise", methods=["POST"])
def randomise():
    data = request.get_json()
    words = data["words"]
    # hidden_words = [words[0][i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
    hidden_words = [words[i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
    original_positions = [1, 2, 3, 10, 11, 12]  # Their original positions
    # Create a map of hidden words to their original positions (1-based index)
    # hidden_word_map = {words[0][i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
    hidden_word_map = {words[i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
    random.shuffle(hidden_words)
    result = ''.join([s for s in hidden_words if s.strip()])
    # Saving the randomization pattern
    randomization_pattern = [hidden_word_map[word] for word in hidden_words]
    randompattern = " / ".join(map(str, randomization_pattern))

    return jsonify({"msg": randompattern, "hidden_words": result})

# Creating wallet name qr code
@app.route("/walletname_qr", methods=["POST"])
def generate_wallet_name_qr():
    # receiving wallet name
    data = request.get_json()
    wallet_name = data["wallet_name"]
    if len(wallet_name) != 16:
        return jsonify({"err": "wallet name should 16 characters"}), 403
    
    if wallet_name:
        img = create_qr_code_flask(wallet_name, filename="wallet_name_qr.png")
        # Convert image to base64 string
        img_base64 = pil_image_to_base64(img)
        return jsonify({"img_walletnme": img_base64}), 200
    # Do something with the data
    return jsonify({"err": "Please enter a wallet name of 16 character"}), 403

if __name__ == '__main__':
    app.run(debug=True)