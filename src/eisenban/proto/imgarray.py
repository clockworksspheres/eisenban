#!/usr/bin/env -S python -u

import os
import sys
import glob

ext_dir = "resources"  # Path to the directory containing icons
ext_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg"]  # List of icon file extensions
ext_files = []
for ext in ext_extensions:
    # Use glob to find files with the specified extension
    for file_path in glob.glob(f"{ext_dir}/**/*{ext}", recursive=True):
        file_path = "/".join(file_path.split("/")[1:])
        ext_files.append(file_path)
        print(file_path)

print(str(ext_files))

   
ext_dir = "resources"  # Path to the directory containing icons
ext_extensions = [".ttf"]  # List of icon file extensions
ext_files = []
for ext in ext_extensions:
    # Use glob to find files with the specified extension
    for file_path in glob.glob(f"{ext_dir}/**/*{ext}", recursive=True):
        file_path = "/".join(file_path.split("/")[1:])
        ext_files.append(file_path)
        print(file_path)

print(str(ext_files))


ext_dir = "resources"  # Path to the directory containing icons
ext_extensions = [".ico", ".icns"]  # List of icon file extensions
ext_files = []
for ext in ext_extensions:
    # Use glob to find files with the specified extension
    for file_path in glob.glob(f"{ext_dir}/**/*{ext}", recursive=True):
        file_path = "/".join(file_path.split("/")[1:])
        ext_files.append(file_path)
        print(file_path)

print(str(ext_files))

