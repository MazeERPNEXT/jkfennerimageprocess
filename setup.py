from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in jkfenner_image_process/__init__.py
from jkfenner_image_process import __version__ as version

setup(
	name="jkfenner_image_process",
	version=version,
	description="AI image process",
	author="muthukumarmazeworks",
	author_email="muthukumar@mazeworkssolutions.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
