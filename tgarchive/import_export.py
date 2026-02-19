import json
import os
import zipfile
import logging
from .db import DB, User, Message, Media
import openpyxl
from datetime import datetime
import py7zr
import rarfile

class ImportExport:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.message_id = 1  # counter for message ids

    def import_downloads(self, downloads_dir):
        if not os.path.exists(downloads_dir):
            logging.error(f"Downloads directory {downloads_dir} not found")
            return

        for file in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, file)
            if file.endswith('.zip'):
                self.import_zip(file_path)
            elif file.endswith('.7z'):
                self._extract_7z(file_path)
            elif file.endswith('.rar'):
                self._extract_rar(file_path)
            elif file.endswith('.csv'):
                self._parse_csv(file_path)
            elif file.endswith('.xlsx'):
                self._parse_xlsx(file_path)
            elif file.endswith('.txt'):
                self._parse_txt(file_path)

        logging.info("Downloads import completed")

    def _extract_7z(self, file_path):
        try:
            with py7zr.SevenZipFile(file_path, mode='r') as z:
                z.extractall('temp_extract')
            self._parse_exports('temp_extract')
        except Exception as e:
            logging.warning(f"Failed to extract {file_path}: {e}")

    def _extract_rar(self, file_path):
        try:
            with rarfile.RarFile(file_path, 'r') as rf:
                rf.extractall('temp_extract')
            self._parse_exports('temp_extract')
        except Exception as e:
            logging.warning(f"Failed to extract {file_path}: {e}")

    def _parse_csv(self, file_path):
        import csv
        chat_name = os.path.basename(file_path).replace('.csv', '')
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    if cell.strip():
                        category = self.categorize(cell)
                        user = User(id=0, username='Importer', first_name='Importer', last_name='', tags=[], avatar=None)
                        self.db.insert_user(user)
                        message = Message(
                            id=self.message_id,
                            type='message',
                            date=datetime(2023, 1, 1, 0, 0, 0),
                            edit_date=None,
                            content=cell.strip(),
                            reply_to=None,
                            user=user,
                            media=None,
                            category=category
                        )
                        self.db.insert_message(message)
                        self.message_id += 1
        self.db.commit()
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.message_id = 1  # counter for message ids

    def categorize(self, text):
        text = text.lower()
        if 't.me/' in text or '@' in text or 'чат' in text:
            return 'tg channels'
        elif 'beeline' in text or 'билайн' in text:
            if 'сотрудник' in text or 'employer' in text:
                return 'beeline сотрудники'
            elif 'интернет' in text or 'inet' in text:
                return 'beeline интернет'
            elif 'gaming' in text or 'игра' in text:
                return 'beeline игры'
            else:
                return 'beeline номера'
        elif any(char.isdigit() for char in text) and len(text) < 20 and ('+' in text or text.startswith('7') or text.startswith('8')):
            return 'номера'
        elif 'sex' in text or 'секс' in text:
            return 'секс группы'
        elif 'впис' in text or 'invite' in text:
            return 'вписки'
        else:
            return 'другое'

    def import_zip(self, zip_path):
        if not os.path.exists(zip_path):
            logging.error(f"ZIP file {zip_path} not found")
            return

        import subprocess
        import shutil

        temp_dir = 'temp_import'
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        if zip_path.endswith('.zip'):
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(temp_dir)
        elif zip_path.endswith('.rar'):
            subprocess.run(['unrar', 'x', zip_path, temp_dir], check=True)
        elif zip_path.endswith('.7z'):
            subprocess.run(['7z', 'x', zip_path, f'-o{temp_dir}'], check=True)
        else:
            logging.error(f"Unsupported archive format: {zip_path}")
            return

        self._parse_exports(temp_dir)
        logging.info("Import completed")

    def _parse_exports(self, base_dir):
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file == 'result.json':
                    chat_dir = os.path.dirname(os.path.join(root, file))
                    chat_name = os.path.basename(chat_dir)
                    self._parse_chat(chat_name, os.path.join(root, file))
                elif file.endswith('.txt'):
                    self._parse_txt(os.path.join(root, file))
                elif file.endswith('.xlsx'):
                    self._parse_xlsx(os.path.join(root, file))

    def _parse_chat(self, chat_name, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for msg in data.get('messages', []):
            user = User(
                id=msg.get('from_id', 0),
                username=msg.get('from', ''),
                first_name=msg.get('from', ''),
                last_name='',
                tags=[],
                avatar=None
            )
            self.db.insert_user(user)

            category = self.categorize(msg.get('text', ''))
            message = Message(
                id=msg.get('id', 0),
                type='message',
                date=datetime.fromisoformat(msg.get('date', '2023-01-01T00:00:00')),
                edit_date=None,
                content=msg.get('text', ''),
                reply_to=msg.get('reply_to_message_id'),
                user=user,
                media=None,
                category=category
            )
            self.db.insert_message(message)

        self.db.commit()

    def _parse_txt(self, file_path):
        chat_name = os.path.basename(file_path).replace('.txt', '')
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        user = User(id=0, username='Importer', first_name='Importer', last_name='', tags=[], avatar=None)
        self.db.insert_user(user)

        for line in lines:
            line = line.strip()
            if line:
                category = self.categorize(line)
                message = Message(
                    id=self.message_id,
                    type='message',
                    date=datetime(2023, 1, 1, 0, 0, 0),
                    edit_date=None,
                    content=line,
                    reply_to=None,
                    user=user,
                    media=None,
                    category=category
                )
                self.db.insert_message(message)
                self.message_id += 1

        self.db.commit()

    def _parse_xlsx(self, file_path):
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        chat_name = os.path.basename(file_path).replace('.xlsx', '')

        user = User(id=0, username='Importer', first_name='Importer', last_name='', tags=[], avatar=None)
        self.db.insert_user(user)

        for row in sheet.iter_rows(values_only=True):
            for cell in row:
                if cell:
                    category = self.categorize(str(cell))
                    message = Message(
                        id=self.message_id,
                        type='message',
                        date=datetime(2023, 1, 1, 0, 0, 0),
                        edit_date=None,
                        content=str(cell),
                        reply_to=None,
                        user=user,
                        media=None,
                        category=category
                    )
                    self.db.insert_message(message)
                    self.message_id += 1

        self.db.commit()