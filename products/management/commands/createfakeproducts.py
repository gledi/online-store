import io

from faker import Faker
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.utils.text import slugify

from products.models import Product


class Command(BaseCommand):
    help = "Creates fake products"

    def add_arguments(self, parser):
        parser.add_argument("--count", "-c", type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(options["count"]):
            name = faker.catch_phrase()
            filename = f'{slugify(name)}.png'
            product = Product(
                name=name,
                price=faker.pydecimal(
                    left_digits=4,
                    right_digits=2,
                    positive=True
                ),
                description="\n".join(faker.paragraphs()),
                photo=ImageFile(io.BytesIO(faker.image()), name=filename)
            )
            product.save()
