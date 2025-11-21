# Swiss Army Knife
Swiss Army Knife (SAK) is a reverse shell
with a small amount of functionalities
like uploading files on the machine, or executing Commands directly into the machine.

## Usage
. The SAK uses the client/server model to work.

. The server is running on the machine and set up in listener and initialize a command shell.

. The client connect to the server and all the data (commands) that he inputs is executed on the machine.

### Example
.Running the SAK in listening mode --> pc is listening for incoming connections from all network interfaces.

![Alt text](1.jpeg?raw=true)

.Running the SAK in the target mode  --> pc connects to the server.

![Alt text](2.jpeg)

.After pressing CRTL+D the server have an **"interactive shell"**.

![Alt text](3.jpeg)

.Executing commands on the shell (i changed the directory where the SAK was executed on Target mode to see that the commands are executing in the directory that the server mode is).

![Alt text](4.jpeg?)

.Server side when a connection is received.

![Alt text](5.jpeg)

