import ajmc_iiif.commentaries as commentaries

def main():
    public = commentaries.prepare_commentaries(public_domain=True)
    public.create_derivatives()


if __name__ == "__main__":
    main()
