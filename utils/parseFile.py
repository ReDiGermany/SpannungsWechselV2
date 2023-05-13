def isVisible(item,visible_area):
    return item < visible_area[1] and item > visible_area[0]

def inVisibleArea(item,visible_area):
    ret = item[0] > visible_area[0][0] and\
          item[0] < visible_area[1][0] and\
          \
          item[1] > visible_area[0][1] and\
          item[1] < visible_area[1][1] and\
          \
          item[2] > visible_area[0][2] and\
          item[2] < visible_area[1][2]
    return ret

def parseFile(name,visible_area=[]):
    items = []

    with open(name) as file:
        lines = file.read().split("\n")
        if len(lines) > 10:
            items = []
            for line in lines:
                l = line.split(" ")
                for idx,n in enumerate(l):
                    l[idx] = int(n)
                if inVisibleArea(l,visible_area):
                    items.append(l)
    return items

def getParsedFiles(dir,visible_area=[]):
    files = []
    for file in dir:
        data = parseFile(file,visible_area)
        
        files.append(data)
    return files