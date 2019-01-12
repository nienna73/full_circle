
import sys
import os
import subprocess

from operator import itemgetter
#
# frequency = sys.argv[1]
# duration = sys.argv[2]
#
# print("\nFrequency: " + str(frequency))
# print("Duration: " + str(duration) + "\n")
# os.system("for(int i=0;i<3;i++)); do echo hi & done")

path = "/home/ryan/watchfile"

# new_files = os.listdir(path)
new_files = subprocess.check_output((["ls", "-al", path]))
new_files = new_files.decode('utf-8')
new_files = new_files.splitlines()


filenames = []

for item in new_files:
    item = item.split()
    if len(item) > 2:
        entry = [item[7], item[8]]
        filenames.append(entry)
filenames = sorted(filenames, key=itemgetter(0))

for item in filenames:
    print(item)
