# import socket
# import threading
# import pickle

# # Счетчик для порядкового номера регистрации
# registration_counter = 0
# # Словарь для хранения таблицы маршрутизации и состояния онлайн
# user_mapping = {}

# def handle_client(client_socket, client_address):
#     global registration_counter
#     while True:
#         data = client_socket.recv(1024)
#         if not data:
#             break
#         try:
#             decoded_data = pickle.loads(data)
#             if decoded_data["action"] == "register":
#                 name = decoded_data["name"]
#                 if name in user_mapping:
#                     response = {"status": "name_taken"}
#                     client_socket.send(pickle.dumps(response))
#                 else:
#                     registration_counter += 1
#                     user_id = str(registration_counter).zfill(4)  # Порядковый номер регистрации в качестве ID
#                     user_mapping[name] = {"user_id": user_id, "status": "online"}
#                     response = {"status": "success", "user_id": user_id}
#                     client_socket.send(pickle.dumps(response))
#                     print(f"User {name} is online.")
#             elif decoded_data["action"] == "send_message":
#                 recipient_name = decoded_data["recipient_name"]
#                 message = decoded_data["message"]
#                 if recipient_name in user_mapping:
#                     recipient_id = user_mapping[recipient_name]["user_id"]
#                     recipient_status = user_mapping[recipient_name]["status"]
#                     if recipient_status == "online":
#                         response = {"status": "delivered"}
#                         client_socket.send(pickle.dumps(response))
#                         print(f"Message from {recipient_name} ({recipient_id}): {message}")
#                     else:
#                         response = {"status": "user_offline"}
#                         client_socket.send(pickle.dumps(response))
#                 else:
#                     response = {"status": "user_not_found"}
#                     client_socket.send(pickle.dumps(response))
#             elif decoded_data["action"] == "disconnect":
#                 name = decoded_data["name"]
#                 if name in user_mapping:
#                     user_mapping[name]["status"] = "offline"
#                     response = {"status": "disconnected"}
#                     client_socket.send(pickle.dumps(response))
#                     print(f"User {name} is offline.")
#         except Exception as e:
#             print("Error:", e)

# def start_server(host, port):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(5)
#     print("Server started on", (host, port))

#     while True:
#         client_socket, client_address = server_socket.accept()
#         print("Accepted connection from", client_address)
#         client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
#         client_handler.start()

# if __name__ == "__main__":
#     start_server("127.0.0.1", 8888)


import socket
import threading
import pickle

# Счетчик для порядкового номера регистрации
registration_counter = 0
# Словарь для хранения таблицы маршрутизации и состояния онлайн
user_mapping = {}



def check_hamming_code(code):
    r = 0
    while 2 ** r <= len(code):
        r += 1

    error_index = 0
    for i in range(r):
        index = 2 ** i - 1
        parity = 0
        for j in range(index, len(code), 2 * (i + 1)):
            parity ^= int(code[j])
        if parity != 0:
            error_index += index + 1

    if error_index != 0:
        print("Error at position:", error_index)
        if code[error_index - 1] == '0':
            code = code[:error_index - 1] + '1' + code[error_index:]
        else:
            code = code[:error_index - 1] + '0' + code[error_index:]
        print("Corrected code:", code)
    else:
        print("No errors detected")
    return code


def handle_client(client_socket, client_address):
    global registration_counter
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        try:
            decoded_data = pickle.loads(data)
            if decoded_data["action"] == "register":
                name = decoded_data["name"]
                if name in user_mapping:
                    response = {"status": "name_taken"}
                    client_socket.send(pickle.dumps(response))
                else:
                    registration_counter += 1
                    user_id = str(registration_counter).zfill(4)  # Порядковый номер регистрации в качестве ID
                    user_mapping[name] = {"user_id": user_id, "status": "online"}
                    response = {"status": "success", "user_id": user_id}
                    client_socket.send(pickle.dumps(response))
                    print(f"User {name} is online.")
            elif decoded_data["action"] == "send_message":
                recipient_name = decoded_data["recipient_name"]
                message = decoded_data["message"]
                # Проверка кода Хэмминга
                corrected_message = check_hamming_code(message)
                if recipient_name in user_mapping:
                    recipient_id = user_mapping[recipient_name]["user_id"]
                    recipient_status = user_mapping[recipient_name]["status"]
                    if recipient_status == "online":
                        response = {"status": "delivered"}
                        client_socket.send(pickle.dumps(response))
                        print(f"Message from {recipient_name} ({recipient_id}): {corrected_message}")
                    else:
                        response = {"status": "user_offline"}
                        client_socket.send(pickle.dumps(response))
                else:
                    response = {"status": "user_not_found"}
                    client_socket.send(pickle.dumps(response))
            elif decoded_data["action"] == "disconnect":
                name = decoded_data["name"]
                if name in user_mapping:
                    user_mapping[name]["status"] = "offline"
                    response = {"status": "disconnected"}
                    client_socket.send(pickle.dumps(response))
                    print(f"User {name} is offline.")
        except Exception as e:
            print("Error:", e)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server started on", (host, port))

    while True:
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server("192.168.1.100", 8888)