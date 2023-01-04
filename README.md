#### How to use:

- for executing and generating graphics: `make all d='value'`
- for generating only graphics: `make graphics`
- for executing storage: `make storage`
- for deleting output files: `make clean`

# Report DC Lab: Queueing and Scheduling
## Part 1
### Purpose of the project <br>
In this part of the project we were asked to complete a simulation of a M/M/1 FIFO, extend it
to a M/M/n and compare our results with the theoretical ones. M/M/1 in the Kendall notation
(the standard system used to describe and classify a queueing node) means that:
* Jobs arrive and are served in a Memoryless fashion (exponential inter-arrival times),
  that means that our queue is a sequence of possible events in which the probability
  of each one to arrive or to be served in a time unit never changes.</li>
* There is only 1 server in the system.
  The final implementation will simulate a distributed system with n servers instead of just one
  and a load balancer that uses the Supermarket queuing model.</li>

The final implementation will simulate a distributed system with n servers instead of just one
and a load balancer that uses the Supermarket queuing model.
#### Supermarket model <br>
The supermarket model refers to a system with a large number of queues, where arriving
jobs are sorted into the emptiest queue among d randomly chosen each time.
The fraction of queues with at least i jobs drops from $λ^i$ to $λ^{\frac{d^i-1}{d-1}}$
### How does it work
Our simulation requires 6 parameters:
* λ: is the average frequency at which jobs join the system
* μ: is the average frequency at which jobs are served
* max-t: defines the life time of our simulation (it refers to the simulated execution time)
* n: defines the number of servers that our system will provide
* d: number of servers consulted by supermarket model, this value must be between 1
and n.
* csv: file path that refers to a txt file that will act as log file (optional)
#### Simulation Class
The core of this simulation is the Simulation class: it represents the simulation state.
Its constructor initialises the value t, that will represent the time in the simulation and a
queue that will contain all the Events. During the execution each event contained in the
queue will be extracted and executed.
#### MMN Class
In order to execute a simulation with our data we must extend Simulation. To achieve this
goal we instantiate MMN, a subclass of Simulation that contains new properties and
methods:<br>
In its properties are included our simulation parameter (λ, μ, n and d) and various structures
useful in jobs (events) management. This class also contains our supermarket(...) method,
this method is called when a new job arrives, it computes the length of d queues randomly
chosen and inserts the arriving job into the "emptiest" one.
#### Event Class
Each job is represented by an instance of one Event’s subclass.<br>
Events is an abstract class that contains the server ID on which a job is executed (or is
waiting for it to be executed) and a method process(...) that defines the event behaviour.
The method process(...) is not defined in this class, but it is defined in his subclasses.
In this part of the project we will use two of them, which are:
1. Arrival
2. Completion<br>

In the Arrival class the process(...) method records the moment of a job’s arrival, carries it
out, schedules its completion and generates a new arrival job. If the server is already
executing another job, the new arrival is added to its queue.<br>
<br>
In the Completion class the process(...) method records the completion time, if the queue of
the same server has one or more jobs within it one is removed and its completion is
scheduled, otherwise the server is put on hold.
### Results
We sampled the simulation’s state at regular intervals (referred to the simulation time t) while
running and saved samples in a file. We used the record of executions that have equal d to
plot a graph that shows how servers behave with different workloads.
In order to achieve different data from our simulations we run our code different times and
with different values.<br>
The first set of results that we are going to present were obtained setting n to 100 and max-t
to 10’000. We chose these values because we needed a high number of nodes in order to
compare our result with theoretical plots that reproduce the workload in a system with a
number of servers that tends towards infinity.
Afterwards we will present tests that show how the jobs’ time in the system decreases by
changing d. To run our simulation with a high value of max-t (100’000) we had to decrease
the number of servers values between 10 and 30 otherwise our PCs couldn't complete the
execution due to exhaustion of the available RAM memory.<br>
Also a lower value of max-t would generate noise by interrupting jobs too soon.
#### Comparison between our plots and the theoretical ones
All our graphs are almost identical to the theoretical ones.<br>
What you notice immediately is the difference in queue length depending on how many
servers the supermarket model has accessed.<br>
f we consider d = 1, the supermarket method will randomly choose one queue among the 'n'
in our system, which makes the probability of the worst case (always choosing the same
queue) higher. Because of that, with a high value of λ our system will be easily overloaded
by new entries. We can notice that in graphs with d equal to 1 (choice 1) we have the most
divergent results, caused by the ease of congestion of such a load balancer. We can also
notice that in this plot we have queues with the greatest number of jobs and even with a λ
equal to 0.5 we had at least one queue with fourteen or more jobs.<br>
<br>
With d = 2 the incoming jobs are scheduled on the emptiest queue of two randomly chosen
among the n of our system. We immediately notice how Supermarket model improves load
distribution, even with λ equal to 0.99 we never had a queue with length greater than 13.<br>
<br>
Queues are even more balanced with d = 5 and in particular with d = 10, we can see
significant improvements also with higher values of λ. This is due to the fact that the
Supermarket model takes into account the length of more queues, compared to the
execution with d = 2 and hence decreasing the possibility of overloading fewer servers,
leaving the rest with fewer tasks.<br>
We must take into account that our simulation does not consider the time needed for the
exchange of messages, we are only considering the positive aspects of increasing d.
# immagini
It could be interesting say a few words about some similarities in all plots:
* All plots start from 1: this has a pretty simple explanation, every queue with size 0
  is always full, and of course every queue has at least 0 element every time.
