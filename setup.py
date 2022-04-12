from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in impala_v2/__init__.py
from impala_v2 import __version__ as version

setup(
	name="impala_v2",
	version=version,
	description="any",
	author="dhinesh",
	author_email="dhinesh200014@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
