import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="online-store",
    version="0.0.1",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django :: 4",
        "Operating System :: OS Independent",
    ],
    keywords="online, store, final, project, SDA",
    package_dir={"": "store"},
    packages=find_packages(where="store"),
    python_requires=">=3.9, <4",
    install_requires=[
    ],
    extras_require={
        "dev": [
        ],
        "test": [
        ],
        "prod": [
        ],
    },
    entry_points={
        "console_scripts": [
            "manage=manage:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/gledi/online-store/issues",
        "Source": "https://github.com/gledi/online-store",
    },
)
