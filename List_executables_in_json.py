## This is a tool that list out all of the executables that ara available inside of the container, the informations listed inculding:
# 1. The name or UUID of the docker image that contains it.
# 2. The path to the executable.
# 3. THe SHA256 checksum of the executable.

## todo: List the output of the version flag if the tools has one.
# The question to get the image ID and tag name within a container is posted on the docker help forum.

## The current output format in json is :
'''
{"path":[
	{
	"filepath":"/path/to/executable",
	"SHA256":"..."
	}
	{
	"filepath":"/path/to/executable",
	"SHA256":"..."
	}
	]
}
'''

## Maintainer: David Weng email:weng#email.arizona.edu

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
strpath = str("")
strsha256 = str("")

rowBeginer = "{\"path\":["
rowEnder = "]}"

## (output, err) = process.communicate()
#The problem with above code is that output, err = p.communicate() will block next statement till ping is completed
# Out put the real time out put of the current available executables in a container.
while True:
	out = processFind.stdout.readline()
	# poll to know if the child prorcess has terminated.
	if out == '' and processFind.poll() != None:
		break;	
	# If there is still have output, write the result into in the following way:
	if out != '':
		## filename and path name.
		pathName = os.path.dirname(out)
		filename = os.path.basename(out)
		tempHashValue = hashlib.sha256(filename)	
		shaHashValue = tempHashValue.hexdigest()	
		strpath = str(out)
		strsha256 = shaHashValue
		rowMiddler = "{\"filepath\":\"" + strpath  +"\",\"SHA256\":\"" + strsha256 +"\"}"
		# If the info out last time has not been writen into json file, give the value to current row.
		if prevRow != None:
			aRow = prevRow
			prevRow = None
	 	#If the previous pathname is the same as the currenct one, write the checksum of executable under this path in json format. 
		if prevPathName == pathName:
			aRow += rowMiddler
		else:	
			if aRow == None:
				aRow = rowBeginer + rowMiddler
				prevRow = None
			# If this all the executables in this path has been gone through, write out into json file and set record info of previous row.  
			else:
				aRow += rowEnder
				aRow = str(aRow) + '\n'
				Jfile.write(aRow)
				aRow = None
				prevRow = rowBeginer + rowMiddler
		# Record the previous path name and row for next loop.
		prevPathName = pathName
		# Flush the stout buffer before next iteration.
		sys.stdout.flush()
