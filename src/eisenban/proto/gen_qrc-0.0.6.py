

import xml.etree.ElementTree as ET
import xml.dom.minidom

# Create the root element
root = ET.Element("RCC")

# Create a qresource element with a prefix
qresource = ET.SubElement(root, "qresource", {"prefix": "/resources"})

# Add multiple font resources
fonts = ['font/Andika-Bold.ttf', 'font/TorusPro.ttf', 'font/Andika-Regular.ttf', 'font/NotoSans.ttf', 'font/Arimo-Medium.ttf']
for font_path in fonts:
    font = ET.SubElement(qresource, "file")
    font.text = font_path

# Add multiple image resources
images = ['img/add.png', 'img/icon.png', 'img/left-arrow.png', 'img/down-arrow.png', 'img/settings.png', 'img/settings_2.png', 'img/logout.png', 'img/right-arrow.png', 'img/delete.png', 'img/up-arrow.png', 'img/kanbaru.png', 'img/bg.png']
for image_path in images:
    image = ET.SubElement(qresource, "file")
    image.text = image_path

# Add multiple icon resources
icons = ['icons/Barkerbaggies-Bag-O-Tiles-E.ico', 'icons/E.ico', 'icons/E.icns', 'icons/Barkerbaggies-Bag-O-Tiles-E.icns']
for icon_path in icons:
    icon = ET.SubElement(qresource, "file")
    icon.text = icon_path

# Create an ElementTree object
tree = ET.ElementTree(root)

# Convert the ElementTree to a string and pretty print it
xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
pretty_xml_str = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")

# Write the pretty printed XML to a .qrc file
with open("resources_rc.qrc", "w", encoding="utf-8") as f:
    f.write(pretty_xml_str)


