#!/usr/bin/env -S python -u

import os
import glob
import xml.etree.ElementTree as ET
import xml.dom.minidom

def generate_qrc_file(output_path, icon_dir):
    # Create the root element
    root = ET.Element("RCC")
    qresource = ET.SubElement(root, "qresource")
    qresource.set("prefix", "/resources")  # You can change the prefix as needed

    ext_dir = "resources"  # Path to the directory containing icons
    ext_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ttf", ".ico", ".icns"]  # List of icon file extensions
    ext_files = []
    for ext in ext_extensions:
        # Use glob to find files with the specified extension
        for file_path in glob.glob(f"{ext_dir}/**/*{ext}", recursive=True):
            ext_files.append(file_path)

    for file in ext_files:
        file_element = ET.SubElement(qresource, "file")
        file_element.text = file 

    # Convert ElementTree to string
    xml_str = ET.tostring(root, encoding="utf-8")

    # Parse the string with minidom to pretty print
    parsed = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = parsed.toprettyxml(indent="  ")

    # Write the pretty-printed XML to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)


def find_ext_files(directory, extensions):
    """
    Search for icon files in the specified directory and its subdirectories.

    :param directory: The root directory to search in.
    :param extensions: A list of file extensions to search for (e.g., ['.png', '.jpg']).
    :return: A list of paths to the found icon files.
    """
    ext_files = []
    for ext in extensions:
        # Use glob to find files with the specified extension
        for file_path in glob.glob(f"{directory}/**/*{ext}", recursive=True):
            ext_files.append(file_path)
    return ext_files


ext_dir = "resources"  # Path to the directory containing icons
ext_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ttf", ".ico", ".icns"]  # List of icon file extensions

ext_files = find_ext_files(ext_dir, ext_extensions)

# Print the found icon files
for file in ext_files:
    print(file)

# Example usage
icon_dir = "icons"  # Path to the directory containing icons
output_path = "resources_rc.qrc"  # Path to the output .qrc file
generate_qrc_file(output_path, icon_dir)
