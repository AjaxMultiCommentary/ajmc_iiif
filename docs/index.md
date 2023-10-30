Ajax Multi-Commentary IIIF Images API
------

Note: For now, this API only implements the [Image API](https://iiif.io/api/image/3.0/). Support for the [Presentation API](https://iiif.io/api/presentation/3.0/) might arrive in the future.

## How to use the API

The API supports level-0 compliance endpoints:

Every request starts the same:

```
https://ajaxmulticommentary.github.io/ajmc_iiif/{commentary_id}/{image_id}
```

To this base URL, you can add

- For basic info about the available images: `/info.json`
- For the full-sized image: `/full/max/0/default.png`
- For the thumbnail image: `/full/250,/0/default.png`

TODO: Add live links for example images.
