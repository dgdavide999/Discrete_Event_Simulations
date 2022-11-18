import matplotlib.pyplot as plt
import re

document = "out.txt"

def insert(sample):
    samp_dict = dict()
    for i in sample:
        i = re.findall(r'\d+', i)
        for j in range(int(i[0])+1):
            if j in samp_dict:
                samp_dict[j] += 1
            else:
                samp_dict[j] = 1
    samp_dict = {k: v/n for k, v in samp_dict.items()}
    percentage.append(samp_dict)
    #print(samp_dict)


try:
    file = open(document, 'r')
    #simulation data
    sim_data = file.readlines(0)
    sim_metadata = sim_data[0].split(" ")
    n = int(sim_metadata[5])
    W = sim_data[2].split(" ")
    W = W[6]
    expectation = sim_data[3].split(" ")
    expectation = expectation[6]

    
    #sampled queue's lenght
    percentage = []
    #sampling data
    #print(sim_data[5:])
    for line in sim_data[5:]:
        line = line.split(" ")
        insert(line[9:])
    #print(percentage)
    '''
    TODO: 
    1) create a dictionary 
    2) keys will be the queue lenght, values the number of time the lenght is reached
        2.1) lenght must be reached in just one queue or in all of them?
        2.2) if it's in one of them i have to consider all servers in probability
        2.2.1) example: sample 2, queue_len 2, only one server has length 2, so the probability
                        to have a full queue is 1 out of 10*2 (2 for the sampling, 10 for the number
                        of server for each sampling)
    2.9)from now on i act like i need just one server with the required lenght
    3)foreach sampling insert the number of server that reach the lenght
        3.1) we must keep trak about the number of samplings (we can write in sampling metadata or use a counter)
        3.2) if a server has lenght = 3, it will be marked like it has reached len 1,2 and 3
        3.3) maybe we should put a limit at queues lenght for this test:
                if we want to see how easily queues of lenght 2 takes to be filed
                we should't allow to have more than 2 job.
                (If the load balancer is optimized this point is irrelevant)
    4) divide all values of the dictionary for the total of possible outcomes (n of sampling * n of servers)
    5) plot the lenghts (keys) as x axis values, and their probability as y axis values 
    '''
except Exception as e:
    print(e)
finally:
    file.close()

final_dict = dict()
for d in percentage:
    for k, v in d.items():
        if k in final_dict:
            final_dict[k] += v
        else:
            final_dict[k] = v
final_dict = {k: v/len(percentage) for k, v in final_dict.items()}

print("\n\n\n", final_dict)

plt.title(sim_metadata[0] + " " + sim_metadata[1]+ " "+sim_metadata[2])
plt.xlabel('queues lenght')
plt.ylabel('percentage fullness')
plt.xlim(0, 14)

lenght_tiks = [0, 2, 4, 6, 8, 10, 12 ,14]
percentage_tiks = [0, 0.2, 0.4, 0.6, 0.8, 1]
plt.plot(final_dict.keys(), final_dict.values())
plt.xticks(lenght_tiks)
plt.yticks(percentage_tiks)
plt.show()