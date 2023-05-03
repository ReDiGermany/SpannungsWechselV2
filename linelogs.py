import sys
import time

if __name__=="__main__":
    t = int(time.time())
    l = 0
    disc = int(sys.argv[1])
    l_str = sys.argv[2]
    l = int(l_str)
    
    input_file = "data/1683148388-0.point"

    min = [9999999999,""]
    max = [-9999999999,""]
    
    with open(input_file, 'r') as file:
        data = file.read().split('\n')
        cache = []
        n = 0

        f = open(f"{input_file}.{l}.{disc}.point", "w")

        for idx,line in enumerate(data):
            if idx == 0:
                cache.append(line)
            ln = line.split(" ")
            ln2int = int(ln[2])

            if ln2int > max[0]:
                max[0] = ln2int
                max[1] = line

            if ln2int < min[0]:
                min[0] = ln2int
                min[1] = line

            if ln2int == l:
                cache.append(line)

        cache.append(min[1])
        cache.append(max[1])

        f.write("\n".join(cache))
        f.close()
        print(f"Done")