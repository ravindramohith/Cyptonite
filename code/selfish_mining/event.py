import heapq


class Event:
    def __init__(self, object, function, params, time):
        """
        Initialize an Event object.

        Parameters:
        - object: The object associated with the event.
        - function: The function to be called when the event occurs.
        - params: Parameters to be passed to the function.
        - time: The time at which the event occurs.
        """
        self.object = object
        self.function = function
        self.params = params
        self.time = time

    def __lt__(self, other):
        """Define less than comparison based on event time."""
        return self.time < other.time

    def __eq__(self, other):
        """Define equality comparison based on event time."""
        return self.time == other.time

    def __gt__(self, other):
        """Define greater than comparison based on event time."""
        return self.time > other.time

    def __le__(self, other):
        """Define less than or equal comparison based on event time."""
        return self.time <= other.time

    def __ge__(self, other):
        """Define greater than or equal comparison based on event time."""
        return self.time >= other.times

    def __str__(self) -> str:
        """Return a string representation of the event."""
        return f"Object: {self.object}, Function: {self.function}, Params: {self.params}, Time: {self.time}"


class EventPriorityQueue:
    def __init__(self):
        """Initialize an empty priority queue for events."""
        self._queue = []

    def push(self, event):
        """Push an event into the priority queue."""
        heapq.heappush(self._queue, event)

    def pop(self):
        """Pop the event with the smallest time from the priority queue."""
        return heapq.heappop(self._queue)

    def peek(self):
        """Return the event with the smallest time without removing it from the priority queue."""
        return self._queue[0] if self._queue else None

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self._queue) == 0
