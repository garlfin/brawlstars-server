import struct
import random
import string
import database

with open('datafiles/beginningohd', mode='rb') as file:
    beginningFile = file.read()
with open('datafiles/middleohd', mode='rb') as file:
    middleFile = file.read()
with open('datafiles/endohd', mode='rb') as file:
    endFile = file.read()

fdat = open('end.dat', 'rb').read()

def getLen(msg):

    return

def genOHDMSG(id):
    name = database.findUserName(id)

    ohdOut = struct.pack('>H', 24101)
    ohdOut += int.to_bytes(773 + len(name), 3, byteorder='big', signed=False)
    ohdOut += beginningFile
    ohdOut += int.to_bytes(id,8,byteorder='big',signed=False)
    ohdOut += middleFile
    ohdOut += int.to_bytes(len(name[0]), 4, byteorder='big', signed=False)
    for letter in name[0]:
        ohdOut += struct.pack('>s', letter.encode('utf-8'))
    ohdOut += endFile

    return ohdOut



def randomStringDigits():
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(40))


def generateID():
    return random.randrange(1000000000, 4294967295)


def writeString(string):
    encoded = string.encode('utf-8')
    return struct.pack('>I', len(encoded)) + encoded


def byteToInt(data):
    return int.from_bytes(data[:2], byteorder='big')


def sendUpdateAvailable(text, link):
    packet = b'\x00\x00\x00\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' + writeString(link) + writeString(
        text) + b'\x00\x00\x01,\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00'

    return struct.pack('>H', 20103) + len(packet).to_bytes(3, 'big') + struct.pack('>H', 0) + packet


def keepAlive():
    return b'\x4e\x8c\x00\x00\x00\x00\x00'

def extractCommandID(data):
    return int.from_bytes(data[9:11],byteorder='big',signed=False)

def extractNameChange(data):
    print(data)
    namelen = int.from_bytes(data[8:11], byteorder='big')
    print(namelen)
    name = data[11:11+ namelen]
    print(name)

    return name.decode('utf-8')


def sendLogin(usrid, tkn, mjr, mnr):

    output = struct.pack('>H', 20104)
    output += b'\x00\x00\x98\x00\x01'
    output += struct.pack('>QQI40s', usrid, usrid, 40, str(tkn).encode('utf-8'))
    output += b'\xff\xff\xff\xff\xff\xff\xff\xff'
    output += struct.pack('>IIII4s', mjr, mnr, 1, 4, 'prod'.encode('utf-8'))
    output += fdat
    output += b'\x01'
    return output


def returnNameChange(newname):
    finalout = b'\x5e\x2f'
    finalout += (len(newname) + 12).to_bytes(3, byteorder='big')
    finalout += b'\x00\x00\x89\x03'
    finalout += len(newname).to_bytes(4, byteorder='big')
    for z in newname:
        finalout += struct.pack('>s', z.encode('utf-8'))
    finalout += b'\x00\x01\x7f\x7f\x00\x00'

    return finalout


def extractLogin(bytes, currentver):
    tf = True
    stringslen = 0
    id = int.from_bytes(bytes[:2], byteorder='big')

    lenth = int.from_bytes(bytes[2:5], byteorder='big')

    unk = int.from_bytes(bytes[5:7], byteorder='big')

    userid = int.from_bytes(bytes[7:15], byteorder='big')
    if userid == 0:
        version = str(int.from_bytes(bytes[19+1:19 + 3+1], byteorder='big')) + '.' + str(
            int.from_bytes(bytes[27+1:27 + 3+1], byteorder='big'))
        #print('cver: ',version)
        if version == currentver:
            tf = True
        else:
            tf = False
        return [tf, 0, 0, 0, 0]

    tokenlen = int.from_bytes(bytes[15:19], byteorder='big')

    stringslen += tokenlen
    token = bytes[19:19 + stringslen]
    # token = token.decode('utf-8')

    major = int.from_bytes(bytes[19 + stringslen:23 + stringslen], byteorder='big')
    minor = int.from_bytes(bytes[27 + stringslen:31 + stringslen], byteorder='big')
    version = str(int.from_bytes(bytes[19 + stringslen:23 + stringslen], byteorder='big')) + '.' + str(
        int.from_bytes(bytes[27 + stringslen:31 + stringslen], byteorder='big'))

    hashlen = int.from_bytes(bytes[31 + stringslen:35 + stringslen], byteorder='big')
    print([userid,token,version])

    masterhash = bytes[35 + stringslen:35 + stringslen + tokenlen]
    stringslen += hashlen
    # masterhash = masterhash.decode('utf-8')

    unkstrlen = int.from_bytes(bytes[35 + stringslen:39 + stringslen], byteorder='big')


    openudidlen = int.from_bytes(bytes[39 + stringslen:39 + 4 + stringslen], byteorder='big')


    openudid = bytes[43 + stringslen:43 + stringslen + openudidlen]
    stringslen += openudidlen
    # openudid = openudid.decode('utf-8')


    unk2len = int.from_bytes(bytes[43 + stringslen:47 + stringslen], byteorder='big')


    modellen = int.from_bytes(bytes[47 + stringslen:51 + stringslen], byteorder='big')


    model = bytes[51 + stringslen:51 + stringslen + modellen]
    stringslen += modellen
    # model = model.decode('utf-8')

    # print(stringslen)
    areacode = int.from_bytes(bytes[51 + stringslen:53 + stringslen], byteorder='big')

    langlen = int.from_bytes(bytes[53 + stringslen:57 + stringslen], byteorder='big')


    lang = bytes[57 + stringslen:57 + stringslen + langlen]
    stringslen += langlen
    # lang = lang.decode('utf-8')


    if version == currentver:
        tf = True
    else:
        tf = False
    return [tf, userid, token, major, minor]
