
from http.server import BaseHTTPRequestHandler, HTTPServer
from graphql import graphql_sync, GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString, format_error, parse
import json


databases = [
    {'id': '1', 'title': 'Post 1', 'content': 'Content 1'},
    {'id': '2', 'title': 'Post 2', 'content': 'Content 2'},
    {'id': '3', 'title': 'Post 3', 'content': 'Content 3'},
    {'id': '4', 'title': 'Post 4', 'content': 'Content 4'},
    {'id': '5', 'title': 'Post 5', 'content': 'Content 5'}
]


# Mendefinisikan tipe GraphQL Post yang memiliki tiga bidang: 'id', 'title', dan 'content'. Setiap bidang menggunakan tipe GraphQLField dengan tipe data GraphQLString
post_type = GraphQLObjectType(
    name='Post',
    fields={
        'id': GraphQLField(GraphQLString),
        'title': GraphQLField(GraphQLString),
        'content': GraphQLField(GraphQLString)
    }
)

root_type = GraphQLObjectType(
    name='Query',
    fields={
        'databases': GraphQLField(post_type, resolve=lambda obj, info: databases),
        'welcomeMessage': GraphQLField(GraphQLString, resolve=lambda obj, info: 'Selamat datang di Tugas 2 GraphQL!')
    }
)

# Mendefinisikan skema GraphQL dengan menggunakan tipe root root_type.
schema = GraphQLSchema(query=root_type)


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        if self.path == '/graphql':
            content_length = int(self.headers['Content-Length'])
            request_string = self.rfile.read(content_length).decode('utf-8')
            request = parse(request_string)
            result = graphql_sync(schema, request)
            response = {'data': result.data, 'errors': [format_error(error) for error in result.errors]}
            self._set_response()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write(b'Not found')

# Fungsi ini digunakan untuk menjalankan server HTTP pada alamat dan port tertentu (dalam contoh ini, alamat kosong dan port 8888).
# Objek HTTPServer dibuat dengan menggunakan alamat server dan kelas RequestHandler.

def run_server():
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Menjalankan server GraphQL di 8888...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
