#Writed by Kerem Demirtürk
class Triangle:
    def __init__(self):
        self.normal = [0.0, 0.0, 0.0]
        self.vertex = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

class Mesh:
    def __init__(self, name):
        self.triangles = list()
        self.importFromFile(name)
        self.setMinMax()
        self.moveToAxis()

    def importFromFile(self, name):
        f = open(name, "r")
        line = f.readline()
        while True:
            triangle = Triangle()

            # normal okunur
            line = f.readline()
            if line == '\n':
                continue
            if line[0:8] == 'endsolid':
                break
            words = line.split()[2:5]
            triangle.normal[0] = float(words[0])
            triangle.normal[1] = float(words[1])
            triangle.normal[2] = float(words[2])
            
            # outer loop okunur
            line = f.readline()
            
            # Vertexler okunur
            for i in range(0,3):
                line = f.readline()
                words = line.split()[1:4]
                triangle.vertex[i][0] = float(words[0])
                triangle.vertex[i][1] = float(words[1])
                triangle.vertex[i][2] = float(words[2])
            
            # end loop ve end facet okunur
            line = f.readline()
            line = f.readline()

            self.triangles.append(triangle)

        f.close()

    def exportToFile(self, name):
        f = open(name, 'w')
        f.write("solid AssimpScene\n")

        for triangle in self.triangles:
            f.write(" facet normal ")
            
            f.write(str(triangle.normal[0]) + " " + str(triangle.normal[1]) + " " + str(triangle.normal[2]) + "\n")
            f.write("  outer loop\n")
            for i in range(0,3):
                f.write("  vertex ")
                f.write(str(triangle.vertex[i][0]) + " " + str(triangle.vertex[i][1]) + " " + str(triangle.vertex[i][2]) + "\n")
            f.write("  endloop\n")
            f.write(" endfacet\n\n")

        f.write("endsolid AssimpScene\n")
        f.close()

    def printToConsole(self):
        for triangle in self.triangles:
            print("Normal: " , triangle.normal)
            print("Vertexler:" , triangle.vertex)

    def setMinMax(self):
        self.minX = self.triangles[0].vertex[0][0]
        self.maxX = self.triangles[0].vertex[0][0]
        self.minY = self.triangles[0].vertex[0][1]
        self.maxY = self.triangles[0].vertex[0][1]
        self.minZ = self.triangles[0].vertex[0][2]
        self.maxZ = self.triangles[0].vertex[0][2]

        for triangle in self.triangles:
            for i in range(0,3):
                if triangle.vertex[i][0] < self.minX:
                    self.minX = triangle.vertex[i][0]
                if triangle.vertex[i][0] > self.maxX:
                    self.maxX = triangle.vertex[i][0]
                if triangle.vertex[i][1] < self.minY:
                    self.minY = triangle.vertex[i][1]
                if triangle.vertex[i][1] > self.maxY:
                    self.maxY = triangle.vertex[i][1]
                if triangle.vertex[i][2] < self.minZ:
                    self.minZ = triangle.vertex[i][2]
                if triangle.vertex[i][2] > self.maxZ:
                    self.maxZ = triangle.vertex[i][2]

    def moveToAxis(self):
        # X, Y, Z eksenine taşıma
        for triangle in self.triangles:
            for i in range(0,3):
                triangle.vertex[i][0] -= self.minX
                triangle.vertex[i][1] -= self.minY
                triangle.vertex[i][2] -= self.minZ

    def move(self, x):
        print("taşıyorum...\n")
        # X, Y, Z eksenine taşıma
        for triangle in self.triangles:
            for i in range(0,3):
                triangle.vertex[i][0] += x
        print("taşıdım...\n")

def merge(mesh1, mesh2):
    mesh2.move(mesh1.maxX - mesh1.minX)
    for otherTriangle in mesh2.triangles:
        mesh1.triangles.append(otherTriangle)
    mesh1.maxX += mesh2.maxX - mesh2.minX

def main():
    mesh1 = Mesh("files/linux.stl")
    mesh2 = Mesh("files/ironman.stl")
    mesh3 = Mesh("files/pythonbadge.stl")

    merge(mesh1, mesh2)
    merge(mesh1, mesh3)

    mesh1.exportToFile("pythonbadgge.stl")
main()


