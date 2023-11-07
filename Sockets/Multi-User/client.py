import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            message = data.decode("utf-8")
            print(message)
        except Exception as e:
            print(f"Erreur lors de la réception du message : {str(e)}")
        break

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('10.128.1.64', 6250))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        destination_ip = input("Entrez l'adresse IP de destination : ")
        message = input("Entrez votre message : ")
        if message.lower() == "exit":
            break
        full_message = f"{destination_ip}:{message}"
        client.send(full_message.encode("utf-8"))

    client.close()

if __name__ == "__main__":
    main()