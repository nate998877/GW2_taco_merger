import xml.etree.ElementTree as ET
import os


def listDirs():
    name = [name for name in os.listdir(os.getcwd()) if os.path.isdir(
        os.path.join(os.getcwd(), name))]
    if '.git' in name:
        name.remove('.git')
    if '.vscode' in name:
        name.remove('.vscode')
    return name


def removeXML(dirs):
    length = len(dirs)
    i = 0
    while(i < length):
        if dirs[i].endswith('.xml'):
            del dirs[i]
            i -= 1
        i += 1
    return dirs


def listXML(xml_list):
    for filename in os.listdir(os.getcwd()):
        if not filename.endswith('.xml'):
            continue
        fullname = os.path.join(os.getcwd() + '/' + filename)
        xml_list.append(fullname)
    return xml_list


def recursiveDirSearch():
    dirs = listDirs()
    dirs = removeXML(dirs)
    xml_list = []

    if dirs:
        for entry in dirs:
            os.chdir('./' + entry)
            xml_list.extend(recursiveDirSearch())

    xml_list = listXML(xml_list)

    os.chdir('../')
    return xml_list


def parseXML(xml_list):
    print(len(xml_list))
    for xml in xml_list:
        try:
            tree = ET.parse(xml)
            root = tree.getroot()
            print(root)
        except:
            print(xml)


def main():
    xml_list = recursiveDirSearch()
    parseXML(xml_list)


if __name__ == "__main__":
    main()
