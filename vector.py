import socket
import pickle
import time
import threading
import random

random.seed()

class Process:
    def __init__(self, process_id: int, total_process: int = 4):
        self.process_id = process_id
        self.total_process = total_process
        self.vector_clock = [0] * total_process
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #define a porta de cada processo com base em seu ID (satisfaz requisito 2)
        self.socket.bind(('localhost', 5000 + process_id))
        self.socket.listen()
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, receiver_port: int):
        #Envia mensagens entre 1 a 4 segundos (satisfaz requisito 6)
        time.sleep(random.randint(1,4))

        #Atualiza o próprio vetor, incrementando um evento (evento de recebimento da mensagem)
        self.vector_clock[self.process_id] += 1

        #Mensagem a ser enviada: o próprio ID e seu próprio vetor
        message = (self.process_id, self.vector_clock)

        #Imprime na tela o vetor que está enviando (satisfaz requisito 4). Adicionalmente, imprime a porta onde a mensagem será enviada
        print(f"P{self.process_id}: Enviando vetor {self.vector_clock} para o processo da porta {receiver_port}")
        recipient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recipient_socket.connect(('localhost', receiver_port))
        recipient_socket.sendall(pickle.dumps(message))
        recipient_socket.close()

    def receive_messages(self):
        while True:
            conn = self.socket.accept()[0]
            data = conn.recv(2048)
            sender_process_id, sender_vector_clock = pickle.loads(data)

            #Imprime na tela o vetor recebido pela mensagem e seu próprio vetor atual (satisfaz 2/3 do requisito 5)
            print(f"P{self.process_id}: mensagem recebida de P{sender_process_id}. Vetor recebido: {sender_vector_clock} // Vetor atual de P{self.process_id}: {self.vector_clock}")

            #Realiza a atualização do vetor com base no que foi mostrado no material: seleciona o maior valor em cada posição e adiciona 1 ao seu próprio relógio
            for p in range(self.total_process):
                max_value = max(self.vector_clock[p], sender_vector_clock[p])
                self.vector_clock[p] = max_value
            
            self.vector_clock[self.process_id] += 1

            #Imprime na tela o vetor resultante (satisfaz o restante que faltava do requisito 5)
            print(f"P{self.process_id}: novo vetor: {self.vector_clock}")

            conn.close()

process_quantity = 4
p0, p1, p2, p3 = [Process(i, process_quantity)
                           for i in range(process_quantity)]

#Cada processo envia mensagens para portas aleatórias em tempos aleatórios (satisfaz requisito 1)
#As portas são sempre da porta 5000 (que é sempre a porta de P0) até a porta 5000 + quantidade de processos - 1 (Sempre a do último processo, nesse caso, P3)
#Poderia ter feito um dicionário para cada processo para funcionar como uma tabela que atribui a respectiva porta de cada processo conhecido
#Em vez disso, optamos por simplesmente manter o intervalo das portas conhecidas para passar como parâmetro.
#Pela simplicidade do algoritmo, creio que essas implementações são suficientes para satisfazer o requisito 3, sem a necessidade de uma tabela

#PRIMEIRA SOLUÇÃO

while True:
     
    p0.send_message(random.randint(5000,5000+process_quantity-1))
    p1.send_message(random.randint(5000,5000+process_quantity-1))
    p2.send_message(random.randint(5000,5000+process_quantity-1))
    p3.send_message(random.randint(5000,5000+process_quantity-1))


#SEGUNDA SOLUÇÃO
'''
#Vetor de portas conhecidas para cada processo, excluindo a própria porta
p0_ports = [5001,5002,5003]
p1_ports = [5000,5002,5003]
p2_ports = [5000,5001,5003]
p3_ports = [5000,5001,5002]
while True:
    #Seleciona aleatoriamente uma porta de seu vetor de portas conhecidas
    p0.send_message(random.choice(p0_ports))
    p1.send_message(random.choice(p1_ports))
    p2.send_message(random.choice(p2_ports))
    p3.send_message(random.choice(p3_ports))
'''