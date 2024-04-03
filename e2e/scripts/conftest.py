import http.server
import socketserver
import threading
from typing import Generator

from pytest import fixture

from .fixtures import html_sources


@fixture
def http_server_fixture() -> Generator[str, None, None]:

    class Handler(http.server.SimpleHTTPRequestHandler):
        def serve_page(self, page: str) -> None:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))

        def do_GET(self) -> None:
            if self.path == "/" or self.path == "/index.html":
                self.serve_page(html_sources.index_0_source)
            elif self.path == "/index1.html":
                self.serve_page(html_sources.index_1_source)
            elif self.path == "/page0.html":
                self.serve_page(html_sources.page_0_source)
            elif self.path == "/page1.html":
                self.serve_page(html_sources.page_1_source)
            elif self.path == "/page2.html":
                self.serve_page(html_sources.page_2_source)
            elif self.path == "/page3.html":
                self.serve_page(html_sources.page_3_source)
            elif self.path == "/page4.html":
                self.serve_page(html_sources.page_4_source)
            elif self.path == "/page5.html":
                self.serve_page(html_sources.page_5_source)
            else:
                self.send_error(404)

    with socketserver.TCPServer(("localhost", 0), Handler) as httpd:
        port = httpd.server_address[1]
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()
        yield f"http://localhost:{port}"
        httpd.shutdown()
        server_thread.join()
