
file = open("temp.txt", "r")
r = file.read()
print([x.split(" ")[1] for x in r.split("\n")])
file.close()
