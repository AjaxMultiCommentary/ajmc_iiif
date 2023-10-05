import pandas
import pathlib
import wand.image

BASE_URL = "https://ajaxmulticommentary.github.io/ajmc_iiif"

"""
See https://iiif.io/api/presentation/3.0/#53-canvas for documentation
and examples.
"""


class Canvas:
    def __init__(
        self, commentary_id: str, filename: pathlib.Path, image: wand.image.Image
    ) -> None:
        pid = filename.stem.split("_")[1]
        label = f"p. {int(pid)}"

        self.id = f"{BASE_URL}/{commentary_id}/canvas/{pid}"
        self.canvas = {
            "id": self.id,
            "type": "Canvas",
            "label": {"none": [label]},
            "height": image.height,
            "width": image.width,
            "items": [
                {
                    "id": f"{BASE_URL}/{commentary_id}/content/{pid}/1",
                    "type": "AnnotationPage",
                    "items": [],
                }
            ],
            "annotations": [
                {
                    "id": f"{BASE_URL}/{commentary_id}/comments/{pid}/1",
                    "type": "AnnotationPage",
                    "items": [],
                }
            ],
        }


class Thumbnail:
    def __init__(
        self,
    ) -> None:
        pass


class Manifest:
    def __init__(self, commentary_id: str, metadata: pandas.DataFrame) -> None:
        author = f"{metadata.commentator_firstname.values[0]} {metadata.commentator_name.values[0]}"
        title = metadata.title.values[0]
        year = metadata.year.values[0]
        publisher = metadata.publisher.values[0]
        language = metadata.language.values[0]
        self.id = f"{BASE_URL}/{commentary_id}"

        self.manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": self.id,
            "@type": "sc:Manifest",
            "license": "https://github.com/AjaxMultiCommentary/ajmc_iiif/blob/main/LICENSE",
            "attribution": "Provided by the Ajax Multi-Commentary Project (AjMC)",
            "metadata": [
                {"label": "Author", "value": author},
                {"label": "Title", "value": title},
                {"label": "Published", "value": f"{publisher} {year}"},
                {"label": "Language", "value": language},
            ],
            "items": [
                {
                    "@id": f"{self.id}/sequence/normal",
                    "@type": "sc:Sequence",
                    "label": "Published Page Order",
                    "viewingDirection": "left-to-right",
                    "viewingHint": "paged",
                    "canvases": [],
                }
            ],
        }

    def append_canvas(self, canvas: Canvas):
        pass


class Collection:
    def __init__(
        self, collection_id: str, collection_label: str, collection_summary: str
    ) -> None:
        self.collection = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "id": f"{BASE_URL}/collections/{collection_id}",
            "type": "Collection",
            "label": {"en": [collection_label]},
            "summary": {"en": [collection_summary]},
            "requiredStatement": {
                "label": {"en": ["Attribution"]},
                "value": {"en": ["Provided by the Ajax Multi-Commentary Project"]},
            },
            "items": [],
        }

    def append_manifest(self, manifest: Manifest):
        pass


class Info:
    def __init__(
        self, commentary_id: str, image_id: str, images: list[wand.image.Image]
    ) -> None:
        self.commentary_id = commentary_id
        self.id = f"{BASE_URL}/{commentary_id}/{image_id}"
        self.image_id = image_id
        self.images = images
        self.info = {
            "@context": "http://iiif.io/api/image/3/context.json",
            "id": self.id,
            "type": "ImageService3",
            "protocol": "http://iiif.io/api/image",
            "profile": "level0",
            "width": images[0].width,
            "height": images[0].height,
            "sizes": [
                {"width": image.width, "height": image.height} for image in images
            ],
        }
