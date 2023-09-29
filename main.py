import ajmc_iiif.commentaries

if __name__ == "__main__":
    public = ajmc_iiif.commentaries.prepare_commentaries(public_domain=True)
    public.create_derivatives()
