import ajmc_iiif
import os
import pathlib
import shutil
import wand.image


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
        self.commentary_ids = ajmc_iiif.PUBLIC_DOMAIN_COMMENTARY_IDS

    def copy_full_size_image(self, commentary_id: str, png: pathlib.Path) -> str:
        full_size_dir = (
            self.iiif_directory / commentary_id / png.stem / "full" / "max" / "0"
        )

        full_size = full_size_dir / "default.png"
        full_size_dir.mkdir(parents=True, exist_ok=True)

        return shutil.copyfile(png, str(full_size))

    def create_derivatives(self):
        for commentary_id in self.commentary_ids:
            pngs_dir = self._base_directory / commentary_id / "images" / "png"

            for png in pngs_dir.iterdir():
                if png.suffix == ".png":
                    self.copy_full_size_image(commentary_id, png)
                    self.create_thumbnail(commentary_id, png)

    def create_thumbnail(self, commentary_id: str, png: pathlib.Path):
        thumbnail_dir = (
            self.iiif_directory / commentary_id / png.stem / "full" / "250," / "0"
        )

        thumbnail = thumbnail_dir / "default.png"
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

        with wand.image.Image(filename=png) as img:
            # resize image to a height of 250 px,
            # retaining the aspect ratio
            img.transform(resize="x250")
            img.save(filename=thumbnail)
