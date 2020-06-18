import extract
import struct
import random
import string
import database

def ooff():
    with open('namedecodetest.data', mode='rb') as file:  # b is important -> binary
        decodetest = file.read()
    f = open("connection.log", "wb")
    def randomStringDigits():
        """Generate a random string of letters and digits """
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(40))

    randTOKEN = randomStringDigits()
    randID = random.randrange(1000000000,4294967295)
    print(extract.sendLogin(randID,randTOKEN,16,167))
    f.write(extract.returnNameChange("e"))
    print(extract.extractNameChange(decodetest))
    f.close()


#database.addUser(extract.generateID(),extract.randomStringDigits())

database.changeUserName(1331237312,'hello')
print(database.findUserName(1331237312))
