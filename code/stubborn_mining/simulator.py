from graph import generate_connected_graph
import heapq, random
import numpy as np
from peer import Peer, Node
from event import Event, EventPriorityQueue


class Simulator:
    def __init__(
        self,
        n,
        z0,
        z1,
        min_transactions_per_mining=3,
        transaction_mean_gap=15,
        max_events=100,
    ):
        """
        Initialize a Simulator object.

        Parameters:
        - n: Number of nodes in the network.
        - z0: Parameter for generating speeds.
        - z1: Parameter for generating CPU speeds.
        - min_transactions_per_mining: Minimum number of transactions required to mine a block.
        - transaction_mean_gap: Mean time gap between transactions.
        - max_events: Maximum number of events to simulate.
        """
        self.peers = []
        self.nodes = []
        self.min_transactions_per_mining = min_transactions_per_mining
        self.transaction_mean_gap = transaction_mean_gap
        self.graph = generate_connected_graph(n)
        speeds = self.generate_array_random(n, z0)
        CPU_speeds = self.generate_array_random(n, z1)
        self.h = 1 / (n + 9 * sum(CPU_speeds))

        # Initialize nodes and peers
        for i in range(n):
            node = Node(
                i, speeds[i], CPU_speeds[i], self.min_transactions_per_mining, self
            )
            self.nodes.append(node)
            self.peers.append(Peer(node, n, self))

        # Connect peers in the network
        self.connect_peers()

        # Initialize latencies matrix
        self.latencies = [[0 for _ in range(n)] for _ in range(n)]
        self.longest_chains = [
            node.blockchain.get_longest_chain() for node in self.nodes
        ]

        # Generate latencies matrix
        for i in range(n):
            for j in range(n):
                if i != j:
                    ij = np.random.uniform(10, 500)
                    cij = 100 if (self.nodes[i].speed and self.nodes[j].speed) else 5
                    dij = np.random.exponential(96 / cij)
                    self.latencies[i][j] = ij + dij
                else:
                    self.latencies[i][j] = 0

        # Initialize priority queue and generate initial transactions
        self.priority_queue = EventPriorityQueue()
        self.generate_transactions_init()
        self.max_events = max_events

    def generate_array_random(self, n, z):
        """Generate a random array of length n with z proportion of ones."""
        num_ones = int(n * z)
        num_zeros = n - num_ones
        array = [1] * num_ones + [0] * num_zeros
        random.shuffle(array)
        return array

    def simulate(self):
        """Simulate the events in the network."""
        for i in range(self.max_events):
            self.event_handler()

    def connect_peers(self):
        """Connect peers in the network based on the generated graph."""
        for i, row in enumerate(self.graph):
            for j, connected in enumerate(row):
                if j <= i:
                    continue
                if connected:
                    self.peers[i].connect_to_peer(self.peers[j])
                    self.nodes[i].add_peer(self.peers[j])
                    self.peers[j].connect_to_peer(self.peers[i])
                    self.nodes[j].add_peer(self.peers[i])

    def generate_transactions_init(self):
        """Generate initial transactions for all peers."""
        for peer in self.peers:
            event = Event(peer, "generate_transactions", {"time": 0}, 0)
            self.priority_queue.push(event)

    def get_latency(self, i, j, messg_size=1):
        """Calculate the latency between two nodes."""
        cij = 100 if (self.nodes[i].speed and self.nodes[j].speed) else 5
        return self.latencies[i][j] + messg_size / cij

    def event_handler(self):
        """Handle the events in the priority queue."""
        if not self.priority_queue.is_empty():
            event = self.priority_queue.pop()
            if event.function == "receive_block":
                index = self.peers.index(event.object)
                longest_chain_before = event.object.node.blockchain.get_longest_chain()
                if hasattr(event.object, event.function):
                    method = getattr(event.object, event.function)
                    if event.params is not None:
                        method(**event.params)
                    else:
                        method()
                longest_chain_after = event.object.node.blockchain.get_longest_chain()
                self.longest_chains[index] = longest_chain_after
                Tk = np.random.exponential(
                    self.nodes[index].avg_time / 10 * self.h
                    if self.nodes[index].CPU_speed == 1
                    else self.h
                )
                if longest_chain_before != longest_chain_after[:-1]:
                    self.priority_queue.push(
                        Event(
                            self.nodes[index],
                            "conditional_mine_block",
                            {
                                "prev_longest_chain": longest_chain_after,
                                "time": event.time + Tk,
                            },
                            event.time + Tk,
                        )
                    )
                    pass
            else:
                if hasattr(event.object, event.function):
                    method = getattr(event.object, event.function)
                    if event.params is not None:
                        method(**event.params)
                    else:
                        method()
        else:
            print("Events are empty")

    def is_proper_prefix(self, list1, list2):
        """Check if list1 is a proper prefix of list2."""
        if len(list1) < len(list2):
            return all(list1[i] == list2[i] for i in range(len(list1)))
        else:
            return False

    def print_blockchain(self):
        """Print the blockchain of each node to a file."""
        with open("blockchain.txt", "w") as file:
            for node in self.nodes:
                file.write(f"Node {node.id} Blockchain:\n")
                for block in node.blockchain.blocks:
                    file.write("Block ID: " + str(block.block_id) + "\n")
                    file.write(
                        "Previous Block ID: " + str(block.previous_block_id) + "\n"
                    )
                    file.write("Transactions:\n")
                    for txn in block.transactions:
                        file.write(str(txn) + "\n")
                    file.write("\n")

    def visualize(self):
        """Visualize the blockchain of each node."""
        for node in self.nodes:
            node.blockchain.visualize(node.id)
