import glob


dir = glob.glob("data\\raw\\*")

files = []

n = 0

for idx,path in enumerate(dir):
    print(f"[READ] {round((idx+1)*100/len(dir),2)}%")
    with open(path) as file:
        lines = file.read().split("\n")
        n = n + len(lines)
        files.append(lines)

print(f"[READ] Done. Removing now. {len(files)} files. {n} total entries")

print(files)

# b = set(files[0])

# for idx,lst in files:
#     print(lst)
#     # tempSet = set(lst)
#     # b = b - tempSet

# print(b)
