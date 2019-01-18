from psd_tools import PSDImage
import os
from pathlib import Path

""" Export image from a photoshop file """
BLUE, END = '\33[94m', '\033[0m'
user_directory = input('PSD path:')

psd = input('PSD name:')

path_of_psd = os.path.join(user_directory + '\\' + psd)

for file in os.listdir(user_directory):
    if psd in file:
        path_of_psd = user_directory + '\\' + file

print(f'\nLoading {{}}{psd}{{}}'.format(BLUE, END))
psd_load = PSDImage.load(path_of_psd)
print(f'Finished loading {{}}{psd}{{}}\n'.format(BLUE, END))

""" make an images directory if it does not exist """
os.makedirs(f'{user_directory}\\images', exist_ok=True)

desktopArtboard, mobileArtboard = None, None
desktopModuleList, mobileModuleList = [], []


""" gets specific desktop and mobile artboard """
for i in psd_load.layers:
    if 'DESKTOP' in i.name:
        desktopArtboard = i
    if 'MOBILE' in i.name:
        mobileArtboard = i


""" collate layers names into a list """
for i in desktopArtboard.layers:
    if i.name == 'HEADER':
        print(f'Excluding layer {i.name}')
    else:
        desktopModuleList.append(i.name)

for i in mobileArtboard.layers:
    if i.name == 'HEADER':
        print(f'Excluding layer {i.name}')
    else:
        mobileModuleList.append(i.name)


def image_extraction(p, name):
    """ export images """
    t = 0
    for layer in p.layers:
        try:
            for j in layer.layers:
                if 'image'.lower() in j.name.lower():
                    t += 1
                    a = j.as_PIL()
                    a.save(f'{user_directory}\\images\\{name}_0{str(t)}.jpg', quality=80, optimize=True)
        except AttributeError as Argument:
            print(f'{Argument}')


image_extraction(desktopArtboard, name='Desktop')
image_extraction(mobileArtboard, name='Mobile')
