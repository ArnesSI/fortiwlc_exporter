import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortiwlc_exporter",
    version="0.0.1",
    author="Luka Vadnjal",
    author_email="luka@vadnjal.net",
    description="FortiWLC Prometheus exporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.arnes.si/monitoring/fortiwlc_exporter",
    packages=setuptools.find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
