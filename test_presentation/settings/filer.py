
INSTALLED_APPS += (  # NOQA
        'filer',
        'easy_thumbnails',
    )

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True