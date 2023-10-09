import ajmc.commons.file_management as ajmc_files
import ajmc.commons.variables as ajmc_variables
import ajmc_iiif.iiif as iiif
import ajmc_iiif.image as image
import os
import pathlib

from tqdm import tqdm


COMMENTARIES_METADATA_SHEET_ID = "1jaSSOF8BWij0seAAgNeGe3Gtofvg9nIp_vPaSj5FtjE"
COMMENTARIES_METADATA_SHEET_NAME = "bibliographic_metadata"


def prepare_commentaries(public_domain=True):
    if public_domain is True:
        return PublicDomainCommentaries()
    else:
        raise NotImplementedError


class Commentary:
    def __init__(self, base_directory: pathlib.Path, commentary_id: str) -> None:
        self.id = commentary_id
        self.pngs_dir = base_directory / self.id / "images" / "png"

    def create_derivatives(self):
        for png in tqdm(self.pngs_dir.iterdir(), desc=self.id):
            if png.suffix == ".png":
                full_size = image.FullSize(self.id, png)
                thumbnail = image.Thumbnail(self.id, png)
                info = iiif.Info(self.id, png.stem, [full_size, thumbnail])
                info.write()


class PublicDomainCommentaries:
    def __init__(self) -> None:
        self._base_directory = pathlib.Path(
            os.getenv("PUBLIC_DOMAIN_COMMENTARIES_BASE_DIR", "")
        )
        self.commentary_ids = ajmc_variables.PD_COMM_IDS
        self.metadata = ajmc_files.read_google_sheet(
            COMMENTARIES_METADATA_SHEET_ID, COMMENTARIES_METADATA_SHEET_NAME
        )

    def create_derivatives(self):
        for commentary_id in tqdm(self.commentary_ids, desc="all commentaries"):
            commentary = Commentary(self._base_directory, commentary_id)
            commentary.create_derivatives()
