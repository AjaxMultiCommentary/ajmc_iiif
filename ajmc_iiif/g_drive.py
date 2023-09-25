import googleapiclient.discovery
import google.oauth2.service_account as g_service_account
import os

"""
On service accounts:
https://googleapis.dev/python/google-auth/latest/reference/google.oauth2.service_account.html

On the Drive API:
https://developers.google.com/drive/api/quickstart/python

Specifically, on the syntax of searches: https://developers.google.com/drive/api/guides/search-files
"""

SERVICE_NAME = "drive"
SERVICE_VERSION = "v3"

class GDrive:
    def __init__(self):
        credentials = g_service_account.Credentials.from_service_account_file(
            os.getenv("SERVICE_ACCOUNT_JSON_FILE"))
        self.client = googleapiclient.discovery.build(
            SERVICE_NAME,
            SERVICE_VERSION,
            credentials=credentials
        )

    def list_files(self):
        containing_folder_req = self.client.files().list( 
            fields="nextPageToken, files(id, name)",
            q = "mimeType = 'application/vnd.google-apps.folder' and name = 'commentaries_data'"
        ).execute()

        containing_folder = containing_folder_req.get('files', [])
        containing_folder_id = containing_folder[0].get('id')
        
        results = self.client.files().list(
            fields="nextPageToken, files(id, name)",
            q = f"mimeType = 'application/vnd.google-apps.folder' and '{containing_folder_id}' in parents"
        ).execute()

        items = results.get('files', [])

        return items

        
