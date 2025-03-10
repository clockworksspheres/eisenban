

import xml.etree.ElementTree as ET
import xml.dom.minidom

# Create the root element
root = ET.Element("RCC")

# Create a qresource element with a prefix
qresource = ET.SubElement(root, "qresource", {"prefix": "/resources"})

# Add multiple font resources
fonts = ['resources/font/Andika-Bold.ttf', 'resources/font/TorusPro.ttf', 'resources/font/Andika-Regular.ttf', 'resources/font/NotoSans.ttf', 'resources/font/Arimo-Medium.ttf']
for font_path in fonts:
    font = ET.SubElement(qresource, "file")
    font.text = font_path

# Add multiple image resources
images = ['resources/img/add.png', 'resources/img/icon.png', 'resources/img/left-arrow.png', 'resources/img/down-arrow.png', 'resources/img/settings.png', 'resources/img/settings_2.png', 'resources/img/logout.png', 'resources/img/right-arrow.png', 'resources/img/delete.png', 'resources/img/up-arrow.png', 'resources/img/kanbaru.png', 'resources/img/bg.png']
for image_path in images:
    image = ET.SubElement(qresource, "file")
    image.text = image_path

# Add multiple icon resources
icons = ['resources/icons/Barkerbaggies-Bag-O-Tiles-E.ico', 'resources/icons/E.ico', 'resources/icons/E.icns', 'resources/icons/Barkerbaggies-Bag-O-Tiles-E.icns']
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


