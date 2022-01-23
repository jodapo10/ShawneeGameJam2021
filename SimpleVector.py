from typing import List, Tuple


class Vector:
    def __init__(self, *data):
        self.data = []
        for i in data:
            if isinstance(i, (float, int)):
                self.data.append(float(i))
            elif isinstance(i, Vector):
                V = i.copy()
                for index in range(V.dim):
                    self.data.append(float(V[index]))
                for index in range(len(i)):
                    if isinstance(index, (int, float)):
                        self.data.append(float(i[index]))
            elif isinstance(i, (List, Tuple)):
                for index in range(len(i)):
                    if isinstance(index, (float, int)):
                        self.data.append(float(i[index]))
            else:
                raise TypeError(" - Vector __init__ error. - ")

        self.dim = len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(value, (float, int)):
            self.data[index] = float(value)
        else:
            raise TypeError(" - Vector __setitem__ error. - ")

    def __len__(self):
        return len(self.data)

    def __str__(self):
        string = "Vector{0} [".format(self.dim)
        for i in range(self.dim):
            if i == self.dim - 1:
                string += " {0} ]".format(self[i])
            else:
                string += " {0},".format(self[i])
        return string

    def __eq__(self, other):
        if isinstance(other, Vector) and self.dim == other.dim:
            for i in range(self.dim):
                if self[i] != other[i]:
                    return False
            return True
        return False

    def __mul__(self, scalar):
        if isinstance(scalar, (float, int)):
            product = self.copy()
            for i in range(self.dim):
                product[i] *= scalar
            return product
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

    def __add__(self, otherVector):
        if isinstance(otherVector, Vector) and self.dim == otherVector.dim:
            tmpSum = self.copy()
            for i in range(self.dim):
                tmpSum[i] += otherVector[i]
            return tmpSum
        else:
            raise TypeError(" - Vector __add__ error. - ")

    def __sub__(self, otherVector):
        return self + -otherVector

    def __neg__(self):
        return self * -1

    def __truediv__(self, scalar):
        if isinstance(scalar, (float, int)) and scalar != 0:
            quotient = self.copy()
            for i in range(self.dim):
                quotient[i] /= float(scalar)
            return quotient
        elif scalar == 0:
            raise ValueError("Cannot divide by 0.")
        else:
            raise TypeError(" - Vector __truediv__ error. - ")

    def copy(self):
        tmpData = []
        for i in self.data:
            tmpData.append(i)
        return Vector(*tmpData)

    @property
    def i(self):
        tmpList = []
        for i in range(self.dim):
            tmpList.append(int(self[i]))
        return tuple(tmpList)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, newValue):
        if isinstance(newValue, (float, int)):
            self[0] = float(newValue)
        else:
            raise TypeError(" - Vector @x.setter error. - ")

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, newValue):
        if isinstance(newValue, (float, int)):
            self[1] = float(newValue)
        else:
            raise TypeError(" - Vector @y.setter error. - ")
