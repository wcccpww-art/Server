
# tg-archive

![favicon](https://user-images.githubusercontent.com/547147/111869334-eb48f100-89a4-11eb-9c0c-bc74cdee197a.png)

**tg-archive** is an enhanced tool for exporting Telegram group chats into static websites, preserving chat history like mailing list archives. Includes categories, sidebar navigation, and import from various formats.

**IMPORTANT:** Original tool by knadh. Enhanced with categories, import, and bot integration.

## Preview
The [@fossunited](https://tg.fossunited.org) Telegram group archive.

![image](https://user-images.githubusercontent.com/547147/111869398-44188980-89a5-11eb-936f-01d98276ba6a.png)

## How it works
tg-archive uses the [Telethon](https://github.com/LonamiWebs/Telethon) Telegram API client to periodically sync messages from a group to a local SQLite database (file), downloading only new messages since the last sync. It then generates a static archive website of messages to be published anywhere. Enhanced with categorization, import from ZIP/TXT/XLSX, and a Telegram bot for automated file processing.

## Features
- Periodically sync Telegram group messages to a local DB.
- Download user avatars locally.
- Download and embed media (files, documents, photos).
- Renders poll results.
- Use emoji alternatives in place of stickers.
- Single file Jinja HTML template for generating the static site.
- Year / Month / Day indexes with deep linking across pages.
- "In reply to" on replies with links to parent messages across pages.
- RSS / Atom feed of recent messages.
- **NEW:** Automatic categorization of messages (tg channels, номера, секс группы, etc.).
- **NEW:** Sidebar with categories for easy navigation.
- **NEW:** Import from ZIP archives containing JSON, TXT, XLSX files.
- **NEW:** Telegram bot for downloading and processing files automatically.

## Install
- Get [Telegram API credentials](https://my.telegram.org/auth?to=apps). Normal user account API and not the Bot API.
  - If this page produces an alert stating only "ERROR", disconnect from any proxy/vpn and try again in a different browser.

- Install with: `uv pip install tg-archive` (tested with Python 3.13.2).

For development:
```bash
git clone https://github.com/wcccpww-art/Server.git
cd Server
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

### Basic Usage
1. `tg-archive --new --path=mysite` (creates a new site. `cd` into mysite and edit `config.yaml`).
2. `tg-archive --sync` (syncs data into `data.sqlite`).
   - Note: First time connection will prompt for your phone number + a Telegram auth code sent to the app. On successful auth, a `session.session` file is created. DO NOT SHARE this session file publicly as it contains the API authorization for your account.
3. `tg-archive --build` (builds the static site into the `site` directory, which can be published).

### Import from Files
- `tg-archive --import-zip path/to/archive.zip` (imports data from ZIP containing JSON/TXT/XLSX files, categorizes automatically).

### Telegram Bot
- Edit `bot.py` with your bot token.
- Run `python bot.py` to start the bot.
- Send files to the bot; it will download, import if ZIP, and delete after processing.
- Site updates automatically.

### Customization
Edit the generated `template.html` and static assets in the `./static` directory to customize the site. Sidebar includes categories for navigation.

### Notes
- The sync can be stopped (Ctrl+C) any time to be resumed later.
- Setup a cron job to periodically sync messages and re-publish the archive.
- Downloading large media files and long message history from large groups continuously may run into Telegram API's rate limits. Watch the debug output.
- Categories are auto-detected: 'tg channels' for links, 'номера' for numbers, etc.

Licensed under the MIT license.
