import ajmc_iiif
import ajmc_iiif.image as image
import json
import pandas
import pathlib
import wand.image

BASE_URL = "https://iiif.ajmc.ch"


"""
See https://iiif.io/api/presentation/3.0/#53-canvas for documentation
and examples.
"""


class Canvas:
    type_ = "Canvas"

    def __init__(
        self, commentary_id: str, filename: pathlib.Path, image: wand.image.Image
    ) -> None:
        self.commentary_id = commentary_id
        self.pid = filename.stem.split("_")[1]
        self.id = f"{BASE_URL}/{commentary_id}/canvas/{self.pid}"
        self.type = self.type_
        self.label = {"none": [f"p. {int(self.pid)}"]}
        self.height = image.height
        self.width = image.width
        self.items = []
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations.append(
            {
                "id": f"{BASE_URL}/{self.commentary_id}/comments/{self.pid}/1",
                "type": "AnnotationPage",
                "items": [annotation],
            }
        )
        pass

    def add_item(self, item):
        self.items.append(
            {
                "id": f"{BASE_URL}/{self.commentary_id}/content/{self.pid}/1",
                "type": "AnnotationPage",
                "items": [item],
            }
        )
        pass

    def json(self):
        return json.dumps(self.__dict__)


class Manifest:
    def __init__(self, commentary_id: str, metadata: pandas.DataFrame) -> None:
        author = f"{metadata.commentator_firstname.values[0]} {metadata.commentator_name.values[0]}"
        title = metadata.title.values[0]
        year = metadata.year.values[0]
        publisher = metadata.publisher.values[0]
        language = metadata.language.values[0]

        self.id = f"{BASE_URL}/{commentary_id}"
        self.type = "Manifest"
        self.label = {"en": [title]}
        self.metadata = [
            {"label": "Author", "value": author},
            {"label": "Title", "value": title},
            {"label": "Published", "value": f"{publisher} {year}"},
            {"label": "Language", "value": language},
        ]

        self.license = (
            "https://github.com/AjaxMultiCommentary/ajmc_iiif/blob/main/LICENSE",
        )
        self.attribution = ("Provided by the Ajax Multi-Commentary Project (AjMC)",)
        self.items = [
            {
                "@id": f"{self.id}/sequence/normal",
                "@type": "sc:Sequence",
                "label": "Published Page Order",
                "viewingDirection": "left-to-right",
                "viewingHint": "paged",
                "canvases": [],
            }
        ]

    def append_canvas(self, canvas: Canvas):
        self.items.append(canvas.__dict__)

    def json(self):
        return json.dumps(
            {"@context": "http://iiif.io/api/presentation/2/context.json"}
            | self.__dict__
        )


class Collection:
    def __init__(
        self, collection_id: str, collection_label: str, collection_summary: str
    ) -> None:
        self.id = f"{BASE_URL}/collections/{collection_id}"
        self.type = "Collection"
        self.label = {"en": [collection_label]}
        self.summary = {"en": [collection_summary]}
        self.requiredStatement = {
            "label": {"en": ["Attribution"]},
            "value": {"en": ["Provided by the Ajax Multi-Commentary Project"]},
        }
        self.items = []

    def append_manifest(self, manifest: Manifest):
        self.items.append(manifest.__dict__)

    def json(self):
        return json.dumps(
            {"@context": "http://iiif.io/api/presentation/3/context.json"}
            | self.__dict__
        )


class Info:
    type_ = "ImageService3"
    protocol = "http://iiif.io/api/image"
    profile = "level0"
    iiif_keys = [
        "id",
        "protocol", 
        "profile", 
        "type", 
        "height",
        "width",
        "sizes",
        "preferredFormats"
    ]

    def __init__(
        self, commentary_id: str, image_id: str, images: list[image.Image]
    ) -> None:
        self.commentary_id = commentary_id
        self.id = f"{BASE_URL}/{commentary_id}/{image_id}"
        self.protocol = "http://iiif.io/api/image"
        self.profile = "level0"
        self.image_id = image_id
        self.type = self.type_
        self.height = images[0].height
        self.width = images[0].width
        self.sizes = [
            {"width": image.width, "height": image.height} for image in images
        ]
        #self.tiles = [
        #    {"width": image.width, "height": image.height, "scaleFactors": [1]} for image in images
        #]
        self.preferredFormats = ["png"]

    def json(self):
        iiif_info = {k: v for k, v in self.__dict__.items() if k in self.iiif_keys}
        return json.dumps(
            {"@context": "http://iiif.io/api/image/3/context.json"} | iiif_info
        )

    def write(self):
        with open(
            ajmc_iiif.IIIF_DIRECTORY / self.commentary_id / self.image_id / "info.json",
            "w",
        ) as f:
            f.write(self.json())
