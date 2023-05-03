import time

if __name__=="__main__":
    t = int(time.time())
    with open('testlogs.log', 'r') as file:
        data = file.read().split('\n')
        cache = []
        n = 0

        f = open(f"data/{t}-0.point", "w")

        for line in data:
            l = line.split("minimal_subscriber")
            if len(l)>1:
                if len(cache) > 30:
                    n = n + 1
                    f.write("\n".join(cache))
                    f.close()
                    f = open(f"data/{t}-{n}.point", "w")
                cache = []
                cache.append(l[1][3:])
            else:
                cache.append(line)
        f.close()
        print(f"Done generating {n} point files")
        print(len(data))