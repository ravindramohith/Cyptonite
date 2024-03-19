from simulator import Simulator  # Importing the Simulator class from simulator module
import sys  # Importing the sys module for command-line arguments

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
    )

    # Running the simulation
    simulator.simulate()

    # Printing the blockchain if "--print-blockchain" is in command-line arguments
    if "--print-blockchain" in sys.argv:
        simulator.print_blockchain()
        print("Blockchain written to file `blockchain.txt`")

    # Visualizing the blockchain if "--visualize-blockchain" is in command-line arguments
    if "--visualize-blockchain" in sys.argv:
        index = input("Enter the index of the node you want to visualize: ")
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
