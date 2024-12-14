import time
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def upload_file(
    service,
    filepath: str,
    filename: str,
    folder_id: str,
    mimetype: str,
    overwrite=False,
) -> str:
    file = None

    try:
        if overwrite:
            # list the file inside of the folder
            results = (
                service.files()
                .list(q=f"'{folder_id}' in parents", fields="files(id, name)")
                .execute()
            )
            files = results.get("files", [])
            for f in files:
                if f.get("name") == filename:
                    file = f

        media = MediaFileUpload(filepath, mimetype=mimetype)

        if file is not None:
            file = (
                service.files()
                .update(fileId=file.get("id"), media_body=media)
                .execute()
            )
        else:
            file_metadata = {"name": filename, "parents": [folder_id]}
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )

    except HttpError as error:
        print(f"An error occurred: {error}")

    return file.get("id")


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        uploads = 0

        while True:
            time.sleep(0.5)

            if not os.path.exists(args.filepath):
                print("Waiting for file to exist...")
                continue

            upload_file(
                service,
                filepath=args.filepath,
                filename=args.filename,
                folder_id=args.folder_id,
                mimetype=args.mime_type,
                overwrite=True,
            )
            uploads += 1

            print(f"{uploads} uploads...")

    except Exception as ex:
        print(f"An error occurred: {ex}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("sample_upload")
    parser.add_argument(
        "--filepath", help="Path to file", type=str, action="store", required=True
    )
    parser.add_argument(
        "--filename",
        help="Destination file name",
        type=str,
        action="store",
        required=True,
    )
    parser.add_argument(
        "--mime-type",
        help="File mime-type",
        type=str,
        action="store",
        default="image/jpeg",
    )
    parser.add_argument(
        "--folder-id",
        help="Destination folder id",
        type=str,
        action="store",
        required=True,
    )
    args = parser.parse_args()

    main()
