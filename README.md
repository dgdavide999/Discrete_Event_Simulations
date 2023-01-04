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
<ul>
  <li>Jobs arrive and are served in a Memoryless fashion (exponential inter-arrival times),
that means that our queue is a sequence of possible events in which the probability
of each one to arrive or to be served in a time unit never changes.</li>
  <li>There is only 1 server in the system.
The final implementation will simulate a distributed system with n servers instead of just one
and a load balancer that uses the Supermarket queuing model.</li>
</ul><br>
The final implementation will simulate a distributed system with n servers instead of just one
and a load balancer that uses the Supermarket queuing model.
#### Supermarket model <br>
The supermarket model refers to a system with a large number of queues, where arriving
jobs are sorted into the emptiest queue among d randomly chosen each time.
The fraction of queues with at least i jobs drops from $λ^i$ to $λ^{\frac{d^i-1}{d-1}}$
