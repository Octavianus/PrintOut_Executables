PrintOut_Executables

Function:
List out all the executables that are available inside the container
print out the executable in the format of json as follow:

     {“path”: [
          {
          “filepath”: “/path/to/executable”,
          “SHA256”: “...”
          } 
          {
          “filepath”: “/path/to/executable”,
          “SHA256”: “...”
          } 
          ]
     }

====================

Usage docker run -t -i -v /path/to/this/python/script:/mount/point/in/container [container ID]

Within in a docker, container run this python script on the mount point which you assigned in the docker commad.
After a while, your result will show in the mount point named as executables_info.json.

