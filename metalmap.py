import numpy as np

class MetalMap:
    def __init__(self):
        self.matrix = np.zeros((3,2))
        self.originCoords = (0, 0)
        self.cellSize = 1
        self.decal_x = 0
        self.decal_y = 0
        self.value = 0

    def addColR(self, n):
        self.matrix = np.c_[self.matrix, np.zeros((np.shape(self.matrix)[0],n))]

    def addColL(self, n):
        self.matrix = np.c_[np.zeros((np.shape(self.matrix)[0],n)),self.matrix]

    def addRowU(self, n):
        self.matrix = np.r_[np.zeros((n, np.shape(self.matrix)[1])), self.matrix]

    def addRowD(self,n):
        self.matrix = np.r_[self.matrix, np.zeros((n, np.shape(self.matrix)[1]))]
    
    def addToMatrix(self, value, x, y):
        if 0 <= x < np.shape(self.matrix)[0] and 0 <= y < np.shape(self.matrix)[1]:
            self.matrix[x + self.decal_x, y + self.decal_y] = value

        else:
            if 0 < x >= np.shape(self.matrix)[0]:
                self.addRowD(x-np.shape(self.matrix)[0]+1)
            if 0 < y >= np.shape(self.matrix)[1]:
                self.addColR(y-np.shape(self.matrix)[1]+1)
            if x < 0:
                self.decal_x += abs(x)
                self.originCoords = (self.decal_x, self.decal_y)
                self.addRowU(abs(x))
            
            if y < 0:
                self.decal_y += abs(y)
                self.addColL(abs(y))
            self.matrix[x + self.decal_x, y + self.decal_y] = value
            self.originCoords = (self.decal_x, self.decal_y)
        

    def addData(self,position,value):
        if position[0] % self.cellSize == 0:
            x = position[0] // self.cellSize
        else:
            x = position[0] // self.cellSize +1

        if position[1] % self.cellSize == 0:
            y = position[1] // self.cellSize
        else:
            y = position[1] // self.cellSize +1

        self.value += value
        self.count += 1
        if self.count == self.SEND_FREQUENCY:
            self.addToMatrix(self.value/self.count, x ,y)
            self.sendMap()
            self.count = 0
            self.value = 0

    def __str__(self):
        return str(self.matrix)


