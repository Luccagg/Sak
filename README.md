# Swiss Army Knife
Swiss Army Knife (SAK) is a reverse shell
with a small amount of functionalities
like uploading files on the victim machine, or executing Commands directly into the victim's machine.

## Usage
. The SAK uses the client/server model to work.

. The server (victim) is running on the victim machine and set up in listener and initialize a command shell.

. The client (attacker) connect to the server and all the data (commands) that he inputs is executed on the victim machine.

### Example
.Running the SAK in listening mode --> victim pc is listening for incoming connections from all network interfaces.

![Alt text](/images/sak1.png?raw=true "Sak1")

.Running the SAK in the target mode (client) --> attacker pc connects to the server.

![Alt text](/images/sak2.png?raw=true "Sak1")

.After pressing CRTL+D the attacker have an **"interactive shell"**.

![Alt text](/images/sak3.png?raw=true "Sak1")

.Executing commands on the shell (i changed the directory where the SAK was executed on Target mode to see that the commands are executing in the directory that the server mode is).

![Alt text](/images/sakco.png?raw=true "Sak1")

.Server side when a connection is received.

![Alt text](/images/sakrre.png)

