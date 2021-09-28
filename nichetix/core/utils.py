import qrcode
import qrcode.image.svg
from io import BytesIO

from django.conf import settings

DOMAIN = settings.ALLOWED_HOSTS[0]


def generate_qr(slug):
    """
    Generate a qr code from slug

    Compare: https://medium.com/geekculture/how-to-generate-a-qr-code-in-django-e32179d7fdf2
    """
    factory = qrcode.image.svg.SvgPathImage
    url = DOMAIN + "/tickets/" + slug
    img = qrcode.make(url, image_factory=factory, box_size=15)
    stream = BytesIO()
    img.save(stream)
    return stream.getvalue().decode()
