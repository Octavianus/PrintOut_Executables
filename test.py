## Tool to list out all of the executables that ara available inside of the container, the informations listed inculding:
# 1. The name or UUID of the docker image that contains it.
# 2. The path to the executable.
# 3. THe SHA256 checksum of the executable.

## todo: List the output of the version flag if the tools has one.
# The question to get the image ID and tag name within a container is posted on the docker help forum.

import json
import subprocess
import sys
import hashlib
import os.path

# Command that list all the executables in the root dir
bashCmdFind = "sudo find / -type f -executable"
#bashCmdFind = "compgen -c"
processFind = subprocess.Popen(bashCmdFind, shell = True, stdout = subprocess.PIPE)
# Open a file in advance, ready to write
Jfile = open('executables_info.json','a+')

# Set the global value
aRow = None
prevRow = None
prevPathName= None
rowBeginer = "{\"path\":{\"pathname\":"
rowMiddler = ",\"executables\":{\"SHA256checksum\":["
rowEnder = "]}}}"

## (output, err) = process.communicate()
#The problem with above code is that output, err = p.communicate() will block next statement till ping is completed
# Out put the real time out put of the current available executables in a container.
while True:
	out = processFind.stdout.readline()
	# poll to know if the child prorcess has terminated.
	if out == '' and processFind.poll() != None:
		# prevRow
		break;
	if out != '':
		## filename may be needed?
		filename = os.path.basename(out)
		tempHashValue = hashlib.sha256(filename)	
		shaHashValue = tempHashValue.hexdigest()	
		strpath = str(out)
		strsha256 = shaHashValue
		pathName = os.path.dirname(out)
		
		# If the previous pathname is the same as the currenct one, write the checksum of executable under this path in json format. 
		if prevPathName == pathName:
			# If this is the first executable in
			# if aRow == None:
				#aRow = rowBeginer + "\"" + pathName + "\"" + rowMiddler + "{\"value\":\"" + strsha256 + "\"}"
			#else:
			aRow += ",{\"value\":\"" + strsha256 + "\"}"
		else:	
			if aRow == None:
				aRow = rowBeginer + "\""+ pathName + "\"" + rowMiddler + "{\"value\":\"" + strsha256 + "\"}"
			else:
				aRow += rowEnder
				aRow = str(aRow) + '\n'
				Jfile.write(aRow)
				aRow = None
		# Record the previous path name and row for next loop.
		prevPathName = pathName
		prevRow = aRow
		# Flush the stout buffer before next iteration.
		sys.stdout.flush()
