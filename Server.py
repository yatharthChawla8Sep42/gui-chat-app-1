import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
     " What is the capital of Finland? \n a.Helsinki\n b.Paris\n c.Oslo\n d.Copenhagen",
     " How many episodes of The Simpsons are there as of March 2022?  \n a.700\n b.721\n c.764\n d.821",
     " Who painted Mona Lisa? \n a.Michelangelo \n b.Pablo Picasso \n c.Leonardo da Vinci \n d.Claude Monet",
     " What is the Starry Night art work's worth? \n a.$10 million\n b.$73 million\n c.$100+ million\n d.$15 million",
     " Which planet is closest to the sun? \n a.Mercury\n b.Pluto\n c.Earth\n d.Venus"
]

answers = ['a', 'b', 'd', 'c', 'a']

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to the quiz game!".encode('utf-8'))
    conn.send("See how much you can score! Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Awesome! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Haha! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()       
    