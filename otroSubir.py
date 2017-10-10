from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

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

#Set up a credentials object I think
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', ['https://www.googleapis.com/auth/drive'])
creds = get_credentials()
#Now build our api object, thing
drive_api = build('drive', 'v3', credentials=creds)

file_name = "test"
print ("Uploading file " + file_name + "...")

#We have to make a request hash to tell the google API what we're giving it
body = {'name': file_name, 'mimeType': 'application/vnd.google-apps.document'}

#Now create the media file upload object and tell it what file to upload,
#in this case 'test.html'
media = MediaFileUpload('test.html', mimetype = 'text/html')

#Now we're doing the actual post, creating a new file of the uploaded type
fiahl = drive_api.files().create(body=body, media_body=media).execute()

#Because verbosity is nice
print ("Created file '%s' id '%s'." % (fiahl.get('name'), fiahl.get('id')))
