import requests
import time

f = open("requests.txt", "r")
f2 = open("output.txt", "a")

i = 0
apis = {'apikey': 'atpvGyxKcznNy'}

for line in f:
    start = time.time()
    r = requests.get(line, headers=apis)
    end = time.time()
    f2.write(str(i) + " " + r.text + '\n' + line + '\n' + str(r) + '\n' + str(end-start))
    print("Finished " + str(i) + "requests\n" + str(end-start))
    i = i + 1
