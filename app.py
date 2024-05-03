import http
from http.server import BaseHTTPRequestHandler
import json

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse

from game_engine import GameEngine;

game_engine = GameEngine()


# Using Lab 2 as a basis for my code
class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse(self.path)
        # check if the web-pages matches the list
        if parsed.path == '/':
            self.serve_file("index.html", "text/html")
        elif parsed.path in ['/game']:
            self.serve_file("game.html", "text/html")
        elif parsed.path in ['/styles.css']:
            self.serve_file("styles.css", "text/css")
        elif parsed.path in ['/script.js']:
            self.serve_file("script.js", "text/javascript")
        elif parsed.path in ['/pool_game_background.jpg']:
            self.serve_file("pool_game_background.jpg", "image/jpeg")
        else:
            self.send_error(404, "Get - File Not Found [" + parsed.path + "]")


    def do_POST(self):
        parsed  = urlparse(self.path)
        if parsed.path in ['/shoot']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))
            game_engine.shoot(params)
            self._set_response(200, content_type='application/json')
            data = {
                "animation_frames": list(map(lambda obj: obj.frame_svg(), game_engine.shoot_animation_data)),
                "next_player": game_engine.get_next_player(),
                "player_one_ball_set": game_engine.player_one_ball_set,
                "player_two_ball_set": game_engine.player_two_ball_set,
                "player_one_ball_set_name": game_engine.player_one_ball_set_name,
                "player_two_ball_set_name": game_engine.player_two_ball_set_name,
                "game_over": game_engine.game_over,
                "winner": game_engine.winner,
                "winner_name": game_engine.get_player_name(game_engine.winner)
            }
            self.wfile.write(json.dumps(data).encode())
        elif parsed.path in ['/start-new-game']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))
            game_engine.create_new_game(params['game_name'], params['player_one'], params['player_two'])
            data = game_engine.table.frame_svg(False)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({
                "rack": data,
                "current_player": game_engine.current_player,
                "game_name": game_engine.game.gameName,
                "player_one": game_engine.game.player1Name,
                "player_two": game_engine.game.player2Name
            }), 'utf-8'))
        else:
            self.send_error(404, "Post - File Not Found [" + parsed.path + "]")
    

    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as file:
                self._set_response(status_code=200, content_type=content_type)
                file_content = file.read()
                self.wfile.write(file_content)
        except FileNotFoundError:
            self.send_error(404, "Open - File Not Found [" + filename + "]")
            
            
    def _set_response(self, status_code=200, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()


def run(server_class=http.server.HTTPServer, handler_class=MyHandler, port=57301):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        run(port=port)
    else:
        run()
