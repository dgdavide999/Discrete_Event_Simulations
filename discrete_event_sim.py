import logging
import heapq
from multiprocessing import heap
# TODO: implement the event queue!
# suggestion: have a look at the heapq library (https://docs.python.org/dev/library/heapq.html)
# and in particular heappush and heappop

class Simulation:
    """Subclass this to represent the simulation state.

    Here, self is the simulated time and self.events is the event queue.
    """
                        
    def __init__(self):
        """
        Extend this method with the needed initialization.
        You can call super().__init__() there to call the code here.
        """

        self.t = 0  # simulated time
        self.events = []        # TODO: set up self.events as an empty queue
        self.sample_list = []   #list of queue lenght samples

    def schedule(self, delay, event):
        """Add an event to the event queue after the required delay."""
        heapq.heappush(self.events, (self.t + delay, event))   # TODO: add event to the queue at time self.t + delay

    def sampling(self):
        self.sample_list.append((self.t, self.queue_len(0)))

    def run(self, max_t=float('inf'), rate=int()):
        """Run the simulation. If max_t is specified, stop it at that time."""
        """manage"""
        last_sample_t = 0
        while self.events != [] :       # TODO: as long as the event queue is not empty:
            t, event = heapq.heappop(self.events)       # TODO: get the first event from the queue
            if t > max_t:
                break
            self.t = t
            event.process(self)
            if self.t - last_sample_t >= rate:
                last_sample_t = self.t
                self.sampling()

    def log_info(self, msg):
        logging.info(f'{self.t:.2f}: {msg}')


class Event:
    """
    Subclass this to represent your events.

    You may need to define __init__ to set up all the necessary information.
    """

    def __init__(self, server_id):
        self.server_id = server_id

    def process(self, sim):
        raise NotImplementedError
    
    def __lt__(self, other):
        return id(self) < id(other)