import googleapiclient.discovery
import google.oauth2.service_account as g_service_account
import os

from ajmc_iiif import PUBLIC_DOMAIN_COMMENTARY_IDS

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

    def list_files_where(self, q: str):
        files_req = self.client.files().list( 
            fields = "nextPageToken, files(id, name)",
            q = q
        ).execute()
    
        return files_req.get('files', [])

    def get_folder_id(self, folder_name: str):
        folder = self.list_files_where(f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'")
        return folder[0].get('id')
    
    def get_subfolder_id(self, parent_id: str, folder_name: str):
        subfolder = self.list_files_where(
            f"mimeType = 'application/vnd.google-apps.folder' and '{parent_id}' in parents and name = '{folder_name}'"
        )

        if len(subfolder) == 0:
            return None

        return subfolder[0].get('id')

    def list_public_domain_commentary_dir(self, public_domain_commentary_id: str):
        commentary_folder_id = self.get_folder_id(public_domain_commentary_id)
        image_folder_id = self.get_subfolder_id(commentary_folder_id, "images")
        png_folder_id = self.get_subfolder_id(image_folder_id, "png")
        pngs = self.list_files_where(f"'{png_folder_id}' in parents")

        return pngs

    def list_public_domain_commentary_dirs(self):
        return [self.list_public_domain_commentary_dir(public_domain_commentary_id)
                for public_domain_commentary_id in PUBLIC_DOMAIN_COMMENTARY_IDS]


        
