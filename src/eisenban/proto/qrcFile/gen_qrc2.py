#!/usr/bin/env -S python -u

import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

def generate_qrc_file(output_path, icon_dir):
    # Create the root element
    root = ET.Element("RCC")
    qresource = ET.SubElement(root, "qresource")
    qresource.set("prefix", "resources")  # You can change the prefix as needed

    # Scan the directory for icon files
    for root_dir, dirs, files in os.walk(icon_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                file_path = os.path.relpath(os.path.join(root_dir, file), icon_dir)
                file_element = ET.SubElement(qresource, "file")
                file_element.text = root_dir + "/" + file_path

    # Convert ElementTree to string
    xml_str = ET.tostring(root, encoding="utf-8")

    # Parse the string with minidom to pretty print
    parsed = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = parsed.toprettyxml(indent="  ")

    # Write the pretty-printed XML to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)

# Example usage
icon_dir = "resources/img"  # Path to the directory containing icons
output_path = "resources.qrc"  # Path to the output .qrc file
generate_qrc_file(output_path, icon_dir)

