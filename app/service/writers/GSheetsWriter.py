import os
from pathlib import Path
from service.IFaces.IWriter import IWriter
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from service.schemas.Post import Post
from google_auth_oauthlib.flow import InstalledAppFlow


class GSheetsWriter(IWriter):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    TableId = "1lHDOonBSaWOdZVZo92ZlM6cCwvc4c4Eg3pJ1BGK1KtM"

    def __init__(self, creds_path: Path, token_path: Path):
        self.creds = self._auth(creds_path, token_path)

        self.service = build("sheets", "v4", credentials=self.creds)

        self._write_header()

    def _auth(self, creds_path: Path, token_path: Path):
        if os.path.exists(token_path):
            return Credentials.from_authorized_user_file(
                token_path, self.SCOPES)

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, self.SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

            return creds

    def _write_header(self):
        self.service.spreadsheets().values().update(
            spreadsheetId=self.TableId,
            range="A1",
            valueInputOption="RAW",
            body={
                "values": [["id", "title", "body", "user_id"]]
            }).execute()

    async def write_post(self, data: Post):
        ids = self.service.spreadsheets().values().get(
            spreadsheetId=self.TableId, range="A2:A",
            majorDimension="COLUMNS").execute()['values'][0]

        if data.id in ids:
            return
        body = {"values": [[data.id, data.title, data.body, data.user_id]]}
        self.service.spreadsheets().values().append(spreadsheetId=self.TableId,
                                                    range="A1",
                                                    valueInputOption="RAW",
                                                    body=body).execute()
