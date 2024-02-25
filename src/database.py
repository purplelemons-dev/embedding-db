
import numpy as np
from numpy.typing import NDArray
from json import load, dump, dumps

class DB:
    vectors: list[list[NDArray[np.float64]]]
    tables: list[dict[str, str]]
    "`[index: {hash: text}]`"
    table_names: list[str]

    def __init__(self):
        try:
            with open("data/vectors.npy", "rb") as file:
                self.vectors = np.load(file)
        except:
            self.vectors = np.array([], dtype=np.float64)

        try:
            with open("data/tables.json", "r") as file:
                self.tables = load(file)
        except:
            self.tables = []

        try:
            with open("data/table_names.json", "r") as file:
                self.table_names = load(file)
        except:
            self.table_names = []

    def save(self):
        with open("data/vectors.npy", "wb") as file:
            np.save(file, self.vectors)

        with open("data/tables.json", "w") as file:
            dump(self.tables, file)

        with open("data/table_names.json", "w") as file:
            dump(self.table_names, file)

    def add_table(self, table_name: str):
        self.tables.append({table_name: ""})
        self.table_names.append(table_name)
        self.vectors.append(np.array([], dtype=np.float64))
        self.save()

    def add_vector(self, table_name:str, vector: NDArray[np.float64]):
        index = self.table_names.index(table_name)
        self.vectors[index].append(vector)
        self.save()

        
        