from psd_tools2 import PSDImage
import os

""" 
    Export images from a photoshop file
    This file is specific to the email process
    Images are saved out with Desktop_01.jpg, Mobile_01.jpg format
"""

BLUE, END = '\33[94m', '\033[0m'
desktopArtboard, mobileArtboard = None, None
desktopModuleList, mobileModuleList = [], []

""" Directory the psd file is located in """
# user_directory = input('PSD path:')
user_directory = 'C:\\Users\\rory.ferguson\\Repositories\\Github\\photoshop_email_image_exporter\\test'

""" psd file name, does not need to include extension """
# psd = input('PSD name:')
psd = 'test.psd'

path_of_psd = os.path.join(user_directory + '\\' + psd)

""" 
    the user directory is then read for the psd,
    if the extension is missing it will use the file with the same name,
    It will fail if there are two files with the same name.
"""
for file in os.listdir(user_directory):
    if psd in file:
        path_of_psd = user_directory + '\\' + file

""" load the psd into memory """
print(f'\nLoading {{}}{psd}{{}}'.format(BLUE, END))
psd_load = PSDImage.open(path_of_psd)
print(f'Finished loading {{}}{psd}{{}}\n'.format(BLUE, END))

""" create an image directory if it does not exist """
os.makedirs(f'{user_directory}\\images', exist_ok=True)


""" get specific desktop and mobile artboard """
for i in psd_load:
    if 'DESKTOP'.lower() in str(i.name).strip("'").lower():
        desktopArtboard = i
    if 'MOBILE'.lower() in str(i.name).strip("'").lower():
        mobileArtboard = i


def module_list(artboard, lst):
    """ collate layers names into a list """
    for layer in artboard.descendants():
        if layer.name == 'HEADER':
            print(f'Excluding layer {layer.name}')
        else:
            lst.append(layer.name)
    return lst


def image_extraction(p, name):
    """ export images """
    counter = 0
    try:
        for j in p.descendants():
            if 'image'.lower() in str(j.name).strip("'").lower() and j.is_visible():
                counter += 1
                print(j.compose())
                image = j.compose()
                save_image(image, counter, name)
    except AttributeError as Argument:
        pass


def save_image(image, counter, name):
    """ Save image if counter length is less than or equal to 9 """
    if counter <= 9:
        image.save(f'{user_directory}\\images\\{name}_0{str(counter)}.jpg')

    """ Save image if counter length is greater than 9 """
    if counter > 9:
        image.save(f'{user_directory}\\images\\{name}_{str(counter)}.jpg')


module_list(desktopArtboard, desktopModuleList)
module_list(mobileArtboard, mobileModuleList)
image_extraction(desktopArtboard, name='Desktop')
image_extraction(mobileArtboard, name='Mobile')
