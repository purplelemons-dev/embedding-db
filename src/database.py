from json import loads
from typing import Literal
from pickle import dump as pkl_dump, load as pkl_load
import numpy as np


class DB:
    tables: dict[str, dict[list[float], str]]

    def __init__(self):
        try:
            with open("data/tables.pkl", "rb") as file:
                self.tables = pkl_load(file)
        except:
            self.tables = {}
            self.save()

    def save(self):
        try:
            with open("data/tables.pkl", "wb") as file:
                pkl_dump(self.tables, file)
        except:
            print("Error saving database")

    def add_table(self, table_name: str):
        self.tables[table_name] = {}
        self.save()

    def add_vector(
        self, table_name: str, vector: list[float], text: str, save: bool = True
    ):
        if not self.tables.get(table_name):
            self.add_table(table_name)
        if any(i == text for i in self.tables[table_name].values()):
            raise ValueError("Text already exists in the table")
        self.tables[table_name][text] = vector
        if save:
            self.save()

    def add_vectors(
        self, table_name: str, vectors: list[list[float]], texts: list[str]
    ):
        print(len(vectors), len(texts))
        assert len(vectors) == len(
            texts
        ), "Length of vectors and texts must be the same"
        if not self.tables.get(table_name):
            self.add_table(table_name)
        for vector, text in zip(vectors, texts):
            self.add_vector(table_name, vector, text, save=False)
        self.save()

    def delete_table(self, table_name: str):
        if table_name in self.tables:
            del self.tables[table_name]
            self.save()

    def get_n_neighbors(
        self,
        table_name: str,
        vector: list[float] | str,
        metric: Literal["dot_product", "euclidean", "cosine"] = "cosine",
        n: int = 10,
    ) -> list[dict[str, str | float]]:
        if isinstance(vector, str):
            vector = loads(vector)
        sorted_vectors: list[tuple[int, float]] = []

        for i, (text, v) in enumerate(self.tables[table_name].items()):
            # v = loads(v)
            if metric == "dot_product":
                similarity = np.dot(vector, v)
            elif metric == "euclidean":
                similarity = np.linalg.norm(np.array(vector) - np.array(v))
            elif metric == "cosine":
                similarity = np.dot(vector, v) / (
                    np.linalg.norm(vector) * np.linalg.norm(v)
                )
            else:
                raise ValueError("Invalid metric")
            sorted_vectors.append((text, similarity))
        sorted_vectors.sort(key=lambda x: x[1], reverse=True)
        return [
            {"text": text, "similarity": similarity}
            for text, similarity in sorted_vectors[:n]
        ]
