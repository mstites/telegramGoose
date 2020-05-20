import string
import logging
def ofile(location):
    with open(location, "r") as file:
        return file.read()

def wfile(location, data):
    """Write file"""
    file = open(location, "w")
    file.write(str(data))
    file.flush()
    file.close()

def cleanInput(text, toStrip = string.punctuation + string.digits + " "):
    """Cleans user input
    toStrip = characters to remove"""
    logging.debug("stripping:" + toStrip)
    cleanText = text.translate(str.maketrans('', '', toStrip))
    # cleanText = ''.join(char for char in text if not char in toStrip)
    return cleanText.lower()

def loadKey (loc):
    """Load key from txt file"""
    lines = ofile(loc).splitlines()
    listKey = []
    for line in lines:
        if line.startswith("#"):
            continue # ignore commented lines
        else:
            line = line.replace(":", ",") # only one seperator type
            line = line.split(",")
            listKey.append(line)
    return listKey

def loadKeyDict(loc, list = False):
    """Construct the key dictionary
    list = return values in list format (for keys for more than one value per key)"""
    listKey = loadKey(loc)
    dictKey = {}
    for ky in listKey:
        output = ky[0] # eventual reply to message, no cleaning
        for item in ky[1:]:
            item = cleanInput(item)
            if list:
                if item not in dictKey:
                    dictKey[item] = [output]
                else:
                    dictKey[item].append(output)
            else:
                dictKey[item] = output
    key = dictKey
    return key
