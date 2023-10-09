import ajmc_iiif
import pathlib
import shutil
import wand.image


class Image:
    def __init__(
        self, commentary_id: str, image_path: pathlib.Path
    ):
        self.commentary_id = commentary_id
        self.path = image_path
        self.height = None
        self.width = None


class FullSize(Image):
    def __init__(
        self, commentary_id: str, image_path: pathlib.Path
    ):
        super().__init__(commentary_id, image_path)

        self.copy_full_size_image()

    def copy_full_size_image(self) -> None:
        full_size_dir = (
            ajmc_iiif.IIIF_DIRECTORY
            / self.commentary_id
            / self.path.stem
            / "full"
            / "max"
            / "0"
        )

        full_size = full_size_dir / "default.png"
        full_size_dir.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(self.path, str(full_size))

        with wand.image.Image(filename=full_size) as img:
            self.height = img.height
            self.width = img.width


class Thumbnail(Image):
    def __init__(
        self, commentary_id: str, image_path: pathlib.Path
    ):
        super().__init__(commentary_id, image_path)

        self.create_thumbnail()

    def create_thumbnail(self) -> None:
        thumbnail_dir = (
            ajmc_iiif.IIIF_DIRECTORY
            / self.commentary_id
            / self.path.stem
            / "full"
            / "250,"
            / "0"
        )

        thumbnail = thumbnail_dir / "default.png"
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

        with wand.image.Image(filename=self.path) as img:
            # resize image to a height of 250 px,
            # retaining the aspect ratio
            # calling img.transform() will modify
            # the img.{height,width} in-place
            img.transform(resize="x250")
            img.save(filename=thumbnail)

            self.height = img.height
            self.width = img.width
