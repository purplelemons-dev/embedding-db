import numpy as np
from numpy.typing import NDArray
from json import load, dump, dumps
from typing import Literal


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

    def add_vector(self, table_name: str, vector: NDArray[np.float64]):
        index = self.table_names.index(table_name)
        self.vectors[index].append(vector)
        self.save()

    def get_n_neighbors(
        self,
        table_name: str,
        vector: NDArray[np.float64],
        metric: Literal["dot_product", "euclidean", "cosine"] = "dot_product",
        n: int = 10,
    ):
        index = self.table_names.index(table_name)
        sorted_vectors: list[tuple[int, float]] = []
        if metric == "dot_product":
            for i, v in enumerate(self.vectors[index]):
                sorted_vectors.append((i, np.dot(v, vector)))
            sorted_vectors.sort(key=lambda x: x[1], reverse=True)
        elif metric == "euclidean":
            for i, v in enumerate(self.vectors[index]):
                sorted_vectors.append((i, np.linalg.norm(v - vector)))
            sorted_vectors.sort(key=lambda x: x[1])
        elif metric == "cosine":
            for i, v in enumerate(self.vectors[index]):
                sorted_vectors.append(
                    (
                        i,
                        np.dot(v, vector)
                        / (np.linalg.norm(v) * np.linalg.norm(vector)),
                    )
                )
            sorted_vectors.sort(key=lambda x: x[1], reverse=True)
        else:
            raise ValueError(f"Invalid metric: {metric}")

        vectors = [self.vectors[index][i] for i, _ in sorted_vectors[:n]]
        final = []
        table_index = self.table_names.index(table_name)
        for i, v in enumerate(vectors):
            hashed = hash(v.tolist())
            final.append(
                {
                    "index": sorted_vectors[i][0],
                    "distance": sorted_vectors[i][1],
                    "hash": hashed,
                    "text": self.tables[table_index][str(hashed)],
                }
            )
        return final

