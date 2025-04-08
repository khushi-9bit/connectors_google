import pdfplumber
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from io import BytesIO

# Load credentials
creds = Credentials.from_authorized_user_file('token.json')
service = build('drive', 'v3', credentials=creds)

# File name
file_name = "geo_chap_9.pdf"

# Search for the file
results = service.files().list(
    q=f"name='{file_name}' and mimeType='application/pdf'",
    spaces='drive',
    fields="files(id, name)"
).execute()

files = results.get('files', [])

if not files:
    print("No file present of this name.")
else:
    file = files[0]
    file_id = file['id']
    print(f"Found file: {file['name']}")

    # Download the PDF to memory
    request = service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    # Use pdfplumber to read the PDF from memory
    fh.seek(0)
    with pdfplumber.open(fh) as pdf:
        print("\n📄 PDF Content:\n")
        for page in pdf.pages:
            print(page.extract_text())
