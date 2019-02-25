from psd_tools import PSDImage
import os
from pathlib import Path

""" 
    Export images from a photoshop file
    This file is specific to the email process
    Images are saved out with Desktop_01.jpg, Mobile_01.jpg format
"""

BLUE, END = '\33[94m', '\033[0m'
desktopArtboard, mobileArtboard = None, None
desktopModuleList, mobileModuleList = [], []

""" Directory the psd file is located in """
user_directory = input('PSD path:')

""" psd file name, does not need to include extension """
psd = input('PSD name:')

if psd:
    for file in os.listdir(user_directory):
        if psd in file:
            path_of_psd = Path(user_directory).joinpath(file)
            break

if not psd:
    for file in os.listdir(user_directory):
        if '.psb' in file or '.psd' in file:
            path_of_psd = Path(user_directory).joinpath(file)
            break

if not path_of_psd:
    path_of_psd = Path(user_directory).joinpath(psd)


""" load the psd into memory """
print(f'\nLoading {{}}{psd}{{}}'.format(BLUE, END))
psd_load = PSDImage.open(path_of_psd)
print(f'Finished loading {{}}{psd}{{}}\n'.format(BLUE, END))

""" create an image directory if it does not exist """
os.makedirs(Path(user_directory).joinpath('images'), exist_ok=True)


""" get specific desktop and mobile artboard """
for i in psd_load:
    if 'DESKTOP'.lower() in i.name.lower():
        desktopArtboard = i
    if 'MOBILE'.lower() in i.name.lower():
        mobileArtboard = i


def module_list(artboard, lst):
    """ collate layers names into a list """
    for layer in reversed(list(artboard.descendants())):
        if layer.name == 'HEADER':
            print(f'Excluding layer {layer.name}')
        else:
            lst.append(layer.name)
    return lst


def image_extraction(p, name):
    """ export images """
    counter = 0
    try:
        for layer in reversed(list(p.descendants())):
            if 'image'.lower() in layer.name.lower() and layer.is_visible():
                try:
                    counter += 1
                    image = layer.compose()
                    save_image(image, counter, name)
                except:
                    pass

    except AttributeError:
        pass


def save_image(image, counter, name):
    """ Save image if counter length is less than or equal to 9 """
    if counter <= 9:
        image.convert('RGB').save(Path(user_directory).joinpath('images', f'{name}_0{str(counter)}.jpg'), quality=85)
        print(f'{name}_0{str(counter)}.jpg')

    """ Save image if counter length is greater than 9 """
    if counter > 9:
        image.convert('RGB').save(Path(user_directory).joinpath('images', f'{name}_{str(counter)}.jpg'), quality=85)
        print(f'{name}_{str(counter)}.jpg')


module_list(desktopArtboard, desktopModuleList)
module_list(mobileArtboard, mobileModuleList)
image_extraction(desktopArtboard, name='Desktop')
image_extraction(mobileArtboard, name='Mobile')
