def upload_file(directory, file_to_upload):
    with open(directory + file_to_upload.name, 'wb+') as destination:
        for chunk in file_to_upload.chunks():
            destination.write(chunk)