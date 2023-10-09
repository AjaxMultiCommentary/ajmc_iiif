import ajmc.commons.file_management as ajmc_files
import ajmc.commons.variables as ajmc_variables
import ajmc_iiif.iiif as iiif
import os
import pathlib
import shutil
import wand.image


COMMENTARIES_METADATA_SHEET_ID = "1jaSSOF8BWij0seAAgNeGe3Gtofvg9nIp_vPaSj5FtjE"
COMMENTARIES_METADATA_SHEET_NAME = "bibliographic_metadata"

IIIF_DIRECTORY = f"{os.path.dirname(os.path.realpath(__file__))}/../iiif"


def prepare_commentaries(public_domain=True):
    if public_domain is True:
        return PublicDomainCommentaries()
    else:
        raise NotImplementedError


class PublicDomainCommentaries:
    def __init__(self) -> None:
        self._base_directory = pathlib.Path(
            os.getenv("PUBLIC_DOMAIN_COMMENTARIES_BASE_DIR", "")
        )
        self.iiif_directory = pathlib.Path(IIIF_DIRECTORY)
        self.commentary_ids = ajmc_variables.PD_COMM_IDS
        self.metadata = ajmc_files.read_google_sheet(
            COMMENTARIES_METADATA_SHEET_ID, COMMENTARIES_METADATA_SHEET_NAME
        )

    def copy_full_size_image(
        self, commentary_id: str, png: pathlib.Path
    ) -> wand.image.Image:
        full_size_dir = (
            self.iiif_directory / commentary_id / png.stem / "full" / "max" / "0"
        )

        full_size = full_size_dir / "default.png"
        full_size_dir.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(png, str(full_size))

        return wand.image.Image(filename=full_size)
    
    def create_derivatives_for_commentary(self, commentary_id):
        metadata = self.metadata[self.metadata.id == commentary_id]

        if metadata.empty:
            print(f"No metadata found for {commentary_id}. Skipping.")
            return

        pngs_dir = self._base_directory / commentary_id / "images" / "png"

        manifest = iiif.Manifest(commentary_id, metadata)

        for png in pngs_dir.iterdir():
            if png.suffix == ".png":
                full_size = self.copy_full_size_image(commentary_id, png)
                thumbnail = self.create_thumbnail(commentary_id, png)

                canvas = iiif.Canvas(commentary_id, png, full_size)
                info = iiif.Info(commentary_id, png.stem, [full_size, thumbnail])

    def create_derivatives(self):
        for commentary_id in self.commentary_ids:
            self.create_derivatives_for_commentary(commentary_id)

    def create_thumbnail(
        self, commentary_id: str, png: pathlib.Path
    ) -> wand.image.Image:
        thumbnail_dir = (
            self.iiif_directory / commentary_id / png.stem / "full" / "250," / "0"
        )

        thumbnail = thumbnail_dir / "default.png"
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

        img = wand.image.Image(filename=png)

        # resize image to a height of 250 px,
        # retaining the aspect ratio
        img.transform(resize="x250")
        img.save(filename=thumbnail)

        return img


def repl():
    commentaries = PublicDomainCommentaries()
    commentaries.create_derivatives()