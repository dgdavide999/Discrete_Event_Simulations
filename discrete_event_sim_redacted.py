from audioop import getsample
import logging
import heapq
from multiprocessing import heap
import threading
from threading import Thread
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
        self.stopSampling = False
        self.getSample = threading.Event()
        self.sampleList = []
        self.t = 0  # simulated time
        self.events:list[tuple[float, "Event"]] = []        # TODO: set up self.events as an empty queue

    def schedule(self, delay, event):
        """Add an event to the event queue after the required delay."""
        heapq.heappush(self.events, (self.t + delay, event))        # TODO: add event to the queue at time self.t + delay

    def sampling(self):
        while not self.stopSampling:
            self.getSample.wait()
            self.sampleList += [(self.t,len(self.events))]
            self.getSample.clear()

    def run(self, max_t=float('inf'), rate=int()):
        """Run the simulation. If max_t is specified, stop it at that time."""
        thread = Thread(target = self.sampling)
        thread.start()
        lastSampleT = 0;
        while self.events != [] :       # TODO: as long as the event queue is not empty:
            t, event = heapq.heappop(self.events)       # TODO: get the first event from the queue
            if t > max_t:
                break
            self.t = t
            event.process(self)
            if self.t - lastSampleT >= rate:
                self.getSample.set()

        self.stopSampling = True;
        thread.join()

    def log_info(self, msg):
        logging.info(f'{self.t:.2f}: {msg}')

 

class Event:
    """
    Subclass this to represent your events.

    You may need to define __init__ to set up all the necessary information.
    """

    def process(self, sim):
        raise NotImplementedError
    
    def __lt__(self, other):
        return id(self) < id(other)