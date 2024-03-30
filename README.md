# CS 765 Assigment-2

## **Environment:**
Make sure python v3 is installed on your system.

## **Running instructions:**
- Navigate to code directory:

`$ cd code/`

### **For stuborn mining without any attacker:** navigate to `stubborn_mining` directory.
### **For mining with attackers:** navigate to `selfish_mining` directory.

- basic command to run event simulator:

`$ python3 main.py --peers [PEERS] --z0 [Z0] --z1 [Z1] --transaction-mean-gap [TRANSATIONMEANGAP] --att1 [ATT1] --att2 [ATT2]`

- for printing blockchain:

`$ python3 main.py --peers [PEERS] --z0 [Z0] --z1 [Z1] --transaction-mean-gap [TRANSATIONMEANGAP] --att1 [ATT1] --att2 [ATT2] --print-blockchain`

- for visualizing the blockchain:

`$ python3 main.py --peers [PEERS] --z0 [Z0] --z1 [Z1] --transaction-mean-gap [TRANSATIONMEANGAP] --att1 [ATT1] --att2 [ATT2] --visualize-blockchain` 

**Note: If u want to print and visualize, add both `--print-blockchain` and `--visualize-blockchain` flags to the basic command (order dosen't matter).

PEERS - No.of peers

Z0 - z0 fraction of low speed distribution

Z1 - z1 fraction of low CPU speed distribution

TRANSACTIONMEANGAP - transaction mean time.

ATT1 - attacker 1's hashing power
ATT2 - attacker 2's hashing power

- to visualize graph of nodes:
    `$ python3 graph.py --generate`