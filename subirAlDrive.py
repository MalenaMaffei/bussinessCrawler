from __future__ import print_function

from apiclient import errors
from apiclient.http import MediaFileUpload
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

WEBSITES = '0B6hqnDHYpCqKeWVmVC1CdnJBd2c'
EMAILS = '0B6hqnDHYpCqKVHJTQm9oemtmLVU'
def insert_file(service, title, description, parent_id, mime_type, filename):
    """Insert new file.

    Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
    Returns:
    Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype=mime_type)

    body = {'parents': [parent_id], 'title': title, 'description': description, 'name': filename, 'mimeType': 'application/vnd.google-apps.spreadsheet'}


    try:

        fiahl = service.files().create(body=body, media_body=media_body).execute()
        return fiahl
    # except errors.HttpError, error:
    #   print ('An error occurred: %s' % error)
    #   return None
    except errors.HttpError:
        print ('An error occurred')
        return None






def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(filename, title, desc, folder):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

# TODO hacer bien esto
    if folder == 'web':
        folder_var = WEBSITES
    elif folder == 'email':
        folder_var = EMAILS


    # def insert_file(service, title, description, parent_id, mime_type, filename):

    res = insert_file(service, title, desc, folder_var, 'text/csv', filename)
    print(res)



if __name__ == '__main__':
    main()
