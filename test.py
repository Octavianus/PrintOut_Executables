## Tool to list out all of the executables that ara available inside of the container, the informations listed inculding:
# 1. The name or UUID of the docker image that contains it.
# 2. The path to the executable.
# 3. THe SHA256 checksum of the executable.

## todo: List the output of the version flag if the tools has one.

import json
import subprocess
import sys
import hashlib
import os.path

# Open a file in advance, ready to write

# Command that list all the executables in the root dir
bashCmdFind = "sudo find / -type f -executable"
#bashCmdFind = "compgen -c"
processFind = subprocess.Popen(bashCmdFind, shell = True, stdout = subprocess.PIPE)
Jfile = open('executables_info.json','a+')
# (output, err) = process.communicate()
#The problem with above code is that output, err = p.communicate() will block next statement till ping is completed
# Out put the real time out put of the current available executables in a container.
while True:
	out = processFind.stdout.readline()
	# poll to know if the child prorcess has terminated.
	if out == '' and processFind.poll() != None:
		break;
	if out != '':
		filename = os.path.basename(out)
		tempHashValue = hashlib.sha256(filename)	
		shaHashValue = tempHashValue.hexdigest()	
		strpath = str(out)
		strsha256 = str(shaHashValue)
		aRow = [strpath.strip('\n'), strsha256]
		aRow = str(aRow) + '\n'
		# check the validation
		# print(aRow)
		Jfile.write(aRow)
		# Flush the stout buffer before next iteration.
		sys.stdout.flush()

