import os
import re
import requests
from dotenv import load_dotenv
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


def save(path, content, mode):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode) as file:
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
                    path = Path(__file__).parent / self._archive_directory / attachment_id / name
                    print(f"Downloading {attachment_id}/{name}...")
                    save(path, self._client.request(attachment["url"]).content, "wb")
                    json_text = json_text.replace(attachment["url"], f"{self._archive_directory}/{attachment_id}/{name}")

                    match attachment["previews"]:
                        case [_, preview, *_]:
                            card_id, attachment_id, preview_id, name = parse_preview_url(preview["url"])
                            path = Path(__file__).parent / self._archive_directory / preview_id / name
                            print(f"Downloading {preview_id}/{name}...")
                            save(path, self._client.request(preview["url"]).content, "wb")
                            json_text = json_text.replace(preview["url"], f"{self._archive_directory}/{preview_id}/{name}")

        save(Path(json_filename), json_text, "w")


def main():
    load_dotenv()

    api_key = os.environ["API_KEY"]
    token = os.environ["TOKEN"]

    client = Client(api_key, token)
    archiver = Archiver(client, "res")

    archiver.archive(get_json_filename(), client.request(board_url_to_json_url(get_board_url())).text)


main()
