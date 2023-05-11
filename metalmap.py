import numpy as np


class MetalMap:
    def __init__(self):
        self.matrix = -np.ones((3, 2))
        self.originCoords = (0, 0)
        self.cellSize = 1
        self.decal_x = 0
        self.decal_y = 0
        self.values = np.array([0])
        self.count = 0
        self.SEND_FREQUENCY = 1
        self.data = {}

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

    def addData(self, position, value):

        self.count += 1
        x = (position[0] + (self.cellSize / 2)) // self.cellSize
        y = (position[1] + (self.cellSize / 2)) // self.cellSize
        self.x = x
        self.y = y
        self.data[position] = value

        if x == self.x and y == self.y:
            self.values = np.append(self.values, value)

        else:
            self.addToMatrix(np.mean(self.values[1:]), int(self.x), int(self.y))
            self.x = x
            self.y = y
            self.values = np.array([0])
            self.values = np.append(self.values, value)

        if self.count == self.SEND_FREQUENCY:
            self.addToMatrix(np.mean(self.values[1:]), int(x), int(y))

            self.count = 0
            # self.sendMap()

    def clearMatrix(self):
        self.matrix = -np.ones((3, 2))

    def clearData(self):
        self.data = {}

    def clearDecal(self):
        self.decal_x = 0
        self.decal_y = 0

    def changePrecision(self, newprecision):
        self.cellSize = newprecision
        self.clearMatrix()
        self.clearDecal()
        for i in self.data:
            self.addData(i, self.data[i])

    def __str__(self):
        return str(self.matrix)
