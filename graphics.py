import matplotlib.pyplot as plt
import re

def sample():
    #sampled queue's lenght
    for line in sim_data[5:]:
        line = line.split(" ")
        #frist queue's lenght in line[9]
        insert(line[9:]) #insert sampled queue's lenght in a list of dictionaries

def insert(sample):
    #create a new dict
    samp_dict = dict()
    #for each queue
    for i in sample:
        i = re.findall(r'\d+', i)
        #increment the number of queues that reach that length
        for j in range(int(i[0])+1):
            if j in samp_dict:
                samp_dict[j] += 1
            else:
                samp_dict[j] = 1
    #turn the number of queues that reach that length into a percentage
    samp_dict = {k: v/n for k, v in samp_dict.items()}
    percentage.append(samp_dict)

def average(final_dict):
    #average of the queues' lenght
    for d in percentage:
        for k, v in d.items():
            if k in final_dict:
                final_dict[k] += v
            else:
                final_dict[k] = v
    final_dict = {k: v/len(percentage) for k, v in final_dict.items()}
    return final_dict

#Main
colour = ['b', 'r', 'darkorange', 'gold', 'g']
for lambd in ["0.5", "0.9", "0.95", "0.99"]:
    with open("out.txt_"+lambd, 'r') as file:
        #simulation data
        sim_data = file.readlines(0)
        sim_metadata = sim_data[0].split(" ")
        n = int(sim_metadata[5])
        
        percentage = []
        sample()
        
    final_dict = dict()
    final_dict = average(final_dict)

    #print("\n\n\n", final_dict)
    plt.plot(final_dict.keys(), final_dict.values(), colour.pop(), label="lambda = "+ lambd)

title = sim_data[0].split(" ")
plt.title(title[14] + " choice")
plt.legend(loc = "upper right")
plt.xlabel('Queue length')
plt.ylabel('Fraction of queues with at least that size')
plt.xlim(0, 14)
lenght_tiks = [0, 2, 4, 6, 8, 10, 12 ,14]
percentage_tiks = [0, 0.2, 0.4, 0.6, 0.8, 1]
plt.xticks(lenght_tiks)
plt.yticks(percentage_tiks)
plt.show()
