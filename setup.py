from setuptools import find_packages, setup

setup(
    name="rift-framework",
    version="0.7.2",
    description="A magical Python3 -> FunC portal",
    license="MIT",
    packages=find_packages(),
    author="Amin Rezaei",
    author_email="AminRezaei0x443@gmail.com",
    keywords=[],
    entry_points={
        "console_scripts": [
            "rift = rift.cli.entry:entry",
        ],
    },
    url="https://github.com/sky-ring/rift",
    install_requires=[],
    extras_require={},
)
