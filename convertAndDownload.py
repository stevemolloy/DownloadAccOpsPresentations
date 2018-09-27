from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():
    """
    Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    files = service.files()

    # Get all folders under the AccOps folder
    results = files.list(q="'1QL9gcfBoz4pE9U9oDDrc-mOwXRYR0bxk' in parents")
    results = results.execute()
    for i in results.get('files', []):
        print(i['name'])
        # Get all presentation files under this folder
        query = "'" + i['id'] + "' in parents"
        query += " and mimeType='application/vnd.google-apps.presentation'"
        n = files.list(q=query)
        n = n.execute()
        for j in n.get('files', []):
            # Now j is a presentation file
            print('\t' + j['name'] + " :: " + j['id'])
            pdf = files.export(fileId=j['id'], mimeType='application/pdf')
            pdf = pdf.execute()
            with open('output/'+j['name'] + '.pdf', 'wb') as f:
                f.write(pdf)


if __name__ == '__main__':
    main()
