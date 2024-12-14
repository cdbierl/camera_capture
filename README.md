# Camera Capture Utility
Capture image from network camera and upload to Google Drive folder. FFMPEG is used to capture a frame from the video feed and saves it to an image. drive_upload.py then uploads image file to Google Drive folder.

## Setup
* Download credentials from Google Console, save to credentials.json
* Run drive_upload.py once to create token.json.

## Usage
./camera_capture.sh backyard config.json

## References
* https://developers.google.com/drive/api/quickstart/python