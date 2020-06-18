import xml.etree.ElementTree as ET

tree = ET.parse('profiles.xml')
treeRoot = tree.getroot()


def addUser(id, token):
    child = ET.Element('profile')
    child.set('id', str(id))
    child.set('token', str(token))
    child.set('name', 'Guest')
    treeRoot.append(child)
    tree.write('profiles.xml')

def changeUserName(id,newname):
    for x in treeRoot:

        if x.get('id') == str(id):
            print(newname)
            x.set('name',str(newname))
            tree.write('profiles.xml')

def findUserName(id):
    for x in treeRoot:
        if x.get('id') == str(id):
            return x.get('name'),x.get('token')
