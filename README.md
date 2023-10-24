# Trello Archiver

This bunch of scripts is used to archive Trello boards allowing you to view them locally whenever you go offline.

## Installation

1. Install [Python 3](https://www.python.org/downloads/).

2. Clone this repository.

```console
git clone https://github.com/LeeeeT/trello-archiver && cd trello-archiver
```

3. Install dependencies.

```console
pip install -r requirements.txt
```

## Usage

1. Create a new Trello API key [here](https://trello.com/app-key).
2. Create a new Trello Token https://trello.com/1/authorize?scope=read&expiration=never&name=archiver&key=REPLACE_WITH_YOUR_API_KEY&response_type=token.
3. Save your API key and token in a file named `.env` in the root of this repository (see `.env.example`).
4. Run the script.

```console
> python download.py
Enter the json filename: boards/trello.json  # where to save the board
Enter the board url: https://trello.com/b/b0j4wlfp/tst  # copy from your browser
```

It will start downloading the board and all the attachments. It may take a while depending on the size of the board. You can keep as many boards as you want.

5. Open `index.html` in your browser.
6. Select your board json file in the top right corner. You will see the board with all the cards and attachments. You can do steps 5 and 6 every time you want to view any of your saved boards (even without the internet connection).
