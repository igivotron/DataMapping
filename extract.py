class Extract:
    def __init__(self, filename):
        self.filename = filename
    
    def read_file(self):
        with open(self.filename) as f:
            return f.read()
    
    def file_to_list(self):
        l = self.read_file().split("\n")
        return l
    
    def list_str(self):
        l = []
        for i in self.file_to_list():
            l.append(i.split(" "))
        return l
    
    def list_int(self):
        l = self.list_str()
        m = []
        for i in range(len(l)):
            n = []
            for j in range(len(l[i])):
                n.append(float(l[i][j]))
            m.append(n)
        return m

    
    def __str__(self):
        return self.read_file()


doc = Extract("test.txt")
print(doc.list_int())