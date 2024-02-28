from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from json import dumps, loads
from database import DB

db = DB()


class Handler(BaseHTTPRequestHandler):

    protocol_version = "HTTP/1.1"

    def send(self, status: int, data: str, content_type: str = "text/plain"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data.encode())

    def send_json(self, status: int, data: dict):
        self.send(status, dumps(data), "application/json")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = loads(body)
        if self.path == "/api/table":
            """
            {
                "table_name": str
            }
            """
            db.add_table(**data)
            self.send(200, "OK")

        elif self.path == "/api/vector/add":
            """
            {
                "table_name": str,
                "vector": float[]
                "text": str
            }
            """
            db.add_vector(**data)
            self.send(200, "OK")

        elif self.path == "/api/vectors/add":
            """
            {
                "table_name": str,
                "vectors": float[][],
                "texts": str[]
            }
            """
            db.add_vectors(**data)
            self.send(200, "OK")

        elif self.path == "/api/neighbors":
            """
            {
                "table_name": str,
                "vector": float[],
                "metric": "dot_product" | "euclidean" | "cosine",
                "n": int
            }
            """
            neighbors = db.get_n_neighbors(**data)
            self.send_json(200, neighbors)

        elif self.path == "/api/tables":
            self.send_json(200, {"tables": list(db.tables.keys())})

        elif self.path == "/api/table/delete":
            """
            {
                "table_name": str
            }
            """
            db.delete_table(**data)

        else:
            self.send(404, "Not Found")

    def do_GET(self):
        # list endpoints

        self.send_json(
            200,
            {
                "endpoints": [
                    {
                        "endpoint": "/api/table",
                        "method": "POST",
                        "description": "Add a table",
                        "body": {"table_name": "str"},
                    },
                    {
                        "endpoint": "/api/vector/add",
                        "method": "POST",
                        "description": "Add a vector to a table",
                        "body": {
                            "table_name": "str",
                            "vector": "float[]",
                            "text": "str",
                        },
                    },
                    {
                        "endpoint": "/api/vectors/add",
                        "method": "POST",
                        "description": "Add multiple vectors to a table",
                        "body": {
                            "table_name": "str",
                            "vectors": "float[][]",
                            "texts": "str[]",
                        },
                    },
                    {
                        "endpoint": "/api/neighbors",
                        "method": "POST",
                        "description": "Get the n neighbors of a vector in a table",
                        "body": {
                            "table_name": "str",
                            "vector": "float[]",
                            "metric": "dot_product | euclidean | cosine",
                            "n": "int",
                        },
                    },
                    {
                        "endpoint": "/api/tables",
                        "method": "POST",
                        "description": "Get all tables",
                        "response": {"tables": "str[]"},
                    },
                    {
                        "endpoint": "/api/table/delete",
                        "method": "POST",
                        "description": "Delete a table",
                        "body": {"table_name": "str"},
                    },
                ]
            },
        )


server = ThreadingHTTPServer(("0.0.0.0", 80), Handler)


def run_server():
    server.serve_forever()


if __name__ == "__main__":
    print("Server started at http://localhost:80")
    run_server()
