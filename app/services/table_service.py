import numpy as np


class TableService:
    base_dir = './data/'

    def __init__(self,
                 file: str):
        self.raw_data = np.genfromtxt(self.base_dir + file, delimiter=',', skip_header=True)
        self.matrix = self.raw_data[:, 1:]

    def get_matrix(self):
        return self.matrix

    def get_drivers(self):
        return self.raw_data[:, 0]

    def get_drivers_for_index(self, index):
        col = self.matrix[:, index]
        indexes = np.argwhere(col > 0)
        return self.get_drivers()[indexes].T.flatten()
