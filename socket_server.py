import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 6
JOB_NUMBER = [1, 2,3,4,5,6]
queue = Queue()
all_connections = []
all_address = []
all_name=[]
z=0

def create_socket():
    try:
        global host
        global port
        global s
        host=''
        port=9090
        s=socket.socket()

    except socket.error as msg:
       print("Socket creation error " + str(msg))

def bind_socket():
     try:
        global host
        global port
        global s
        
        #print("Binding the Port " + str(port))
        
        s.bind((host,port))
        s.listen(5)

     except socket.error as msg:
      #  print("Socket binding error " + str(msg) +'\n' + "Retrying....")
        bind_socket()

def accepting_connections():
  # for c in all_connections:
  #      c.close()
    global z
    global coz
    del all_connections[:]
    del all_address[:]
    del all_name[:]
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # ethu vanthu timeout error illama pannum
	    #inga thaan name recieve pannum
            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established :" + address[0] ,end=" ")
            coz=conn
            z=1
            name=coz.recv(1024)
            name=name.decode()    
            print("    1234" +str(name))
            if name:
             all_name.append(name)
             break

        except:
           # print("Error accepting connections")
            z=0
 
#1) See all the clients list2) Select a client select 1 3) Send commands to the connected client

def start_shell():

    while True:
        cmd = input('shell> ')
        if cmd == 'list':
            list_connections()
        elif cmd == 'list_active':
            list_active()
        elif 'select' in cmd:
            conn = get_target(cmd)
            # if conn is not None:
            #    send_target_commands(conn)
        elif 'connect' in cmd:
            conn=rec_target(cmd)
        elif 'exitz' in cmd:
           quit(0)
        else:
            print("Command not recognized")


def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):

        results = str(i) + "   " + str(all_name[i])+ "   " +str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("------------Clients------------" + "\n" + results)
def list_active():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            del all_name[i]
            continue

        results = str(i) + "   " + str(all_name[i])+ "   " +str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("------------Clients------------" + "\n" + results)


# Selecting the target
def get_target(cmd):
    target = cmd.replace('select ', '')  # target = id
    target = int(target)
    conn = all_connections[target]
    print("Server is connected to : " + str(all_address[target][0]) + "  " + str(all_name[target]))
    message='no'
    print(str(all_name[target]) + " : ")
    zz='loudxshellz'
    while True and zz!=message:
        data=conn.recv(1024)                                #sendto    recvfrom
        data=data.decode()
        if not data:   #c.recv retruns false
           break
        print(str(all_name[target])+ " : " + str(data))
        message=input("loud : ")
        byt=message.encode()
        conn.send(byt)
    #conn.close()
    start_shell()
def rec_target(cmd):
    target = cmd.replace('connect ', '')  # target = id
    target = int(target)
    conn = all_connections[target]
    print("Server is connected to : " + str(all_address[target][0]) + "  " + str(all_name[target]))
    message='no'
    print(str(all_name[target]) + " : ")
    zz='loudxshellz'
    while True and zz!=message:
        message=input("loud : ")
        byt=message.encode()
        conn.send(byt)
        data=conn.recv(1024)                                #sendto    recvfrom
        data=data.decode()
        if not data:   #c.recv retruns false
           break
        print(str(all_name[target])+ " : " + str(data))

    conn.close()
    start_shell()




#threads in progress
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if (x%2) == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if (x%2) == 0:
            start_shell()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()






