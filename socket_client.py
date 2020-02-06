import socket

def Mai():
    host='Enter the host ip here'#enter the host ip here
    port=9090
    s=socket.socket()
    s.connect((host,port))
    print('connecting...........')
    while True:
     name=input("Enter your name : ")
     name=name.encode()
     s.send(name)
     name=name.decode()
     if name:
       break
    print("-------------------------------INSTRUCTIONS-----------------------------------")
    print("--To start conversation ENTER SOME TEXT LIKE 'hi , hello' and WAIT for reply--")
    print("-----------------In case of no reply follow the above line--------------------")
    print("----------If your a busy one, then make a call to the respected one-----------")
    print("--'LOUDXSHELLZ' MEANS wait for reply, he might be in some other conversation--")
    print("-------------BE POLITE...DONT'T USE WORDS WHICH MAY HURT OTHERS---------------")
    print("---------IF REPORTED , YOUR IP WILL BE BLOCKED..SO BE CAREFULL----------------")
    print("--------------------To end the conversation , enter 'q'-----------------------")
    print("")	
    print(str(name) ,end=" : ")
    zz='loudxshellz'
    message=input()
    while message!='q':
        byt=message.encode()
        s.send(byt)
        data=s.recv(1024)
        data=data.decode()
        if zz==data:
          print('---------wait--loud--is--busy---------')
        else:

         print("loud : "+str(data))
         print(str(name),end=" : ")
         message=input()
    s.close()

if __name__=="__main__":
    Mai()
