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
        with wand.image.Image(filename=self.path) as img:
            self.height = img.height
            self.width = img.width

            max_dir = (
                ajmc_iiif.IIIF_DIRECTORY
                / self.commentary_id
                / self.path.stem
                / "full"
                / "max"
                / "0"
            )

            max_img = max_dir / "default.png"
            max_dir.mkdir(parents=True, exist_ok=True)

            shutil.copyfile(self.path, str(max_img))

            full_size_dir = (
                ajmc_iiif.IIIF_DIRECTORY
                / self.commentary_id
                / self.path.stem
                / "full"
                / f"{self.width},{self.height}"
                / "0"
            )

            full_size = full_size_dir / "default.png"
            full_size_dir.mkdir(parents=True, exist_ok=True)

            shutil.copyfile(self.path, str(full_size))


class Thumbnail(Image):
    def __init__(
        self, commentary_id: str, image_path: pathlib.Path
    ):
        super().__init__(commentary_id, image_path)

        self.create_thumbnail()

    def create_thumbnail(self) -> None:
        with wand.image.Image(filename=self.path) as img:
            # resize image to a height of 250 px,
            # retaining the aspect ratio
            # calling img.transform() will modify
            # the img.{height,width} in-place
            img.transform(resize="x250")

            self.height = img.height
            self.width = img.width

            thumbnail_dir = (
                ajmc_iiif.IIIF_DIRECTORY
                / self.commentary_id
                / self.path.stem
                / "full"
                / f"{self.width},{self.height}"
                / "0"
            )

            thumbnail = thumbnail_dir / "default.png"
            thumbnail_dir.mkdir(parents=True, exist_ok=True)

            img.save(filename=thumbnail)