* In all cases, the fraction of queues with at least 1 job is λ:
  This “coincidence” is proved by Mitzematcher, he find out that the fraction of queues
  with at least i job is equal to: $$Mitzemacher: λ^{\frac{d^i-1}{d-1}}$$ In our case i is equal to 1, so $λ^{\frac{d^i-1}{d-1}}$
  is equal to λ. In addition we can obtain the same result with the “d=1” case, because if we chose randomly we have the fraction of queues with at least   1 job equal to λ , therefore in our case the result is always λ. 

During the tests we noticed a different behaviour with low value of n the workload of the
queues was much higher than we expected.
# image n = 10
In a real system there are some aspects which affect the workload that aren’t considered in
the theoretical values. In a structure composed of a “low” number of servers, the queues
length do not match the theoretical plot. We can still notice that queues’ length improves
incrementing d.
#### Comparison of system with different choice
In order to see how the Supermarket model improved our system we compared the average
time spent in the system of every job (W) with the theoretical expectation calculated by the
Little’s law, which represents a system that doesn’t use Supermarket but chooses queues
randomly.
$$Little's Low: W=\frac{1}{1-\lambda}$$
We can see how much Supermarket model affects the time spent by jobs in the system, the
greatest difference is observed between d equal to 1 (thus from a random load balancer)
and d equal to 2:<br>
<br>
  n: 10, d: 1, lambda: 0.5, mu: 1, max_t: 1000000, W: 2.000102636558352, Theoretical expectation: 2.0<br />
  n: 10, d: 1, lambda: 0.9, mu: 1, max_t: 1000000, W: 9.977195609851059, Theoretical expectation: 10.000000000000002<br />
  n: 10, d: 1, lambda: 0.95, mu: 1, max_t: 1000000, W: 20.080390667103952, Theoretical expectation: 19.999999999999982<br />
  n: 10, d: 1, lambda: 0.99, mu: 1, max_t:,1000000, W: 97.21159508029618, Theoretical expectation: 99.99999999999991<br />
  n: 10, d: 2 lambda: 0.5, mu: 1, max_t: 1000000, W: 1.352620161943183, Theoretical expectation: 2.0<br />
  n: 10, d: 2 lambda: 0.9, mu: 1, max_t: 1000000, W: 3.147716419057929, Theoretical expectation: 10.000000000000002<br />
  n: 10, d: 2 lambda: 0.95, mu: 1, max_t: 1000000, W: 4.595384699122842, Theoretical expectation: 19.999999999999982<br />
  n: 10, d: 2 lambda: 0.99, mu: 1, max_t: 1000000, W: 12.611703690277528, Theoretical expectation: 99.99999999999991<br />
  (if you want, we kept some other results in the file log.txt)<br>
<br>
From the results saved in the log file we notice that the variation of n does not affect W, this
happens because as the number of servers increases we also increase λ so that the
workload remains proportionate. Another interesting observation is that as the value λ gets
greater the improvement increases exponentially.
## Part 2
### Purpose of the project
In this part of the project we used the same structure that allowed us to run simulations
(Simulation and Event classes) to emulate distributed systems with different architectures
with the aim of storing and keeping information for a fixed amount of time, despite nodes
might have failures that cause data loss.
Our task was to complete the missing parts in the code in order to have a working simulation
that allows nodes to swap data with each other and recover data after failures.
The network structure is defined in a configuration file, which defines the type of different
nodes (e.g. peer, client, server) and some of their specifications, like:
* node type: a name for nodes that share the same customization
* number: how many nodes of this type are in the system.
* n : number of blocks in one node
* k : number of blocks where data are stored
* data_size: amount of data owned by the node
* storage_size: all the space designed to store data
* upload_speed: how many MiB per seconds can be sent
* download_speed: how many MiB per seconds can be received
* average_uptime: average time spent online
* average_downtime: average time spent offline
* average_lifetime: average time passed before a failure
* average_recover_time: average time needed to recover after a failure
* arrival_time: time spent before the node will come online for the first time

