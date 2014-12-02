DFS-Project
===========

###Brief Description 
This project contains the source code for a distributed file system (DFS), the DFS is made up of a metadata server, several data nodes and its clients. If a file is stored in the DFS it will distribute the file among all it's available data nodes and when a file is read from the DFS it will recunstruct it from it's data nodes and write it on a destination of your choice.

###Set Up
Create Database:

```
python createdb.py
```

###Usage
- Run the metadata server in the following manner:
```
python meta-data.py <port, default=8000> 
```
- Once the metadata server is up and running one can add datanodes to this server:

```
python data-node.py <server> <port> <datapath> <metadata port, default=8000>
```
- If running on local machine server is localhost, the port can be anyone not in use, the datapath is the directory where the data node will write the file chunks 

- Once data nodes are connected to the metadata server and running, one can add files to the DFS and read files from it by using copy.py

- This command will read from the DFS (Copy from DFS to computer):

```
python copy.py <server>:<port>:<dfs file path> <destination file>
```
- server and port stay the same. Path on the DFS has to be an existing file on the DFS and <destination file> is the path and the name where you wish to create the new file on your computer.

- To know all the files that are currently in the DFS you can use the ls.py

- This command will display a list of all the files on the DFS and displays them on your terminal:

```
python ls.py <server>:<port, default=8000>
```
- If running locally <server> will be localhost

###How it works:
- createdb.py:
This script is provided by the professor and it creates the data base that we use in the project.

- meta-data.py:
The meta-data creates an interface between the datanodes and the client. Depending on the commands given from the other scripts it will call it's functions.
They are the following:
*list: it sends a list of all the files currently on the DFS.
*reg: Register a new client to the DFS. ACK if successfully registered, NAK if problem and DUP if its a duplicate registration.
*put: copy.py will send this command. Insert a new file into the database and send to data nodes to save the file.
*get: copy.py will send this command. This function is used for reading from the DFS (copy from the DFS to your computer). It will recieve a file name and return the information needed to reconstruct it to the computer.
*blocks: copy.py sends this command. This function recieves the information necesary to create blocks, this are to keep track of the file chunks and be able to recunstruct the file if asked for a read.

- ls.py:
ls.py will recieve the server and port for the metadata server. It will send the list command and display the files currently stored in the DFS in an orderly fashion.

- data-node.py:
This will receive <server> <port> <data path> <metadata port, default=8000>. The data node will first register itself with the metadata server and then it will listen for connections from copy.py. If copy.py sends a write command this will write the chunks on the designated directory and send the chunkID back to the copy client. If it sends read then it will read the chinks and return its contents to the copy client.

- copy.py:
The copy client will recieve instructions to write to the DFS or read from the DFS. When writting to the DFS it will send the put command to the metadata server and recieve the availabe data nodes and their information. Then it will separate the file and send a chunk to each data node, then it will recieve the node name and the chunk ID from each node and send this information to the metadata server so that it may store this blocks. If given instructions to read it will send the get command to the metadata server and the server will reply with the nodes that store this file and with the information needed to reconstruct it. It will then send the read command to all the data nodes which store the file and the chunkID so that it may create a file out of all the chunks.


