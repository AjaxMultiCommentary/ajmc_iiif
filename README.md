AjMC IIIF
------

This repository represents a bare-bones, static, compliance level-0 implementation of the [IIIF Image API](https://iiif.io/api/image/3.0/).

In practice, that means that it is little more than a few scripts that fetch the base images, generate thumbnails, half-sized derivatives, and `info.json` files, and place each item in a directory that maps onto the IIIF Image API.

The IIIF Image API requires URIs in the following format:

```
{scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}
```

Omitting `scheme` and `server` (as these are implementation details that are easy to change --- but perhaps imagine `https://ajmc.org`), the URLs in this repository might look like the following:

```
/ajmc-iiif/commentary_identifier/image_identifier/full/max/0/default.jpg
```

Note that as of 2017, URNs can contain `/` characters as part of their identifiers, meaning that it should be valid for us to use the full path to an image on the server. See https://datatracker.ietf.org/doc/html/rfc8141#section-2.

## Examples

Let's say we want to create IIIF derivatives for Wecklein's commentary on _Ajax_.

### Full-sized images

First, we'll need to copy of the full-sized images to their base location:

```bash
# copy images from /path/to/Wecklein1894/images{/pdf,png}/*.{pdf,png} to
# ./ajmc-iiif/Wecklein1894/{image_id}/full/max/0/default.jpg
```

### Thumbnails
 
From these base images, we can generate thumbnail-sized derivatives:

```bash
# imagemagick script for thumbnail-sized outputs --- they go in
# ./ajmc-iiif/Wecklein1894/{image_id}/full/125,/0/default.jpg
```

### info.json

We can also put together an [info.json](https://iiif.io/api/image/3.0/#52-technical-properties) file, which should be accessible for each `image_id` at `/ajmc-iiif/Wecklein1894/{image_id}/info.json`.

```json
{
  "@context": "http://iiif.io/api/image/3/context.json",
  "id": "https://ajmc.org/ajmc-iiif/Wecklein1894/{image_id}",
  "type": "ImageService3",
  "protocol": "http://iiif.io/api/image",
  "profile": "level0",
  "width": 6000,
  "height": 4000,
}
```

In fact, we only need to plug in the `id`, `width`, and `height` attributes --- the other attributes are static strings requird by the IIIF spec.

We should probably include a [`sizes`](https://iiif.io/api/image/3.0/#53-sizes), which is a list of objects with `height` and `width` pairs --- in our case, we'll start with just two elements, one for the full-sized image and one for the thumbnail.  


### Presentation API Manifest

We will probably want to generate a manifest.json for each commentary that adheres to the [IIIF Presentation API] specification.


See https://iiif.io/api/presentation/3.0/#b-example-manifest-response.


# License

GNU AGPLv3 --- see [LICENSE].