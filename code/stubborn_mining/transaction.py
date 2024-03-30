class Transaction:
    def __init__(self, sender, receiver, amount, timestamp=0):
        """
        Initialize a Transaction object.

        Parameters:
        - sender: ID of the sender.
        - receiver: ID of the receiver.
        - amount: Amount of coins being transferred.
        - timestamp: Timestamp of the transaction.
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

    def __str__(self) -> str:
        """
        Return a string representation of the transaction.
        """
        return f"TxnID: ID{self.sender} pays ID{self.receiver} {self.amount} coins"
