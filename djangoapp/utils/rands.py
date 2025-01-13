from random import SystemRandom
import string
from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase+string.digits,
        k=k
    ))


def gen_new_slug(text, k=5):
    return slugify(text) + "-" + random_letters(k)


if __name__ == "__main__":
    print(gen_new_slug("Ressonância Magnética"))
