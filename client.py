import socket
import select
import sys
import msvcrt
# checks if user entered 3 arguments
# ideally in this project, the IP address would be localhost (127.0.0.1) as well
if len(sys.argv) != 3:
    print("Please enter args in following order: IP Address, port")
    exit()

if not (sys.argv[2]).isdigit():
    print("Port number is not an integer.")
    exit()

try:
    socket.inet_aton(sys.argv[1])
except socket.error:
    print("Enter a valid host address.")
    exit()

IP = str(sys.argv[1])
port = int(sys.argv[2])

# boilerplate for client socket, same as in server.py
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))

print("Client registered")


while True:
    # possible input methods are user or from the client itself from the server
    inputs = [client]
    # select.select assigns sockets to 3 categories: sockets that read input, write output, or report errors
    # the client only reads input, so the other socket lists are empty
    # **select.select() blocks until something is ready for reading from one of the input methods
    # The last argument is a timer to end the block, to work around getting stdin to function.
    read_list, write_list, error_list = select.select(inputs, [], [], 1)

    # Windows doesn't accept stdin as a socket, so msvcrt is used to provide some of the functionality
    # of using sys.stdin as a socket.
    # Detects keyboard input, and the loop is blocked until user hits enter.
    if msvcrt.kbhit():
        read_list.append(sys.stdin)

    for readable in read_list:
        # input received from server, so client itself writes
        if readable is client:
            message = readable.recv(4096).decode()
            print(message)
        # input received from user, so user standard input writes
        else:
            message = sys.stdin.readline().replace('\n', '').encode()
            client.send(message)
            sys.stdout.flush()
