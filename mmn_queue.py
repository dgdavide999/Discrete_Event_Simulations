#!/usr/bin/env python

import argparse
import csv
import collections
import numpy as np
from random import expovariate, randint

from discrete_event_sim import Simulation, Event

# To use weibull variates, for a given set of parameter do something like
# from weibull import weibull_generator
# gen = weibull_generator(shape, mean)
#
# and then call gen() every time you need a random variable


class MMN(Simulation):

    def __init__(self, lambd, mu, n, d):

        # extend this to make it work for multiple queues
        # check if there is at least one server

        super().__init__()
        self.running = [] # if not None, the id of the running job
        self.queues = []
        self.arrivals = {}  # dictionary mapping job id to arrival time
        self.completions = {}  # dictionary mapping job id to completion time
        self.lambd = lambd  #probability of a new job entry
        self.n = n  #number of servers
        self.mu = mu    #probability of finishing a job
        self.arrival_rate = lambd * n
        self.completion_rate = mu
        self.d = int(round(n/100*d, 0))    #percentage of queues to be monitored
        if self.d == 0:
            self.d = 1
        for i in range(n):
            self.running.append(None)
            self.queues.append(collections.deque())  # FIFO queue of the system
            self.schedule(expovariate(lambd), Arrival(i, 0))   #first job

    def schedule_arrival(self, job_id): 
        # schedule the arrival following an exponential distribution, 
        # to compensate the number of queues the arrival time should depend also on "n"
        min_index = randint(0, self.n-1)
        min = self.queue_len(min_index)
        
        for i in range(self.d - 1): #searching for the empiest queue among the d monitored
            temp_index = randint(0, self.n-1)
            temp = self.queue_len(temp_index)
            if min > temp:
                min_index = temp_index

        self.schedule(expovariate(self.lambd), Arrival(min_index, job_id))

    def schedule_completion(self, server_id, job_id): #TODO find a way to remember the queue
        # schedule the time of the completion event
        self.schedule(expovariate(self.completion_rate), Completion(server_id, job_id))
        
    #@property
    def queue_len(self, server_id):
        return (self.running[server_id] is None) + len(self.queues[server_id])


class Arrival(Event):

    def __init__(self, server_id, job_id):
        super().__init__(server_id)
        self.id = job_id

    def process(self, sim: MMN):
        # set the arrival time of the job
        sim.arrivals[self.id] = sim.t
        # if there is no running job, assign the incoming one and schedule its completion
        if sim.running[self.server_id] is None:
            sim.running[self.server_id] = self.id
            sim.schedule_completion(self.server_id, self.id)
        # otherwise put the job into the queue
        else:
            sim.queues[self.server_id].append(self.id)
        # schedule the arrival of the next job (this is where we create jobs)
        sim.schedule_arrival(self.id + 1)

class Completion(Event):
    def __init__(self, server_id, job_id):
        super().__init__(server_id)
        self.id = job_id  # currently unused, might be useful when extending

    def process(self, sim: MMN):
        assert sim.running[self.server_id] is not None
        # set the completion time of the running job
        sim.completions[self.id] = sim.t
        # if the queue is not empty
        if len(sim.queues[self.server_id]) != 0:
            # get a job from the queue
            job = sim.queues[self.server_id].pop()
            # schedule its completion
            sim.schedule_completion(self.server_id, job)
        else:
            sim.running[self.server_id] = None

def main():
    #command line option
    parser = argparse.ArgumentParser()
    parser.add_argument('--lambd', type=float, default=0.7)
    parser.add_argument('--mu', type=float, default=1)
    parser.add_argument('--max-t', type=float, default=1_000_000)
    parser.add_argument('--n', type=int, default=10)
    parser.add_argument('--csv', help="CSV file in which to store results")
    parser.add_argument('--sample_rate', type=int, default=1000, help="queue lenght sampling rate based in simulation time")#queue lenght sampling
    parser.add_argument('--d', type=int, default=70, help="percentage of servers to be queried")
    args = parser.parse_args()
    assert args.d > 0 and args.d <= 100
    #initialization of MMN simulation
    sim = MMN(args.lambd, args.mu, args.n, args.d)
    sim.run(args.max_t, args.sample_rate)

    completions = sim.completions
    W = (sum(completions.values()) - sum(sim.arrivals[job_id] for job_id in completions)) / len(completions)
    print(f"Average time spent in the system: {W}")
    print(f"Theoretical expectation for random server choice: {1 / (1 - args.lambd)}")
    # lambda = 1 lead to an division by 0, lambda > 1 lead to a negative expectation

    #-------------------------------------------------------------------------------------------------#
    '''for t, leng in sim.sample_list:
        print("time: ", t , ",\tnumber of events in the queue " , leng)'''
    #-------------------------------------------------------------------------------------------------#
    
    if args.csv is not None:
        with open(args.csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([args.lambd, args.mu, args.max_t, W])


if __name__ == '__main__':
    main()