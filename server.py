import socket
import struct
import xml.etree.ElementTree as ET
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostname())
s.bind((socket.gethostname(), 9331))
s.listen(5)
tree = ET.parse('profiles.xml')
treeroot = tree.getroot()

clientsocket, address = s.accept()
print(address)


def sendOK():
    clientsocket.send(struct.pack('>2sII', 'GS'.encode('utf-8'), 1, 0))


while True:

    msg = clientsocket.recv(1024)

    print("rcv: ", msg)
    if len(msg) != 0:
        # print(msg)
        mgc, id, length = struct.unpack('>2sII', msg[:10])
        print('id',id)
        print(id)
        if id == 0:
            print('HELLO SIGNAL')
            print(length)
            sendOK()
        if id == 2:
            print('set')
            sendOK()
            # ok
            mgc, id, length, string2 = struct.unpack('>2sII16s', msg)
            print(mgc,' ',id,' ',length,' ',string2.decode('utf-8'))
            print("NEW ACCOUNT SIGNAL")
            child = ET.Element('profile')
            print(string2.decode('utf-8'))
            child.set('name', str(string2.decode('utf-8')).replace('.', ''))
            child.set('value', '10')
            treeroot.append(child)
            tree.write('profiles.xml')
        if id == 3:
            print('get')
            #sendOK()
            mgc, id, length, string3 = struct.unpack('>2sII16s', msg)
            print("REQUEST ACC SIGNAL")
            # child = ET.Element('profile')
            # child.set('name', str(string[2:1]).replace('.', ''))
            # child.set('value', '10')
            # treeroot.append(child)
            # tree.write('profiles.xml')
            for x in treeroot:

                # s.send(struct.pack('>2sII16s','GS'.encode('utf-8'),2,16,name.encode('utf-8')))
                if x.get('name') == str(string3.decode('utf-8')).replace('.', ''):
                    namevar = x.get('name')+'.'*(16-len(x.get('name')))
                    print(x.get('value'))
                    #stuff =
                    #print(stuff)
                    clientsocket.send(struct.pack('>2sII16sI', 'GS'.encode('utf-8'), 4, 16,namevar.encode('utf-8'),int(x.get('value'))))

