import sys
from pathlib import Path

import setuptools

# Add src to path so we can import redis_redirect
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from redis_redirect import version  # noqa: E402

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.in") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="redis-redirect",
    version=version.VERSION,
    author="Andrey Sorokin",
    author_email="andrey@sorokin.engineer",
    description="(aio)REDIS wrapper to deal with cluster redirect exceptions (`MOVED`).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andgineer/redis-redirect",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.8",
    keywords="redis asyncio wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
