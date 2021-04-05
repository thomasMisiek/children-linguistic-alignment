import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='children-linguistic-alignment',
    version="0.0.1",
    author='Thomas MISIEK',
    author_email='thomas.misiek@gmail.com',
    description="A small example package",
    url="https://github.com/pypa/sampleproject",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": ""},
    packages=setuptools.find_packages(where=""),
    python_requires=">=3.x",
)
