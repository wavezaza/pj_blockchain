from flask import render_template , jsonify ,request
from app import app

from contract.static import static
from contract.helper import helper

helper = helper()
@app.route('/')
def index():
    accounts_pair = helper.pairAddressPrivateK()
    return render_template('index.html', accounts_pair=accounts_pair)
#get
@app.route('/accounts', methods=['GET'])
def accounts():
    data = helper.get_accounts()
    return jsonify(data)

# @app.route('/get_all_transactions', methods=['GET'])
# def get_all_transactions():
#     data = helper.get_all_transactions()
#     return jsonify(data)

@app.route('/get_all', methods=['GET'])
def get_all():
    data = helper.get_all()
    return jsonify(data), 200


#Post
@app.route('/balance', methods=['POST'])
def balance():
    address = request.get_json()
    data = helper.get_balance(address['address'])
    balance_data = {
        'wei': str(data['wei']),
        'ether': str(data['ether'])
    }
    return jsonify(balance_data)

@app.route('/send', methods=['POST'])
def send():
    req = request.get_json()
    sender_private_key = req['sender_private_key']
    sender_address = req['sender_address']
    receiver_address = req['receiver_address']
    amount = int(req['amount'])
    if int(amount) > helper.get_balance(sender_address)['ether']:
        return jsonify({'error': 'true', 'message': 'Not enough balance'})
    result = static(sender_private_key, sender_address, receiver_address, amount).send()
    return jsonify({'error': 'false', 'message': 'Transaction Complete'})