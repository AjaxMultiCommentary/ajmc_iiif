import ajmc_iiif.g_drive as drive


if __name__ == "__main__":
    client = drive.GDrive()
    items = client.list_files()

    if not items:
        print('No files found.')
    else:    
        print('Files:')
        
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
