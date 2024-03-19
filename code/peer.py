from blockchain import Blockchain
import numpy as np, random
from transaction import Transaction
from event import Event


class Node:
    def __init__(
        self, id, speed, CPU_speed, min_transactions_per_mining, simulator=None
    ):
        """
        Initialize a Node object.

        Parameters:
        - id: Unique identifier for the node.
        - speed: Speed of the node in the network.
        - CPU_speed: CPU speed of the node.
        - min_transactions_per_mining: Minimum number of transactions required to mine a block.
        - simulator: Reference to the simulator object.
        """
        self.id = id
        self.speed = speed
        self.CPU_speed = CPU_speed
        self.blockchain = Blockchain()
        self.transaction_pool = []
        self.peers = []
        self.min_transactions_per_mining = min_transactions_per_mining
        self.simulator = simulator
        self.blocks_received = 0
        self.time_for_avg = 0
        self.avg_time = 0

    def __eq__(self, other):
        """Check equality between nodes based on their IDs."""
        return self.id == other.id

    def add_peer(self, peer):
        """Add a peer to the list of connected peers."""
        self.peers.append(peer)

    def check_if_exists_in_blockchain(self, block):
        """Check if a block exists in the node's blockchain."""
        for b in self.blockchain.blocks:
            if b == block:
                return True
        return False

    def receive_block(self, block, time):
        """
        Receive a block from a peer.

        Parameters:
        - block: Block received from the peer.
        - time: Time at which the block is received.
        """
        self.time_for_avg += time
        self.blocks_received += 1
        self.avg_time = self.time_for_avg / self.blocks_received
        if self.validate_block(block) and not self.check_if_exists_in_blockchain(block):
            for transaction in block.transactions:
                (
                    self.transaction_pool.remove(transaction)
                    if transaction in self.transaction_pool
                    else None
                )
            self.blockchain.add_block(block)
            self.simulator.priority_queue.push(
                Event(self, "propagate_block", {"block": block, "time": time}, time)
            )

    def receive_transaction(self, transaction, time):
        """
        Receive a transaction from a peer.

        Parameters:
        - transaction: Transaction received from the peer.
        - time: Time at which the transaction is received.
        """
        found = False
        for block in self.blockchain.blocks:
            if transaction in block.transactions:
                found = True
                break
        if not found:
            self.transaction_pool.append(transaction)

        # Automatically mine a block when the transaction pool reaches a size of 2
        time += 1
        if len(self.transaction_pool) >= self.min_transactions_per_mining:
            self.mine_block(time)

    def mine_block(self, time):
        """
        Mine a block with transactions from the transaction pool.

        Parameters:
        - time: Time at which the block is mined.
        """
        self.transaction_pool.append(
            Transaction(-1, self.id, 50, timestamp=time)
        )  # Add a reward transaction
        new_block = self.blockchain.create_block(self.transaction_pool, self.id)
        self.simulator.longest_chains[self.simulator.nodes.index(self)] = (
            self.blockchain.get_longest_chain()
        )
        self.simulator.priority_queue.push(
            Event(
                self,
                "propagate_block",
                {
                    "block": new_block,
                    "time": time,
                },
                time,
            )
        )
        self.transaction_pool = []  # Clear the transaction pool
        return new_block

    def conditional_mine_block(self, prev_longest_chain, time):
        """
        Mine a block conditionally based on the longest chain.

        Parameters:
        - prev_longest_chain: Previous longest chain.
        - time: Time at which the block is mined.
        """
        if self.simulator.is_proper_prefix(
            prev_longest_chain, self.blockchain.get_longest_chain()
        ):
            self.mine_block(time)

    def propagate_block(self, block, time):
        """
        Propagate a mined block to other nodes in the network.

        Parameters:
        - block: Block to be propagated.
        - time: Time at which the block is propagated.
        """
        for peer in self.peers:
            self.simulator.priority_queue.push(
                Event(
                    peer,
                    "receive_block",
                    {
                        "block": block,
                        "time": time
                        + self.simulator.get_latency(
                            self.id, peer.node.id, messg_size=len(block.transactions)
                        ),
                    },
                    time
                    + self.simulator.get_latency(
                        self.id, peer.node.id, messg_size=len(block.transactions)
                    ),
                )
            )

    def validate_block(self, block):
        """Validate a received block before adding it to the blockchain."""
        # Check if sender has sufficient balance
        for transaction in block.transactions:
            if transaction.sender != -1:
                sender_balance = self.get_balance(transaction.sender)
                if sender_balance < transaction.amount:
                    return False
        # For simplicity, assume all blocks are valid in this implementation
        return True

    def get_balance(self, account_id):
        """Get the balance of an account from the blockchain."""
        balance = 1200000
        for b in self.blockchain.blocks:
            for txn in b.transactions:
                if txn.sender == account_id:
                    balance -= txn.amount
                if txn.receiver == account_id:
                    balance += txn.amount
        return balance


