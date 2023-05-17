from http.server import BaseHTTPRequestHandler, HTTPServer
import json

databases = [
    {'id': 1, 'title': 'Post 1', 'content': 'Content 1'},
    {'id': 2, 'title': 'Post 2', 'content': 'Content 2'},
    {'id': 3, 'title': 'Post 3', 'content': 'Content 3'},
    {'id': 4, 'title': 'Post 4', 'content': 'Content 4'},
    {'id': 5, 'title': 'Post 5', 'content': 'Content 5'}
]

class RequestHandler(BaseHTTPRequestHandler):

# digunakan untuk mengatur respons HTTP dengan mengirimkan kode status, header, dan tipe konten.
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
# digunakan untuk mengurai data permintaan JSON yang diterima dari klien.
    def _parse_request_data(self):
        return json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))

    def do_GET(self):
        if self.path == '/databases':
            self._set_response()
            self.wfile.write(json.dumps(databases).encode('utf-8'))
        elif self.path == '/':
            self._set_response()
            self.wfile.write(b'Selamat datang di Tugas 2 GraphQL!')
        else:
            self._set_response(404)
            self.wfile.write(b'url yang anda inputkan salah, periksa kembali....')

# Ketika perintah '/databases' dijalankan, tambahkan data baru ke databases dan tampilkan ID nya saja sebagai respons
    def do_POST(self):
        if self.path == '/databases':
            data = self._parse_request_data()
            post_id = len(databases) + 1
# format yang digunakan untuk menambahkan data baru
            new_post = {'id': post_id, 'title': data['title'], 'content': data['content']}
            databases.append(new_post)
            self._set_response(201)
            self.wfile.write(json.dumps({'id': post_id}).encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write(b'Not found')

    def do_PUT(self):
        if self.path.startswith('/databases/'):
# apabila kita akses /databases/ maka akan ada tindakan ambil ID dari path dan perbarui data dengan data permintaan PUT
            post_id = int(self.path.split('/')[2])
            data = self._parse_request_data()
            for post in databases:
# format untuk melakukan update pada data di databases
                if post['id'] == post_id:
                    post['title'] = data['title']
                    post['content'] = data['content']
                    self._set_response()
                    self.wfile.write(b'Data telah di update')
                    return
            self._set_response(404)
            self.wfile.write(b'data tidak ditemukan')
        else:
            self._set_response(404)
            self.wfile.write(b'Not found')

    def do_DELETE(self):
        if self.path.startswith('/databases/'):
# apabila kita akses /databases/ maka akan ada tindakan ambil ID dari path melakukan penghapusan data
            post_id = int(self.path.split('/')[2])
            for post in databases:
                if post['id'] == post_id:
                    databases.remove(post)
                    self._set_response()
                    self.wfile.write(b'Post deleted')
                    return
            self._set_response(404)
            self.wfile.write(b'Post not found')
        else:
            self._set_response(404)
            self.wfile.write(b'Not found')

def run_server():
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Menjalankan server dummy di 8888...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()


#     {
#   "title": "Post 6",
#   "content": "Content 6"
# }

# {
#   "title": "Post 7",
#   "content": "Content 7"
# }
