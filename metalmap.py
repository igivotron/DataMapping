import numpy as np

class MetalMap:
    def __init__(self):
        self.matrix = -np.ones((3, 2))
        self.originCoords = (0, 0)
        self.cellSize = 1
        self.decal_x = 0
        self.decal_y = 0
        self.values = np.array([])
        self.count = 0
        self.SEND_FREQUENCY = 1
        self.data = {}
        self.x = 0
        self.y = 0

    def addColR(self, n):
        self.matrix = np.c_[self.matrix, -np.ones((np.shape(self.matrix)[0], n))]

    def addColL(self, n):
        self.matrix = np.c_[-np.ones((np.shape(self.matrix)[0], n)), self.matrix]

    def addRowU(self, n):
        self.matrix = np.r_[-np.ones((n, np.shape(self.matrix)[1])), self.matrix]

    def addRowD(self, n):
        self.matrix = np.r_[self.matrix, -np.ones((n, np.shape(self.matrix)[1]))]

    def addToMatrix(self, value, x, y):

        if 0 <= x < np.shape(self.matrix)[0] and 0 <= y < np.shape(self.matrix)[1]:
            self.matrix[x + self.decal_x, y + self.decal_y] = value

        else:
            if 0 < x >= np.shape(self.matrix)[0]:
                self.addRowD(x - np.shape(self.matrix)[0] + 1)
            if 0 < y >= np.shape(self.matrix)[1]:
                self.addColR(y - np.shape(self.matrix)[1] + 1)
            if x < 0:
                self.decal_x += abs(x)
                self.originCoords = (self.decal_x, self.decal_y)
                self.addRowU(abs(x))

            if y < 0:
                self.decal_y += abs(y)
                self.addColL(abs(y))
            self.matrix[x + self.decal_x, y + self.decal_y] = value
            self.originCoords = (self.decal_x, self.decal_y)

    def addData(self, position, value, dico=True):
        self.count += 1
        x = (position[0] + (self.cellSize / 2)) // self.cellSize
        y = (position[1] + (self.cellSize / 2)) // self.cellSize

        if dico:    # Rajoute les données dans un dictionnaire
            self.data[position] = value

        if x == self.x and y == self.y:
            self.values = np.append(self.values, value)

        else:
            if len(self.values) > 0:    # self.x et self.y sont de base à 0, 0 donc lorsque qu'on exécute le programme, il veut envoyer la moyenne d'une liste vide
                self.addToMatrix(np.mean(self.values), int(self.x), int(self.y))
            self.x = x
            self.y = y
            self.values = np.array([value])
        
        if self.count == self.SEND_FREQUENCY:
            self.addToMatrix(np.mean(self.values), int(self.x), int(self.y))
            self.count = 0
            #self.sendMap()

    def clearData(self):
        self.data = {}

    def clearMatrix(self):
        self.decal_x = 0
        self.decal_y = 0
        self.x = 0
        self.y = 0
        self.matrix = -np.ones((3, 2))
        self.values = [0]

    def changePrecision(self, newprecision):
        self.cellSize = newprecision
        self.clearMatrix()
        for i in self.data:
            self.addData(i, self.data[i], dico=False)
        self.clearData()


    def __str__(self):
        return str(self.matrix)
