#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clipfree",
    version="1.0.0",
    author="ClipFree Contributors",
    author_email="",
    description="100% Free & Open Source Long-Form to Viral Shorts Pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnwangui374-bot/ClipFree",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.10",
    install_requires=[
        "yt-dlp>=2024.1.1",
        "openai-whisper>=20240314",
        "google-genai>=0.3.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "clipfree=clipfree:main",
        ],
    },
)
