#!/usr/bin/env python3
"""
Setup script for ARXML Editor
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="arxml-editor",
    version="1.0.0",
    author="hedeya",
    author_email="hedeya@example.com",  # Replace with actual email
    description="A professional AUTOSAR XML (ARXML) editor with dynamic schema detection and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hedeya/arxml-editor",
    project_urls={
        "Bug Reports": "https://github.com/hedeya/arxml-editor/issues",
        "Source": "https://github.com/hedeya/arxml-editor",
        "Documentation": "https://github.com/hedeya/arxml-editor#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Tools",
        "Topic :: Text Processing :: Markup :: XML",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "build": [
            "pyinstaller>=5.0",
            "setuptools>=65.0",
            "wheel>=0.37.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "arxml-editor=main:main",
        ],
        "gui_scripts": [
            "arxml-editor-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["schemas/*.xsd", "*.arxml"],
    },
    keywords="autosar, arxml, xml, editor, automotive, ecu, validation, schema",
    zip_safe=False,
)