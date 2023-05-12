import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="online-store",
    version="0.1.5a2",
    description="An example of an online store - SDA Tirana, Albania",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gledi/online-store",
    author="Gledi Caushaj",
    author_email="gledi.alb@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: Free For Educational Use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django :: 4",
        "Operating System :: OS Independent",
    ],
    keywords="online, store, final, project, SDA",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11, <4",
    install_requires=[
        "django",
        "environs",
        "dj-database-url",
        "djangorestframework",
        "django-crispy-forms",
        "crispy-bootstrap5",
        "pillow",
        "django-imagekit",
        "django-taggit",
        "django-ckeditor",
        "django-filter",
        "whitenoise[brotli]",
        "psycopg[c,pool]",
        "django-redis",
        "redis",
        "hiredis",
        "channels[daphne]",
        "channels-redis",
        "stripe",
    ],
    extras_require={
        "dev": [
            "django-debug-toolbar",
            "django-extensions",
            "ipython",
            "ruff",
            "mypy",
            "graphviz",
            "pytest",
            "pytest-django",
            "coverage",
            "model-bakery",
            "faker",
        ],
        "prod": [
            "daphne",
            "twisted[tls,http2]",
        ],
    },
    entry_points={
        "console_scripts": [
            "ostore=store.manage:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/gledi/online-store/issues",
        "Source": "https://github.com/gledi/online-store",
    },
)
