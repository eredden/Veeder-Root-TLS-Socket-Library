# setup.py - Setup for the veeder_root_tls_socket_library package.
# This can be executed to make a wheel package by running "python -m build" in this directory.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="veeder_root_tls_socket_library",
    author="Evan Redden",
    author_email="redden.evan@gmail.com",
    description="Socket library for querying and extracting data from Veeder-Root TLS systems.",
    keywords="veeder-root, socket, networking, internet, protocol, query",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eredden/Veeder-Root-TLS-Socket-Library",
    project_urls={
        "Source Code": "https://github.com/eredden/Veeder-Root-TLS-Socket-Library"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    test_suite="unittest",
    tests_require=["unitest"],
    version = "1.0.0"
)