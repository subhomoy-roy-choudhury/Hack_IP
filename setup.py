import setuptools
import pathlib

DESCRIPTION = "This is a tool to get ip and system of a specific device"
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="Hack_IP",
    version="2.0.0",
    description= DESCRIPTION,
    long_description = README,
    long_description_content_type="text/markdown",
    author="Subhomoy Roy Choudhury",
    author_email = "subhomoyrchoudhury@gmail.com",
    url="https://github.com/subhomoy-roy-choudhury/Hack_IP",
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
    packages=['hackip','hackip.utils','hackip.helpers'],
    # package_dir = {"": "hackip"},
    include_package_data=True,
    install_requires=['colorama','pyfiglet','termcolor','psutil','requests','maxminddb-geolite2'],
    entry_points={
        "console_scripts": [
            "hackip=hackip:run",
        ]
    },
)