import uuid
from flask import Flask, jsonify, request, render_template_string
from network import SimpleBlockchain
from explorer import EXPLORER_HTML

app = Flask(__name__)

# Generate a globally unique address for this node instance
node_identifier = str(uuid.uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = SimpleBlockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing values'}), 400

    index = blockchain.new_transaction(
        values['sender'], 
        values['recipient'], 
        values['amount'], 
        values['signature']
    )
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['POST'])
def mine():
    last_block = blockchain.last_block
    nonce = blockchain.proof_of_work(last_block, difficulty=2)
    
    block = blockchain.new_block(previous_hash=None, nonce=nonce)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash'],
        'hash': block['hash']
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None or not isinstance(nodes, list):
        return jsonify({'message': 'Error: Please supply a valid list of nodes'}), 400

    try:
        blockchain.nodes.register_many(nodes)
    except ValueError as exc:
        return jsonify({'message': str(exc)}), 400

    response = {
        'message': 'New nodes have been added',
        'total_nodes': blockchain.nodes.list_nodes(),
    }
    return jsonify(response), 201

@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        'nodes': blockchain.nodes.list_nodes()
    }
    return jsonify(response), 200

@app.route('/explorer', methods=['GET'])
def explorer():
    """Minimal Explorer HTML view showing recent blocks and mempool."""
    return render_template_string(EXPLORER_HTML, chain=blockchain.chain, mempool=blockchain.mempool)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)