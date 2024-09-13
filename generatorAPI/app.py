# from flask import Flask, request, jsonify, abort
# from seedcard import create_qr_code, generate_random_number,sparrow_same, compute_fingerprint, checkSum, generate_new_walletx, format_number, split_into_chunks, sha256_hash, get_bip39_words, generate_xpub, create_qr_code_flask
# import base64
# from io import BytesIO
# from PIL import Image
# import random
# from flask_cors import CORS, cross_origin
# from flask import Response
# from generate import generate_new_wallet

# app = Flask(__name__)
# CORS(app)

# def pil_image_to_base64(img):
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
#     return img_str

# # def check_authentication():
# #     auth = request.headers.get("Authorization")
# #     if auth is None or auth == "":
# #         abort(401, description="Unauthorized Access")

# # Declaring middleware before proceeding in an application
# # @app.before_request
# # def before_request():
# #     headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
# #     if request.method == 'OPTIONS' or request.method == 'options': return jsonify(headers), 200
# #     if request.endpoint != "login":
# #         check_authentication()

# # Defining an API endpoint
# @app.route("/xpub", methods=["GET", 'OPTIONS', 'options'])
# @cross_origin()
# def xpub_request():
#     random_number = generate_random_number()
#     hex_format, bin_format = format_number(random_number)
#     bin_chunks = split_into_chunks(bin_format)
#     hex_hash, bin_hash = sha256_hash(bin_format)
#     wordsx, concatenated_indices = get_bip39_words(bin_chunks)
#     xpub, bip44_acc, seed_phrase = generate_xpub(wordsx)
#     img = create_qr_code_flask(xpub)

#     # Convert image to base64 string
#     img_base64 = pil_image_to_base64(img)
#     return jsonify({"img_xpub": img_base64, "words": wordsx})

# # Generate QR CODE
# @app.route("/generateqr", methods=['POST'])
# def generateqr():
#     data = request.get_json()
#     words = data["words"]
#     img = create_qr_code_flask(words)
#     # Convert image to base64 string
#     img_base64 = pil_image_to_base64(img)

#     return jsonify({"img_base64": img_base64})

# # Generate a new wallet
# @app.route("/generatewallet", methods=['POST', 'OPTIONS'])
# def generate_wallet():
#     if request.method == 'OPTIONS':
#         return _build_cors_prelight_response()
#     elif request.method == 'POST':
#         data = request.get_json()
#         print(data)
#         words = data["words"]
#         print({"words": words})
#         word_reserve = ["alpha", "between", "balance","balcony", "dog"]
#         new_wallet_words, new_wallet_hex = generate_new_walletx(words)
#         check_word_new_wallet = checkSum(new_wallet_words[:-1])
#         new_wallet_words[-1] = check_word_new_wallet
#         # Compute and display the fingerprint for the first new wallet
#         new_wallet_fingerprint1 = compute_fingerprint(' '.join(new_wallet_words))
#         # sparrow_same.extend(new_wallet_words[3:9])
#         sparrow_same.extend(words[3:9])
#         sparrow_words = word_reserve[:3] + sparrow_same + word_reserve[3:]
#         sparrow_same.clear()
#         # print(sparrow_words)
#         check_word = checkSum(sparrow_words)
#         sparrow_words.append(check_word)
#         print({"sparroe words": sparrow_words})
#         concatenated_indices = generate_new_wallet(sparrow_words)

#         # img = create_qr_code_flask(concatenated_indices)
#         img = create_qr_code_flask(concatenated_indices)
#         # Compute and display the fingerprint for the new wallet
#         new_wallet_fingerprint2 = compute_fingerprint(' '.join(sparrow_words))
        
#         # Convert image to base64 string
#         img_base64 = pil_image_to_base64(img)
#         return jsonify({"img_newallet": img_base64, "fingerprint1": new_wallet_fingerprint1, "fingerprint2": new_wallet_fingerprint2})

# def _build_cors_prelight_response():
#     response = jsonify({'message': 'CORS preflight successful'})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
#     return response

# # RANDOMISATION 
# @app.route("/randomise_qr", methods=["POST"])
# def randomise_qr():
#     data = request.get_json()
#     words = data["words"]
#     fingerprint1 = data["fingerprint1"]
#     cardissuer = data["cardissuer"]
     
#     # hidden_words = [words[0][i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
#     hidden_words = [words[i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
#     original_positions = [1, 2, 3, 10, 11, 12]  # Their original positions
#     # Create a map of hidden words to their original positions (1-based index)
#     # hidden_word_map = {words[0][i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
#     hidden_word_map = {words[i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
#     random.shuffle(hidden_words)
#     result = ''.join([s for s in hidden_words if s.strip()])
#     # Saving the randomization pattern
#     randomization_pattern = [hidden_word_map[word] for word in hidden_words]
#     randompattern = " / ".join(map(str, randomization_pattern))
    
#     # Generate randomisation qr code
#     randomise_qr_words = str(fingerprint1) + "_" + str(cardissuer) + "_" + str(result)
#     print({"randomise_qr_words": randomise_qr_words})

#     img = create_qr_code_flask(randomise_qr_words)
    
#     # Convert image to base64 string
#     img_base64 = pil_image_to_base64(img)
#     return jsonify({"msg": randompattern, "hidden_words": result, "img_randomised_qr_words": img_base64})

