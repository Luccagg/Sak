#!/usr/bin/python3 
import sys
import socket
import getopt
import threading
import subprocess

# define global variables
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

def usage():
    print("SWISS ARMY KNIFE")
    print()
    print("Usage: ./swiss_army_knife.py -t target_host -p port")
    print("-l --listen                      - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run         - execute the given file upon receiving a connection")
    print("-c --command                     - initialize a command shell")
    print("-u --upload=destination          - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples: ")
    print("./swiss_army_knife.py -t 192.168.0.1 -p 5555 -l -c")
    print("./swiss_army_knife.py -t 192.168.0.1 -p 5555 -l -u=c:\\\\target.exe")
    print("./swiss_army_knife.py  -t 192.168.0.1 -p 5555 -l -e='cat /etc/passwd'")
    sys.exit(0)



# Client
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to our target host
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode("utf-8"))
        while True:
            # now wait for data back
            recv_len = 1
            response = b""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break

            print(response.decode("utf-8"), end=' ')
            # wait for more input
            buffer = input("")
            buffer += "\n"
            # send it off
            client.send(buffer.encode("utf-8"))
    except Exception as e:
        print(e)
        print("[*] Exception! Exiting.")
        client.close()

# Server
def client_handler(client_socket):
    global upload 
    global execute
    global command

    # check for upload
    if len(upload_destination):
        # read in all bytes and write to destination
        file_buffer = ""
        # keep reading data until finished
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        # now take the these bytes and try to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer.encode("utf-8"))
            file_descriptor.close()
            # acknowledge that we wrote the file out
            client_socket.send(f"Successfully saved file to {upload_destination}\r\n")
        except:
            client_socket.send(f"Failed to save file to {upload_destination}\r\n")
    # check for command execution
    if len(execute):
        # run the command
        output = run_command(execute)
        client_socket.send(output)
    # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            client_socket.send("<SAK:#> ".encode('utf-8'))
            # now we receive until we see a linefeed
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                try:
                    cmd_buffer += client_socket.recv(1024)
                except:
                    print('Connection Closed')
            # send back the command output
            response = run_command(cmd_buffer)
            # send back the response
            client_socket.send(response)


def server_loop():
    global target
    global port
    # if target not defined, we listen on all interfaces
    print(target)
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        print(f"Connection received from {addr}")
        # Use Multi-Threading to handle client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    # trim newline
    command = command.rstrip()
    # run command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    # send the output back to client
    return output

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target   
    
    if not len(sys.argv[1:]):
        usage()
    # read the commandline options
    try:
        opts, args= getopt.getopt(sys.argv[1:], "hle:t::p:cu", ["help", "listen", "execute", "target", "port", "comman"         , "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage() 
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--comand"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert(False, "Unhandled Option")
    # Are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if no sending input
        # to stdin
        buffer = sys.stdin.read()
        # send data off
        client_sender(buffer)
    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
       print(f"Listening on 0.0.0.0:{port}")
       server_loop()

if __name__ == '__main__':
    main()
