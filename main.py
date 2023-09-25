import ajmc_iiif.g_drive as drive


if __name__ == "__main__":
    client = drive.GDrive()
    items = client.list_public_domain_commentary_dirs()

    print(items)