# # OP_RETURN 
# @app.route("/op_return", methods=["POST"])
# def op_return():
#     data = request.get_json()
#     fingerprint1 = data["fingerprint1"]
#     cardissuer = data["cardissuer"]
#     result = data["result"]
#     # Generate randomisation qr code
#     randomise_qr_words = str(fingerprint1) + "_" + str(cardissuer) + "_" + str(result)
#     print({"randomise_qr_words": randomise_qr_words})

#     img_qr_words = create_qr_code_flask(randomise_qr_words)
#     # Convert image to base64 string
#     img_qr_base64 = pil_image_to_base64(img_qr_words)
#     return jsonify({"img_qr_base64": img_qr_base64})

# # RANDOMISATION 
# @app.route("/randomise", methods=["POST"])
# def randomise():
#     randomised_words = []
#     data = request.get_json()
#     words = data["words"]
#     hashMap = {
#         1: "one",
#         2: "two",
#         3: "three",
#         10: "ten",
#         11: "elevator",
#         12: "twelve",
#     }
    
#     # hidden_words = [words[0][i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
#     hidden_words = [words[i] for i in [0, 1, 2, 9, 10, 11]]  # Words 1, 2, 3, 10, 11, 12
#     original_positions = [1, 2, 3, 10, 11, 12]  # Their original positions
#     # Create a map of hidden words to their original positions (1-based index)
#     # hidden_word_map = {words[0][i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
#     x = hidden_words
#     # print({"initial-hidden-words": hidden_words})
#     hidden_word_map = {words[i]: i + 1 for i in [0, 1, 2, 9, 10, 11]}
#     random.shuffle(hidden_words)
#     # print({"shuffle-hidden-words": hidden_words})
#     result = ''.join([s for s in hidden_words if s.strip()])
#     print({"result": result})
#     # Saving the randomization pattern
#     randomization_pattern = [hidden_word_map[word] for word in hidden_words]
#     # print({"randomisation-pattern": randomization_pattern})
#     randompattern = " / ".join(map(str, randomization_pattern))

#     for item in randomization_pattern:
#         randomised_words.append(hashMap[item])

#     # for idx, word in enumerate(hidden_words, start=1):
#     #     randomised_words.append(word)
    
#     # print({"randomised_words": randomised_words})
#     # Generate a new words and substitue the words variable with the new words
#     random_number = generate_random_number()
#     hex_format, bin_format = format_number(random_number)
#     bin_chunks = split_into_chunks(bin_format)
#     hex_hash, bin_hash = sha256_hash(bin_format)
#     wordsx, concatenated_indices = get_bip39_words(bin_chunks)

#     new_wallet_words, new_wallet_hex = generate_new_walletx(wordsx)
#     # check_word_new_wallet = checkSum(new_wallet_words[:-1])
#     # new_wallet_words[-1] = check_word_new_wallet
#     new_wallet_words_frm_randomisation = new_wallet_words[:3] + randomised_words + new_wallet_words[10:]
#     # randomised_words.clear()
#     check_word = checkSum(new_wallet_words_frm_randomisation)
#     new_wallet_words_frm_randomisation.append(check_word)
#     # print({"new_wallet_words_frm_randomisation": new_wallet_words_frm_randomisation})
#     concatenated_indices = generate_new_wallet(new_wallet_words_frm_randomisation)

#     img = create_qr_code_flask(concatenated_indices)
#     # Compute and display the fingerprint for the new wallet
#     new_wallet_randomise_fingerprint = compute_fingerprint(' '.join(new_wallet_words_frm_randomisation))

#     # Convert image to base64 string
#     img_base64 = pil_image_to_base64(img)
#     # return jsonify({"Initial-hidden-words": x, "shuffle-hidden-words": hidden_words, "randomisation-pattern": randomization_pattern, "randomised-words": randomised_words, "result": result})
#     return jsonify({"fingerprint": new_wallet_randomise_fingerprint, "msg": randompattern, "hidden_words": result, "img_randomised": img_base64 })

# # Creating wallet name qr code
# @app.route("/walletname_qr", methods=["POST"])
# def generate_wallet_name_qr():
#     # receiving wallet name
#     data = request.get_json()
#     wallet_name = data["wallet_name"]
#     if len(wallet_name) != 16:
#         return jsonify({"err": "wallet name should 16 characters"}), 403
    
#     if wallet_name:
#         img = create_qr_code_flask(wallet_name)
#         # Convert image to base64 string
#         img_base64 = pil_image_to_base64(img)
#         return jsonify({"img_walletnme": img_base64}), 200
#     # Do something with the data
#     return jsonify({"err": "Please enter a wallet name of 16 character"}), 403

# # Creating web page url qr code
# @app.route("/url_qr", methods=["POST"])
# def generate_url_qr():
#     # receiving url string
#     data = request.get_json()
#     url = data["url"]
#     if url:
#         img = create_qr_code_flask(url)
#         print(img)
#         # Convert image to base64 string
#         img_base64 = pil_image_to_base64(img)
#         return jsonify({"url_qr": img_base64}), 200
    
#     return jsonify({"err": "Please input a url"}), 403

# if __name__ == '__main__':
#     app.run(debug=True)