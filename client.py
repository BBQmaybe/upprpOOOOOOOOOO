# import socket
# import pickle

# def register_user(server_host, server_port, name):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((server_host, server_port))
#     data = {"action": "register", "name": name}
#     client_socket.send(pickle.dumps(data))
#     response = client_socket.recv(1024)
#     decoded_response = pickle.loads(response)
#     if decoded_response["status"] == "success":
#         user_id = decoded_response["user_id"]
#         print("Registration successful. Your user ID is:", user_id)
#     client_socket.close()

# def send_message(server_host, server_port, sender_name, recipient_name, message):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((server_host, server_port))
#     data = {"action": "send_message", "recipient_name": recipient_name, "message": message}
#     client_socket.send(pickle.dumps(data))
#     response = client_socket.recv(1024)
#     decoded_response = pickle.loads(response)
#     print(decoded_response["status"])
#     client_socket.close()

# if __name__ == "__main__":
#     server_host = "127.0.0.1"
#     server_port = 8888
#     name = input("Enter your name: ")
#     register_user(server_host, server_port, name)
#     sender_name = name

#     try:
#         while True:
#             recipient_name = input("Enter recipient's name: ")
#             message = input("Enter your message: ")
#             send_message(server_host, server_port, sender_name, recipient_name, message)
            
#             choice = input("Do you want to send another message? (yes/no): ").lower()
#             if choice == 'no':
#                 print("\nClosing the client...")
#                 client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 client_socket.connect((server_host, server_port))
#                 data = {"action": "disconnect", "name": name}
#                 client_socket.send(pickle.dumps(data))
#                 response = client_socket.recv(1024)
#                 decoded_response = pickle.loads(response)
#                 print(decoded_response["status"])
#                 client_socket.close()
#                 break
#     except KeyboardInterrupt:
#         print("\nClosing the client...")
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((server_host, server_port))
#         data = {"action": "disconnect", "name": name}
#         client_socket.send(pickle.dumps(data))
#         response = client_socket.recv(1024)
#         decoded_response = pickle.loads(response)
#         print(decoded_response["status"])
#         client_socket.close()
        



import socket
import pickle

def register_user(server_host, server_port, name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    data = {"action": "register", "name": name}
    client_socket.send(pickle.dumps(data))
    response = client_socket.recv(1024)
    decoded_response = pickle.loads(response)
    if decoded_response["status"] == "success":
        user_id = decoded_response["user_id"]
        print("Registration successful. Your user ID is:", user_id)
    client_socket.close()

def send_message(server_host, server_port, sender_name, recipient_name, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    
    # Генерация кода Хэмминга для сообщения
    hamming_code = generate_hamming_code(message)
    data = {"action": "send_message", "sender_name": sender_name, "recipient_name": recipient_name, "message": hamming_code}
    client_socket.send(pickle.dumps(data))
    
    response = client_socket.recv(1024)
    decoded_response = pickle.loads(response)
    print(decoded_response["status"])
    client_socket.close()

def generate_hamming_code(data):
    # Преобразуем входные данные в последовательность битов
    data = ''.join(format(ord(char), '08b') for char in data)
    
    r = 0
    while 2**r < len(data) + r + 1:
        r += 1
    
    # Создаем список с расширенными данными
    extended_data = []
    j = 0
    k = 0
    for i in range(len(data) + r):
        if i+1 == 2**j:
            extended_data.append(0)
            j += 1
        else:
            extended_data.append(int(data[k]))
            k += 1
    
    # Вычисляем значения проверочных битов
    for i in range(r):
        position = 2**i - 1
        count = 0
        for j in range(position, len(extended_data), 2*(position+1)):
            count += sum(extended_data[j:j+(position+1)])
        if count % 2 == 0:
            extended_data[position] = 0
        else:
            extended_data[position] = 1
    
    # Возвращаем Хэмминг-код
    return ''.join(map(str, extended_data))



if __name__ == "__main__":
    server_host = "192.168.1.100"
    server_port = 8888
    name = input("Enter your name: ")
    register_user(server_host, server_port, name)
    sender_name = name
    
    while True:
        recipient_name = input("Enter recipient's name: ")
        message = input("Enter your message: ")
        send_message(server_host, server_port, sender_name, recipient_name, message)
        
        choice = input("Do you want to send another message? (yes/no): ").lower()
        if choice == 'no':
            print("\nClosing the client...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_host, server_port))
            data = {"action": "disconnect", "name": name}
            client_socket.send(pickle.dumps(data))
            response = client_socket.recv(1024)
            decoded_response = pickle.loads(response)
            print(decoded_response["status"])
            client_socket.close()
            break