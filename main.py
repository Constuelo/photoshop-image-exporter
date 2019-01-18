from psd_tools import PSDImage
import os
from pathlib import Path

""" Export image from a photoshop file """
psd = 'Campaign1_CR_Layering.psd'
psd_load = PSDImage.load(Path(os.path.dirname(__file__)) / psd)


""" make an images directory if it does not exist """
os.makedirs('images', exist_ok=True)

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
                    a.save(f'images\\{name}_0{str(t)}.jpg', quality=80, optimize=True)
        except AttributeError as Argument:
            print(f'{Argument}')


image_extraction(desktopArtboard, name='Desktop')
image_extraction(mobileArtboard, name='Mobile')
