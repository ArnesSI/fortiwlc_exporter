import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortiwlc_exporter",
    version="1.5.3",
    author="Luka Vadnjal",
    author_email="luka@vadnjal.net",
    description="FortiWLC Prometheus exporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.arnes.si/monitoring/fortiwlc_exporter",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['fortiwlc=fortiwlc_exporter.server:main'],
    },
    install_requires=['prometheus_client', 'requests'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
