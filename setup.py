from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


def get_long_description():
    with open("README.rst", encoding="utf-8") as f:
        return f.read()


setup(
    name="strictly_typed_pandas",
    url="https://github.com/nanne-aben/strictly_typed_pandas",
    license="MIT",
    author="Nanne Aben",
    author_email="nanne.aben@gmail.com",
    description="Static type checking of pandas DataFrames",
    keywords="typing type checking pandas mypy linting",
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    packages=find_packages(include=["strictly_typed_pandas", "strictly_typed_pandas.*"]),
    install_requires=get_requirements(),
    python_requires=">=3.8.0",
    classifiers=["Typing :: Typed"],
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
    package_data={"strictly_typed_pandas": ["py.typed"]},
)
