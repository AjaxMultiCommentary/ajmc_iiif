import ajmc_iiif.commentaries as commentaries
import ajmc_iiif.iiif as iiif

def main():
    public = commentaries.prepare_commentaries(public_domain=True)
    public.create_derivatives()


# if __name__ == "__main__":
#     main()