class Peer:
    def __init__(self, node, n, simulator=None):
        """
        Initialize a Peer object.

        Parameters:
        - node: Reference to the associated node.
        - n: Total number of nodes in the network.
        - simulator: Reference to the simulator object.
        """
        self.node = node
        self.connections = []
        self.rel_transaction_timestamp = 0
        self.n = n
        self.simulator = simulator

    def __eq__(self, other) -> bool:
        """Check equality between peers based on their associated nodes."""
        return self.node.id == other.node.id

    def connect_to_peer(self, peer):
        """Establish a connection to another peer."""
        self.connections.append(peer)

    def generate_transactions(self, time):
        """
        Generate and broadcast a new transaction.

        Parameters:
        - time: Time at which the transaction is generated.
        """
        sender = self.node.id
        nodes = [i for i in range(self.n) if i != sender]
        receiver = random.choice(nodes)
        amount = random.randint(1, 50)
        transaction = Transaction(
            sender, receiver, amount, self.rel_transaction_timestamp
        )
        self.rel_transaction_timestamp += np.random.exponential(
            self.simulator.transaction_mean_gap
        )
        self.simulator.priority_queue.push(
            Event(
                self,
                "generate_transactions",
                {"time": self.rel_transaction_timestamp},
                self.rel_transaction_timestamp,
            )
        )
        self.simulator.priority_queue.push(
            Event(
                self,
                "broadcast_transaction",
                {"transaction": transaction, "time": self.rel_transaction_timestamp},
                self.rel_transaction_timestamp,
            )
        )

    def receive_block(self, block, time):
        """
        Receive a block from a peer.

        Parameters:
        - block: Block received from the peer.
        - time: Time at which the block is received.
        """
        self.node.receive_block(block, time)

    def receive_transaction(self, transaction, time):
        """
        Receive a transaction from a peer.

        Parameters:
        - transaction: Transaction received from the peer.
        - time: Time at which the transaction is received.
        """
        self.node.receive_transaction(transaction, time)

    def mine_block(self):
        """Mine a new block using the associated node's mining function."""
        return self.node.mine_block()

    def propagate_block(self, block, time):
        """
        Propagate a mined block to other peers.

        Parameters:
        - block: Block to be propagated.
        - time: Time at which the block is propagated.
        """
        for peer in self.connections:
            self.simulator.priority_queue.push(
                Event(peer, "receive_block", {"block": block, "time": time}, time)
            )

    def broadcast_transaction(self, transaction, time):
        """
        Broadcast a transaction to other peers.

        Parameters:
        - transaction: Transaction to be broadcasted.
        - time: Time at which the transaction is broadcasted.
        """
        for peer in self.connections:
            self.simulator.priority_queue.push(
                Event(
                    peer,
                    "receive_transaction",
                    {"transaction": transaction, "time": time},
                    time,
                )
            )
