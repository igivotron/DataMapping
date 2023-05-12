from metalmap import MetalMap
from extract import Extract

doc = Extract("test.txt")
carte = MetalMap()

l = doc.list_int()

for i in l:
    carte.addData((i[0], i[1]), i[2])

print(carte)

