#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

import json

import config
from db import database

clients = {}

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(origin, args):
        return True

    def open(self):
        clients[self] = {
            "admin" : False,
            "send_current_data":True
        };

    def on_message(self, message):
        try:
            json_array = json.loads(message);
        except:
            self.write_message('{"status":400,"statusText":"c\'ant parse JSON"}')
            return;
        if json_array['mode'] == "authenticate":
            # { "mode":"authenticate", "authenticate":{"key":"YOUR KEY"} }
            if json_array['authenticate']['key'] == config.api_key:
                clients[self]['admin'] = True;
                self.write_message('{"status":200}')
            else:
                self.write_message('{"status":401,"statusText":"wrong key"}')
        elif json_array['mode'] == "update_current_data":
            # { "mode":"update_current_data", "update_current_data":{YOUR DATA} }
            if clients[self]['admin'] == True:
                tmp = {
                    "mode":"update_current_data",
                    "update_current_data":json_array['update_current_data']
                }
                for client in clients.keys():
                    if client != self and clients[client]["send_current_data"] == True:
                        client.write_message(tmp)
                self.write_message('{"status":200}')
            else:
                self.write_message('{"status":403,"statusText":"please authenticate"}');
        else:
            self.write_message('{"status":400,"statusText":"bad request"}');

    def on_close(self):
        del(clients[self])

class APIHandler(tornado.web.RequestHandler):
    def get(request):
        request.set_header("Content-Type", "application/json; charset=UTF-8")
        try:
            getFrom = int(request.get_argument("from", strip=True, default=""));
            getTo = int(request.get_argument("to", strip=True, default=""));
        except:
            request.write('{"status":400,"statusText":"from and to are not correctly"}')
            return;
        try:
            steps = int(request.get_argument("steps", strip=True, default=""));
        except:
            steps = config.default_steps
        try:
            data = '{"data":"asd"}'
        except:
            request.write('{"status":500,"statusText":"can\'t get data from the database"}')
            return;
        try:
            request.write(data)
        except:
            request.write('{"status":500,"statusText":"unknown server error"}')
            return;

handlers = [
    (r'/', WebSocketHandler),
    (r'/api/getData', APIHandler)
]

def main():
    db = database(config.db_path)
    app = tornado.web.Application(handlers);
    app.listen(8888)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print ("");
        db.close();
        print ("Stop");

if __name__ == '__main__':
    main();
