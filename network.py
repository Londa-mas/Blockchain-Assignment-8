import hashlib
import json
import time
from urllib.parse import urlparse

class NodeDirectory:
    """Manages peer node registrations and address normalisation."""
    def __init__(self):
        self.nodes = set()

    def register(self, address: str):
        self.nodes.add(normalise_address(address))

    def register_many(self, addresses: list):
        for address in addresses:
            self.register(address)

    def list_nodes(self) -> list:
        return sorted(list(self.nodes))


def normalise_address(address: str) -> str:
    """Normalises peer address scheme, host, and port."""
    address = address.strip().rstrip('/')
    parsed = urlparse(address if '://' in address else f'http://{address}')
    if parsed.scheme not in {'http', 'https'} or not parsed.hostname:
        raise ValueError(f'Invalid node address: {address}')
    host = parsed.hostname
    port = parsed.port
    if port:
        return f'{parsed.scheme}://{host}:{port}'
    return f'{parsed.scheme}://{host}'


class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.nodes = NodeDirectory()
        # Create the genesis block
        self.new_block(previous_hash="0" * 64, nonce=0)

    def new_block(self, previous_hash, nonce):
        block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.mempool,
            'nonce': nonce,
            'previous_hash': previous_hash or (self.chain[-1]['hash'] if self.chain else "0" * 64)
        }
        # Compute self-hash using canonical JSON
        block['hash'] = self.hash(block)
        self.mempool = []  # Clear mempool
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount, signature):
        tx = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature
        }
        self.mempool.append(tx)
        return len(self.chain)  # Returns index of the block that will hold this

    @staticmethod
    def hash(block):
        # Create a SHA-256 hash of a Block using canonical JSON serialization
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_block, difficulty=2):
        last_hash = self.hash(last_block)
        nonce = 0
        target = "0" * difficulty
        while True:
            guess = f"{last_hash}{nonce}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash.startswith(target):
                return nonce
            nonce += 1