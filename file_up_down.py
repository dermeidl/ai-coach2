import dropbox
import os
dbx = dropbox.Dropbox(os.environ.get('DROPBOX_TOKEN'))


def upload_file_to_dropbox(file, file_to):
  try:
    dbx.files_upload(file.read(), file_to)
    # return filename to save in Database at user
    return 'uploaded'
  except dropbox.exceptions.ApiError as err:
    print("Error while uploading to Dropbox: ", err)


def downlad_file_from_dropbox(file_from):
  try:
    #return the file for futher processing
    metadata, responce = dbx.files_download(file_from)
    return responce.content.decode('utf-8')
  except dropbox.exceptions.ApiError as err:
    print("Error while uploading to Dropbox: ", err)