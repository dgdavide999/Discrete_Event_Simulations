import matplotlib.pyplot as plt
import pandas as p

document = "out.txt"
file = open(document, 'r')

first = file.readlines(0)
first = first[0].split(" ")

plt.title(first[0] + " " + first[1]+ " "+first[2])
plt.xlabel('queues lenght')
plt.ylabel('percentage fullness')

lenght = [0, 1, 2, 3, 4, 5]
percentage = [0, 0.2, 0.4, 0.6, 0.8, 1]
#plt.plot(lenght, percentage)
plt.xticks(lenght)
plt.yticks(percentage)
plt.show()