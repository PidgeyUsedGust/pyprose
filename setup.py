from setuptools import setup, find_packages


setup(
    name="pyprose",
    version="0.0.1",
    description="Python wrapper around the Microsoft PROSE framework.",
    author="Gust Verbruggen",
    author_email="gust.verbruggen@cs.kuleuven.be",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7,<3.8",
    install_requires=["pycparser", "pythonnet"],
)