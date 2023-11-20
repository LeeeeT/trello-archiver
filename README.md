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
2. Run the script.

```console
> python download.py
Enter your API key: 1234567890abcdef1234567890abcdef  # your key from step 1
# it will give you a link to create a token
Enter your token: ... # your token from the link
Enter the board url: https://trello.com/b/b0j4wlfp/tst  # copy from your browser
Enter the json filename: boards/trello.json  # where to save the board
```

Once you created an api key and a token, they will be saved in a file `.env`, so you don't have to enter them again.

It will start downloading the board and all the attachments. It may take a while depending on the size of the board. You can keep as many boards as you want.

3. Open `index.html` in your browser.
4. Select your board json file in the top right corner. You will see the board with all the cards and attachments. You can do steps 3 and 4 every time you want to view any of your saved boards (even without the internet connection).
