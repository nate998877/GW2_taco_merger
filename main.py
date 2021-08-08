import xml.etree.ElementTree as ET
import os
import struct


def list_current_dirs(path_filter=[]):
    """list the dirs in the current directory excluding filtered paths

    Args:
        path_filter (list, optional): directories to omit from. Defaults to [].

    Returns:
        dict: dict containing arrays of file paths relative to project root
    """
    all_files = os.listdir(os.path.curdir)
    dir_list = filter(os.path.isdir, all_files)
    dir_list = list(dir_list)
    for item in path_filter:
        if item in dir_list: dir_list.remove(item)

    return dir_list


def list_file(file_type):
    """list files in the current dir with a given extension

    Args:
        file_type (str): the extension in format '.FileType' eg ".txt" || '.png'

    Returns:
        list: relative paths from project root to files in cwd.
    """

    file_list = []
    base_path = os.getcwd()

    for filename in os.listdir(base_path):
        if not filename.endswith(file_type):
            continue

        fullname = os.path.join(f"{base_path}/{filename}")
        file_list.append(fullname)

    return file_list


def recursive_dir_search():
    """Searches project directory for relevant files and adds them to the path.

    Returns:
        dict: contains lists of paths to trails, png, and xml
    """

    dir_filter = ['.git', '.vscode', 'Ideal_Layout'] #This is here just to save processing time. Filtering shouldn't be required as irrelevant files should be ignored.
    dirs = list_current_dirs(dir_filter)

    xml_list = []
    trl_list = []
    png_list = []

    if dirs:
        for entry in dirs:
            os.chdir('./' + entry)
            d = recursive_dir_search()

            xml_list.extend(d['xmls'])
            trl_list.extend(d['trls'])
            png_list.extend(d['pngs'])

    xml_list.extend(list_file('.xml'))
    trl_list.extend(list_file('.trl'))
    png_list.extend(list_file('.png'))

    os.chdir('../')
    return {
        'xmls': xml_list,
        'trls': trl_list,
        'pngs': png_list,
    }


def parse_trail_file(filename, chunksize=4096):
    """converts a binary trail file into a human redable array of XYZ values

    Args:
        filename (str): Path to file to parse
        chunksize (int, optional): Size of binary chunks to be read. Defaults to 4096.

    Returns:
        dict: trail data in human readable form
    """

    init = True
    trl_data = {
        'map_id': -1,
        'trail': [],
    }

    with open(filename, "rb") as f:
        for chunk in iter((lambda:f.read(chunksize)), b''):
            if init:
                init = False
                raw_map_id = chunk[4:8] # bytes 0-4 is always 0000 skip to 4-8 which is the map ID. All of the subsequent data is trail data
                trl_data['map_id'] = int.from_bytes(raw_map_id, byteorder='little')

            for cord_bytes in range(8,len(chunk),12):
                raw_trail = chunk[cord_bytes:cord_bytes+12]
                parsed_trail = struct.unpack('3f', raw_trail)
                trl_data['trail'].append(parsed_trail)

    return trl_data


#TODO: impliment this in a way that it works
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
    return False


#TODO: finish this method.
def parse_XML(xml_list):
    """ list the root element of all xml files a list of xml. This needs expanded and improved and is in this state for sanity checking xml """
    for xml in xml_list:
        try:
            tree = ET.parse(xml)
            root = tree.getroot()
        except:
            print(xml) #XML is invalid. just print path to broken file


def super_printer(url_dict, **kwargs):
    if kwargs.get('default', False):
        print(len(url_dict['xmls']))
        print(len(url_dict['trls']))
        print(len(url_dict['pngs']))


def main():
    url_dict = recursive_dir_search()
    foo = parse_trail_file(url_dict['trls'][0])
    # parse_XML(url_dict['xmls'])

    super_printer(url_dict=url_dict, default=True)


if __name__ == "__main__":
    main()
