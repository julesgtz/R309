import socket
from time import sleep
from mathfunct import log_de_x

server_socket = socket.socket()
server_socket.bind(("127.0.0.1", 6350))
server_socket.listen(1)
conn, address = server_socket.accept()

print("Succesfully connected")

is_last_msg_ln = False
c_msg = 0
running = True
reply = 0

while running:
    while c_msg != 2:
        try:
            message = conn.recv(1024).decode()
            if message:
                c_msg += 1

                print(message)

                if message == "arret":
                    conn.close()
                    server_socket.close()
                    running = False
                    break

                if is_last_msg_ln:
                    try:
                        reply = log_de_x(float(message))
                    except:
                        reply = "erreur"
                    finally:
                        c_msg = 0
                        is_last_msg_ln = False

                        print(reply)
                        conn.send(str(reply).encode())
                        sleep(1)

                        conn.close()
                        print("Attente d'une connexion")
                        server_socket.listen(1)
                        conn, address = server_socket.accept()
                        print("Succesfully connected")

                if message == "ln" and not is_last_msg_ln:
                    is_last_msg_ln = True
                else:
                    c_msg = 0
            else:
                server_socket = socket.socket()
                server_socket.bind(("127.0.0.1", 6350))
                server_socket.listen(1)
                conn, address = server_socket.accept()
                is_last_msg_ln = False
                c_msg = 0

        except ConnectionResetError:
            server_socket = socket.socket()
            server_socket.bind(("127.0.0.1", 6350))
            server_socket.listen(1)
            conn, address = server_socket.accept()
            is_last_msg_ln = False
            c_msg = 0