Nodes in our simulation will split their data into k blocks, then they will use the remaining
n − k blocks as parity blocks.
A low value of k allows a peer to recover its blocks even if it has few of them, e.g. with k
equal to 14 the peer needs at least 14 blocks to be able to recover all of the blocks that are
missing.
We tested our code with two configuration files, the first one describes a peer-to-peer
scenario, the second one describes a client-server architecture.
During this testing we changed the values in the files to test different systems and
distributions.
### How does it work
Like we said, the cores of this simulation are the Simulation and Event classes, this time the
class Simulation is extended by the class Backup.
Backup Class
This class adds to Simulation the property nodes, a list that contains all the nodes in our
system.
The constructor creates the first two events for each node: the first one will turn on the node
after the amount of time defined in arrival_time, the second will simulate a failure which will
occur at a random point in the life of the node.
Inside of the Backup class is also defined the method schedule_transfer(...) which allows the
peer to download and upload blocks to and from other peers.
#### Node Class
Each instance of this class represents the configuration of a given node, it contains the info
taken by the cfg file and it calculates others (such as block_size and free_space).
In this class there are also two important methods: schedule_next_upload(...) and
schedule_next_download(...).
Behind these two methods lies the logic according to which we find the blocks to transfer or
receive from other peers. We prioritise transfers that restore missing blocks.
#### NodeEvent Classes
NodeEvent is an abstract class that represents events related to nodes. For each different
event we have a different subclass:
* Online: turn online a offline node
* Offline: turn a running node offline
* Fail: simulate a node failure that causes the loss of all its local data
* Restore: recover a node from a failure
* Disconnection: make a node disconnect
#### TransferComplete Class
Event generated when a transfer is complete. It updates all the structures that simulate the
blocks’ storage. There are other two classes that specialise TransferComplete(...):
BlockBackupComplete(...) and BlockRestoreComplete(...) which respectively manage blocks
backups and restores.
### Extension
We noticed that the configuration file for the client-server architecture was provided with only
one client. We later figured out that this was the only way to simulate this kind of
architecture, preventing clients from backing up blocks on other clients and thus avoiding a
hybrid structure between client-server and peer to peer.
Our extension allows to use a new value in the cfg files: a list that identifies nodes that
should not be able to send messages to each other.
The control over where to backup is done at the time of its creation, more precisely in the
methods BlockBackupComplete(...) and BlockRestoreComplete(...).
### Results
We tried to execute our simulation by making some little changes in the configuration files,
the following data come from simulations of peer to peer structures.
Our histograms show how many blocks we lost in different executions. We decided to
comprehend all the n blocks instead of the k that contains relevant data, that's because we
think that even the loss of a parity block is relevant information to take into account.
#### Decreasing k:
By executing our simulation with the default values (n equal to 10, k equal to 8, a maximum
time of 100 years, etc.) we lose slightly more than half of the data on average.
# image  
If we decrease the value of k, peers are able to recover lost blocks more easily. For example
just decreasing k by one ( k equal to 7) the simulation ends with all the data in the majority of
cases, even if there are some cases where few blocks are lost.
# image
This happens because when we decrease k we increase the number of parity blocks and the
total redundancy:
Before we had 1GiB divided in 8 blocks and we had 2 parity blocks, that means that each
block contain 1GiB / 8 = 0. 125GiB , and the total amount of storage we need for 1GiB is
0. 125GiB * 10 = 1. 25GiB. <br>
Now we still have 1GiB, but it’s divided in 7 blocks and we have 3 parity blocks.
The amount of data stored in each blocks is 1GiB/7 $\simeq$ 0. 14GiB , and the amount of storage
we need for 1GiB is 0. 14GiB * 10 = 1. 4GiB .
This increase in redundancy allows us to tolerate multiple failures simultaneously, if we
consider M as the number of failures that we can manage it will be calculated as follows:
$$M = n−k$$
Thus, In our first case we were able to manage only two failures (simultaneously*), with k
equal to 7 M increases up to 3.<br>
*simultaneously: this term does not mean that the peers must be down at the same time but
that the effects of a failure (data loss) is still present, which means that a peer has not
recovered its data yet.
# image
#### Increasing n:
In order to increase redundancy we could also increment n . If we increase n by one we
would have 11 blocks of size: 1GiB / 8 = 0. 125GiB and a total amount of memory used
equal to 0. 125GiB * 11 = 1. 375GiB . Increasing n increases the redundancy of our data
and consequently the resistance to failures, similar to what we get by decreasing k.
# image
#### Decreasing max_t:
By decreasing the average execution time less blocks are lost; this is because a lower
execution time statistically reduces the average of concurrent possible failures.
Nevertheless, the number of lost blocks decreases only marginally. A situation where no
blocks are lost can only be achieved by setting max_t to the same value as the lifetime of
peers.
# image
#### Increasing/decreasing average_lifetime and average_downtime:
Increasing the average life of one peer increases the time interval in which a failure may
happen, this, in addition to decreasing the total number of peers failures during the
simulation, makes it less likely that more nodes fail at the same time and blocks to get lost.
# image
Offline nodes that haven’t failed do not result in a data loss, but a node that is looking for its
data may not receive a block for some time. If the "restoring” peer takes longer to recover all
its blocks, the risk that some of them could get lost in another failure before at least k are
recovered increases.
Another way to obtain a similar result is to decrease the time spent offline of the nodes.
# image
#### Increasing/decreasing average_recover_time:
As for the average_down_time, reducing the average_recover_time the risk that some of the
blocks get lost in another failure before at least k are recovered increases.
# image
#### ncreasing/decreasing connection speed:
By changing the upload/download speed of the peers we change the time required to
resolve the data loss caused by a failure, higher is the speed, more likely they are able to
recover a block from another peer before its own failure.
# image
Unfortunately, cases in which this improvement actually prevents data loss are very rare.
Even if failures in different nodes occurred in a short time are less likely seen as concurrent,
the majority of the block loss is caused by simultaneous failures.
Therefore, we don't think improving the network speed is the best way to increase fault
tolerance.
### Client Server
We replicated the same tests on client server architecture. We observed that changing the
values in the cfg lead to performance improvements similar to the peer to peer architecture,
for some values the impact of changes may differ, but the number of lost blocks increase or
decrease for the same reason.<br><br>
An interesting comparison could be the one made between the given client server
configuration (that is a hybrid structure) and our configuration (straight client server
structure).
### Straight
# image
This three graph shows the percentage of blocks lost in the straight configuration with
different clients and 10 servers. They seem to indicate a greater percentage of lost blocks.
We think that increasing the number of clients leads to more blocks lost because with more
clients that can have a failure more upload/download are needed, slowing the network.
This increases the time required by a node to recover all blocks after a failure.<br>
What happens if we increase the number of servers instead?
# image
If we increase the number of servers the system will lose less blocks, this happens because
each block has one backup and each server can hold only one backup for each client.
Having 10 blocks and 10 servers, when a server fails, the client will remain without a backup
until the failure is resolved. With multiple servers the client is able to create a new backup as
soon as it realises that the crashed server has lost its data.
#### Hybrid
# image
Even if the structure is different, the behaviour is very similar with the values we used.
The test where we increased the number of servers, since it was done with only one client,
didn't show any difference.
# image
### Comparison
[DEFAULT]<br>
average_lifetime = 1 year<br>
arrival_time = 0<br>
[client]<br>
number = 10<br>
n = 3<br>
k = 2<br>
data_size = 1 GiB<br>
storage_size = 2 GiB<br>
upload_speed = 500 KiB<br>
download_speed = 2 MiB<br>
average_uptime = 8 hours<br>
average_downtime = 16 hours<br>
average_recover_time = 3 days<br>
without_access = ['client']<br>
[server]<br>
number = 3<br>
n = 0<br>
k = 0<br>
data_size = 0 GiB<br>
storage_size = 1 TiB<br>
upload_speed = 100 MiB<br>
download_speed = 100 MiB<br>
average_uptime = 30 days<br>
average_downtime = 2 hours<br>
average_recover_time = 1 day<br>
without_access = []<br>
<br>
We used these parameters for the straight client server architecture, this graph has a lower
block loss compared to the hybrid architecture. That’s because the parameters of the
servers are "better" than those of the clients, storing the backups on them ensures greater
security.
An advantage of the hybrid version, however, is the amount of additional space, the
simulation of this architecture has been simulated with only one server instead of 3. The
hybrid solution would therefore lead to a better savings in server management while having
less fault-toleration.
## Noise in results
To evaluate the performance of our simulations, we counted the blocks that were lost at the
end of the execution. This method contains noise caused by the fact that not all of the lost
blocks contained the original data but some were parity blocks. This noise turns out to be
homogeneous and therefore not relevant when we compare executions with the same
values of n and k, when instead these values change it must be kept in mind that there may
be differences in the results based on the difference of the values n and k in the two
performances evaluated.
