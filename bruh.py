import socket
import threading
import struct
import extract
import time
import database


# f = open("connection.log", "wb")
with open('datafiles/clientBox.data', mode='rb') as file:  # b is important -> binary
    clientBox = file.read()
with open('datafiles/serverBox.data', mode='rb') as file:  # b is important -> binary
    serverBox = file.read()
with open('LoginOk.data', mode='rb') as file:  # b is important -> binary
    loginData = file.read()
#with open('OHD.data', mode='rb') as file:  # b is important -> binary
    #ohdData = file.read()
with open('unkbutigottasendit.data', mode='rb') as file:  # this is not mail... actually its OHD
    ohdData = file.read()
with open('lwarbweirdthing.data', mode='rb') as file:  # b is important -> binary
    lwarbThing = file.read()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 9339))

sock.listen(1)

connections = []




def handler(c, a):
    global loginData
    global ohdData
    global connections
    userid = 0


    # c.send(loginData)
    # c.send(ohdData)

    while True:
        data = c.recv(1024)

        #print(data)
        if data != b'':



            if extract.byteToInt(data) == 10101:
                tf, userid, token,major,minor = extract.extractLogin(data,'16.167')

                if tf == True:
                    if userid != 0:
                        print('Logging in: ', userid,token, ' on version ',major ,'.',minor)
                        # print('sending:',extract.sendLogin(userid,token,major,minor))
                        userid = userid
                        c.send(extract.sendLogin(userid,token,major,minor))
                        c.send(extract.genOHDMSG(userid))
                        c.send(lwarbThing)
                    else:
                        print('Creating new account.')

                        genID = extract.generateID()
                        genToken = extract.randomStringDigits()
                        userid = genID
                        c.send(extract.sendLogin(genID,genToken,16,167))

                        database.addUser(genID,genToken)

                        time.sleep(0.2)
                        #ownhomedata V
                        c.send(ohdData)
                        c.send(lwarbThing)


                elif tf == False:
                    print('Refused connection.')
                    c.send(extract.sendUpdateAvailable(
                        "You don't have the latest version of Garlfin Stars! Click to download the update.",
                        'https://github.com/garlfin/dae2scw'))
            elif extract.byteToInt(data) == 10108:
                print('Keeping alive',userid,'.')
                c.send(extract.keepAlive())
            elif extract.byteToInt(data) == 14102:
                print('End client turn from ',userid)
                #if extract.extractCommandID(data) == 35075:

                    # print(data)

                #else:
                print('Unknown command id', extract.extractCommandID(data),'. ',data)
            elif extract.byteToInt(data) == 23591:
                print('Weird info coming in from', userid)
            elif data == clientBox:
                c.send(serverBox)
            elif extract.byteToInt(data) == 14366:
                print('14366 incoming: ', data)
            elif extract.byteToInt(data) == 10107:
                print('Client capabilities (10107) incoming: ', data)
            elif extract.byteToInt(data) == 14600:
                print('Changing name for', userid, '.')
                c.send(extract.returnNameChange(extract.extractNameChange(data)))
                database.changeUserName(userid, extract.extractNameChange(data))
            else:
                print(data)

        # for connection in connections:
        # connection.send()

        # connection.send(bytes(data))

        if not data:
            print(c, " left")
            connections.remove(c)
            c.close()

            break


while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c, a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(c, ' joined')
    #print(connections)
