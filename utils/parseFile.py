def parseFile(name):
    items = []

    with open(name) as file:
        lines = file.read().split("\n")
        if len(lines) > 10:
            items = []
            for line in lines:
                l = line.split(" ")
                for idx,n in enumerate(l):
                    l[idx] = int(n)
                items.append(l)
    return items

def getParsedFiles(dir):
    files = []
    for file in dir:
        data = parseFile(file)
        files.append(data)
    return files