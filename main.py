from typing import ItemsView
import xml.etree.ElementTree as ET
import os
import binascii
import struct


def listCurrentDirs(filter=[]):
    dir_list = filter(os.path.isdir, os.listdir(os.path.curdir)) 
    dir_list = list(dir_list)
    for item in filter:
        if item in dir_list: dir_list.remove(item)

    return dir_list


def listFile(file_list, file_type):
    for filename in os.listdir(os.getcwd()):
        if not filename.endswith(file_type):
            continue
        fullname = os.path.join(f"{os.getcwd()}/{filename}")
        file_list.append(fullname)
    return file_list


def recursiveDirSearch():
    """[summary]

    Returns:
        dict: contains lists of paths to trails, png, and xml in S
    """
    dir_filter = ['.git', '.vscode', 'Ideal_Layout']
    dirs = listCurrentDirs(dir_filter)

    xml_list = []
    trl_list = []
    png_list = []

    if dirs:
        for entry in dirs:
            os.chdir('./' + entry)
            d = recursiveDirSearch()

            xml_list.extend(d['xmls'])
            trl_list.extend(d['trls'])
            png_list.extend(d['pngs'])

    xml_list = listFile('.xml')
    trl_list = listFile('.trl')
    png_list = listFile('.png')

    os.chdir('../')
    return {
        'xmls': xml_list,
        'trls': trl_list,
        'pngs': png_list,
    }


def parseXML(xml_list):
    for xml in xml_list:
        try:
            tree = ET.parse(xml)
            root = tree.getroot()
            print(root)
        except:
            print(xml)



def bytes_from_file(filename, chunksize=4096):
    init = 0
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)

            if chunk:
                if init == 0:
                    init = 1
                    yield chunk[4:8] # bytes 0-4 is always 0000, this is map ID

                for b in range(8,len(chunk),12):
                    yield chunk[b:b+12]
            else:
                break


def check_sphere(point1, point2, radius):
    """given 2 points and a radius tells if point2 is within range of point 1

    Args:
        point1 ([type]): [description]
        point2 ([type]): [description]
        radius ([type]): [description]

    Returns:
        [type]: [description]
    """
    x1 = (point2['x']-point1['x']) ** 2 
    y1 = (point2['y']-point1['y']) ** 2 
    z1 = (point2['z']-point1['z']) ** 2 
    ans = x1 + y1 + z1
    if ans <=(radius**2):
        return True
    else:
        return False



def parseTrl(trl_list):
    """Converts a trl file into a list tuples with 3 floats representing a position in the trail

    Args:
        trl_list ([type]): [description]
    """
    trl_arr = []
    first_instance = True
    map_ID = -1
    for byte in bytes_from_file(trl_list[0]):
        if first_instance:
            first_instance = False
            map_ID = int.from_bytes(byte, byteorder='little')
            continue
        trl_arr.append(struct.unpack('3f', byte))
    return (trl_arr, map_ID)



def main():
    url_dict = recursiveDirSearch()
    print(parseTrl(url_dict['trls']))
    print(len(url_dict['trls']))
    parseXML(url_dict['xmls'])


if __name__ == "__main__":
    main()
