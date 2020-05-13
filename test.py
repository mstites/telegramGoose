lines = loadMessage("replies/~key").splitlines()
listKey = []
for line in lines:
    if line.startswith("#"):
        continue # ignore commented lines
    else:
        line = line.replace(":", ",") # only one seperator type
        line = line.split(",")
        listKey.append(line)

dictKey = {}
for ky in listKey:
    output = cleanInput(ky[0]) # eventual reply to message
    for item in ky[1:]:
        dictKey[item] = output
