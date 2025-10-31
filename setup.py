from setuptools import setup

setup(
    name="lncn",
    version="0.1.0",
    description="simple python cli to count SLOC in a project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="qque",
    url="https://github.com/qque/lncn",

    py_modules=["lncn"],

    entry_points={
        "console_scripts": [
            "lncn = lncn:main",
        ],
    },
)