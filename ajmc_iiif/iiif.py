import pandas
import wand.image


class Info:
    def __init__(
        self, commentary_id: str, image_id: str, images: list[wand.image.Image]
    ) -> None:
        self.commentary_id = commentary_id
        self.image_id = image_id
        self.images = images
        self.info = {
            "@context": "http://iiif.io/api/image/3/context.json",
            "id": f"https://ajaxmulticommentary.github.io/ajmc_iiif/{commentary_id}/{image_id}",
            "type": "ImageService3",
            "protocol": "http://iiif.io/api/image",
            "profile": "level0",
            "width": images[0].width,
            "height": images[0].height,
            "sizes": [
                {"width": image.width, "height": image.height} for image in images
            ],
        }


class Manifest:
    def __init__(self, commentary_id: str, metadata: pandas.DataFrame) -> None:
        author = f"{metadata.commentator_firstname.values[0]} {metadata.commentator_name.values[0]}"
        title = metadata.title.values[0]
        year = metadata.year.values[0]
        publisher = metadata.publisher.values[0]
        language = metadata.language.values[0]
        manifest_id = f"https://ajaxmulticommentary.github.io/ajmc_iiif/{commentary_id}"

        self.manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": manifest_id,
            "@type": "sc:Manifest",
            "license": "https://github.com/AjaxMultiCommentary/ajmc_iiif/blob/main/LICENSE",
            "attribution": "Provided by the Ajax Multi-Commentary Project (AjMC)",
            "metadata": [
                {"label": "Author", "value": author},
                {"label": "Title", "value": title},
                {"label": "Published", "value": f"{publisher} {year}"},
                {"label": "Language", "value": language},
            ],
            "sequences": [
                {
                    "@id": f"{manifest_id}/sequence/normal",
                    "@type": "sc:Sequence",
                    "label": "Published Page Order",
                    "viewingDirection": "left-to-right",
                    "viewingHint": "paged",
                    "canvases": [],
                }
            ],
        }

    def append_canvas(self):
        pass
