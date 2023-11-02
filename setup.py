from setuptools import setup, find_packages


def setup_package():
    VERSION = '0.0.1'

    # Setting up
    setup(
        name="alphatube",
        version=VERSION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=["youtube_transcript_api", "transformers", "sentencepiece",
                          "deepmultilingualpunctuation", "pysbd"]
    )


if __name__ == "__main__":
    setup_package()
