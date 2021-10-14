import requests
from html_epub import settings
from django.utils.crypto import get_random_string
import string
import os
import glob


STATIC = settings.STATICFILES_DIRS[0]
os

def get_image_from_link(url: str) -> str:
    """
    This function downloads an image from a url link. However,
    It must be a url ending in .jpg or .png or any image variant.

    Args:
        url (str): Link to image. Must end in .jpg, .png or image variants.

    Returns:
        str: filename image create
    """

    local_filename = url.split("/")[-1]
    path = f"{STATIC}/{local_filename}"

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def get_unique_string(length: int = 6) -> str:
    """
    This function generates a unique string

    Args:
        length (int, optional): The length of output string. Defaults to 6.

    Returns:
        str: Unique string
    """

    code = get_random_string(
        length, allowed_chars=string.ascii_lowercase + string.digits
    )
    return code


def clean_static_dir():
    """
    This function cleans the django static directory
    """
    files = glob.glob(os.path.join(STATIC, '*'))
    for f in files:
        os.remove(f)
