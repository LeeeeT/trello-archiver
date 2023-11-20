import os
import re
import requests
import dotenv
from pathlib import Path
from json import loads


class Client:
    def __init__(self, api_key, token):
        self._api_key = api_key
        self._token = token

    def request(self, url):
        return requests.get(url, headers={"Authorization": f"OAuth oauth_consumer_key=\"{self._api_key}\", oauth_token=\"{self._token}\""}, allow_redirects=True)


def get_board_url():
    return re.fullmatch(r"(https://trello.com/b/(?:[^/]+))(?:/[^/]*)?", input("Enter the board url: ")).group(1)


def get_json_filename():
    return input("Enter the json filename: ")


def board_url_to_json_url(board_url):
    return board_url + ".json"


def save(path, content, *args, **kwargs):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, *args, **kwargs) as file:
        file.write(content)


def parse_attachment_url(url):
    match = re.fullmatch(r"https://trello.com/1/cards/([^/]+)/attachments/([^/]+)/download/(.+)", url)
    return match.group(1), match.group(2), match.group(3)


def parse_preview_url(url):
    match = re.fullmatch(r"https://trello.com/1/cards/([^/]+)/attachments/([^/]+)/previews/([^/]+)/download/([^/]+)", url)
    return match.group(1), match.group(2), match.group(3), match.group(4)


class Archiver:
    def __init__(self, client, archive_directory):
        self._client = client
        self._archive_directory = archive_directory

    def archive(self, json_filename, json_text):
        json = loads(json_text)

        for card in json["cards"]:
            for attachment in card["attachments"]:
                if attachment["isUpload"]:
                    card_id, attachment_id, name = parse_attachment_url(attachment["url"])
                    path = Path(self._archive_directory) / attachment_id / name
                    print(f"Downloading {attachment_id}/{name}...")
                    save(path, self._client.request(attachment["url"]).content, "wb")
                    json_text = json_text.replace(attachment["url"], f"{self._archive_directory}/{attachment_id}/{name}")

                    match attachment["previews"]:
                        case [_, preview, *_]:
                            card_id, attachment_id, preview_id, name = parse_preview_url(preview["url"])
                            path = Path(self._archive_directory) / preview_id / name
                            print(f"Downloading {preview_id}/{name}...")
                            save(path, self._client.request(preview["url"]).content, "wb")
                            json_text = json_text.replace(preview["url"], f"{self._archive_directory}/{preview_id}/{name}")

        save(Path(json_filename), json_text, "w", encoding="utf-8")


def api_key_and_token_exist():
    dotenv.load_dotenv()
    return "API_KEY" in os.environ and "TOKEN" in os.environ


def ask_api_key_and_token():
    api_key = input("Enter your API key: ")
    print(f"Open the following url and copy the token:\nhttps://trello.com/1/authorize?scope=read&expiration=never&name=archiver&key={api_key}&response_type=token")
    token = input("Enter your token: ")
    return api_key, token


def save_api_key_and_token(api_key, token):
    dotenv.set_key(".env", "API_KEY", api_key)
    dotenv.set_key(".env", "TOKEN", token)


def ask_and_save_api_key_and_token():
    api_key, token = ask_api_key_and_token()
    save_api_key_and_token(api_key, token)
    return api_key, token


def load_api_key_and_token():
    dotenv.load_dotenv()
    return os.environ["API_KEY"], os.environ["TOKEN"]


def get_api_key_and_token():
    if not api_key_and_token_exist():
        ask_and_save_api_key_and_token()
    return load_api_key_and_token()
       


def main():
    api_key, token = get_api_key_and_token()

    client = Client(api_key, token)
    archiver = Archiver(client, "res")

    board_url = get_board_url()
    json_filename = get_json_filename()

    archiver.archive(json_filename, client.request(board_url_to_json_url(board_url)).text)


main()
