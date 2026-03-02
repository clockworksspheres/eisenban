#!/usr/bin/env -S python -u

import xml.etree.ElementTree as ET

def generate_qrc_file(output_path, resources):
    root = ET.Element("RCC")
    qresource = ET.SubElement(root, "qresource")
    qresource.set("prefix", "/")

    for resource in resources:
        file_element = ET.SubElement(qresource, "file")
        file_element.text = resource

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    return tree

resources = ["icons/icon1.png", "icons/icon2.png"]
generate_qrc_file("resources.qrc", resources)


