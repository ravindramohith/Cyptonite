from simulator import Simulator  # Importing the Simulator class from simulator module
import sys  # Importing the sys module for command-line arguments
from graph import visualize_graph

# Main function
if __name__ == "__main__":
    # Creating an instance of Simulator with parameters extracted from command-line arguments
    simulator = Simulator(
        int(sys.argv[2]),  # Number of nodes
        float(sys.argv[4]),  # z0
        float(sys.argv[6]),  # z1
        min_transactions_per_mining=10,  # Minimum transactions per mining
        transaction_mean_gap=int(sys.argv[8]),  # Transaction mean gap
        max_events=10000,  # Maximum number of events
        attacker_hash1=0,  # Attacker 1 hashing power
        attacker_hash2=0,  # Attacker 2 hashing power
    )

    attacker_1 = simulator.att1
    attacker_2 = simulator.att2

    # Running the simulation
    simulator.simulate()

    # Printing the blockchain if "--print-blockchain" is in command-line arguments
    if "--print-blockchain" in sys.argv:
        simulator.print_blockchain()
        print("Blockchain written to file `blockchain.txt`")

    if "--visualize-graph" in sys.argv:
        visualize_graph(simulator.graph, att1=simulator.att1, att2=simulator.att2)

    # Visualizing the blockchain if "--visualize-blockchain" is in command-line arguments
    if "--visualize-blockchain" in sys.argv:
        while True:
            index = input("Enter the index of the node you want to visualize: ")
            if(index == "exit"):
                break
            if index.isdigit():
                index = int(index)
                # Checking if the entered index is within the range of nodes
                if index < len(simulator.nodes):
                    # Visualizing the blockchain of the specified node
                    simulator.nodes[index].blockchain.visualize(index)
                else:
                    print(
                        f"Invalid index. Index should be an integer from 0 to {int(sys.argv[2]) - 1}"
                    )
            else:
                print(
                    f"Invalid index. Index should be an integer from 0 to {int(sys.argv[2]) - 1}"
                )

    def find_block(block_id, blocks):
        for block in blocks:
            b = block.block_id
            if b == block_id:
                return block
        return None

    chain = simulator.nodes[0].blockchain.blocks
    atb1 = 0
    atb2 = 0
    tat1 = 0
    tat2 = 0
    tbl = 0
    tb = len(chain)
    longest_chain = []
    for block in chain:
        if block.miner_id == attacker_1:
            tat1 += 1
        if block.miner_id == attacker_2:
            tat2 += 1
        current_chain = [block]
        while current_chain[-1].previous_block_id is not None:
            prev_block = find_block(current_chain[-1].previous_block_id, chain)
            if prev_block:
                current_chain.append(prev_block)
            else:
                break
        if len(current_chain) > len(longest_chain):
            atb1 = 0
            atb2 = 0
            tbl = 0
            for block in current_chain:
                tbl += 1
                if block.miner_id == attacker_1:
                    atb1 += 1
                if block.miner_id == attacker_2:
                    atb2 += 1
            longest_chain = current_chain

    print(f"length of longest chain: {len(longest_chain)}, A1 {tat1}, A2 {tat2}")
    print(f"length of attacker 1 blocks: {atb1}", "MPU1(adv): ", atb1/tbl)
    print(f"length of attacker 2 blocks: {atb2}", "MPU2(adv): ", atb2/tbl)
    print(f"length of total blocks: {tb}", "MPU(total): ", tbl/tb)
