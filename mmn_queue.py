import argparse
import csv
import collections
from random import expovariate, randint
import datetime

from discrete_event_sim import Simulation, Event

# To use weibull variates, for a given set of parameter do something like
# from weibull import weibull_generator
# gen = weibull_generator(shape, mean)
#
# and then call gen() every time you need a random variable


class MMN(Simulation):

    def __init__(self, lambd, mu, n, d, sampling_rate):
        super().__init__()
        assert n > 0  # check if there is at least one server

        # data structures for Events
        self.running = []  # if not None, the id of the running job
        self.queues = []  # list of server queue
        self.arrivals = {}  # dictionary mapping job id to arrival time
        self.completions = {}  # dictionary mapping job id to completion time

        # simulation parameters
        self.lambd = lambd  # probability of a new job entry
        self.n = n  # number of servers
        self.mu = mu  # probability of finishing a job
        self.arrival_rate = lambd 
        self.completion_rate = mu
        self.d = d  # number of queues to be checked in supermarket

        # sampling data
        self.last_sample_t = 0
        self.sampling_rate = sampling_rate
        self.sample_list = []  # list of queue lenght samples

        for _ in range(n):
            self.running.append(None)
            self.queues.append(collections.deque())  # FIFO queue of the system
        self.schedule(expovariate(lambd * self.n), Arrival(0, 0))  # first job 
    

    def supermarket(self):
        min_index = randint(0, self.n-1)
        min = self.queue_len(min_index)

        for _ in range(self.d-1):  # searching for the empiest queue among the d monitored
            temp_index = randint(0, self.n-1)
            temp = self.queue_len(temp_index)
            if min > temp:
                min = temp
                min_index = temp_index
        return min_index


    def schedule_arrival(self, job_id):
        # schedule the arrival following an exponential distribution,
        # to compensate the number of queues the arrival time should depend also on "n
        self.schedule(expovariate(self.lambd * self.n), Arrival(self.supermarket(), job_id))

    # TODO find a way to remember the queue
    def schedule_completion(self, server_id, job_id):
        # schedule the time of the completion event
        self.schedule(expovariate(self.completion_rate), Completion(server_id, job_id))

    # @property
    def queue_len(self, server_id):
        return (self.running[server_id] is not None) + len(self.queues[server_id])

    def sampling(self):
        if self.t - self.last_sample_t < self.sampling_rate:
            return
        sample = []
        for i in range(self.n):
            sample.append(self.queue_len(i))
        self.sample_list.append([self.t, sample])
        


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
        sim.sampling()



class Completion(Event):
    def __init__(self, server_id, job_id):
        super().__init__(server_id)
        self.id = job_id

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
        sim.sampling()



def main():
    # command line option
    parser = argparse.ArgumentParser()
    parser.add_argument('--lambd', type=float, default=0.50)
    parser.add_argument('--mu', type=float, default=1)
    parser.add_argument('--max-t', type=float, default=1_000_000)
    parser.add_argument('--n', type=int, default=10)
    parser.add_argument('--csv', default="log.txt", help="CSV file in which to store results")
    parser.add_argument('--sample_rate', type=int, default=100, help="queue lenght sampling rate based in simulation time")  # queue lenght sampling
    parser.add_argument('--d', type=int, default=10, help="percentage of servers to be queried")
    args = parser.parse_args()
    assert args.d > 0 and args.d <= args.n
    
    # MMN simulation
    sim = MMN(args.lambd, args.mu, args.n, args.d, args.sample_rate)
    sim.run(args.max_t, args.sample_rate)
    completions = sim.completions
  
    # save simulation data and sampled queue's lenght in a file
    with open("out.txt_"+ str(args.lambd),'w+') as f:
        date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("Simulation:",date_time, "\tn =", args.n, "\tlambd =", args.lambd, "\tmu =", args.mu, "\td =", args.d, "\tmax_t =", args.max_t, "\n", file=f)
        
        W = (sum(completions.values()) - sum(sim.arrivals[job_id] for job_id in completions)) / len(completions)
        # WARNING: changing the format will mess up plot creation
        # space before \n make easier parsing
        print(f"Average time spent in the system: {W} ", file=f)
        print(f"Theoretical expectation for random server choice: {1 / (1 - args.lambd)} \n", file=f)
        
        for t, leng in sim.sample_list:
            print("time:", round(t, 0), " number of events in the queue", leng, file=f)
        print("\n\n", file=f)

    # save a log in a given file
    if args.csv is not None:
        with open(args.csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["n:",args.n,"d:",args.d,"lambda:",args.lambd, " mu:",args.mu, " max_t:",args.max_t, " W:",W, f" Theoretical expectation: {1 / (1 - args.lambd)}" ])
 

if __name__ == '__main__':
    main()