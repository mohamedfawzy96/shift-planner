import numpy as np


class TableService:
    def __init__(self,
                 file: str):
        self.raw_data = np.genfromtxt(file, delimiter=',', skip_header=True)
        self.matrix = self.raw_data[:, 1:]

    def get_matrix(self):
        return self.matrix

    def get_drivers(self):
        return self.raw_data[:, 0]
