from psd_tools import PSDImage
import os
from pathlib import Path

"""
    Export images from a PSD
"""
psd = 'default.psd'
psd_load = PSDImage.load(Path(os.path.dirname(__file__)) / psd)


""" Make an image directory if it does not exist """
os.makedirs('images', exist_ok=True)


counter = []


def recurse(p):
    """
        Loop recursively through the visible photoshop layers \
        For group containing the word 'image' \
        Writes out images inside an 'images' directory \
        For best quality use Pixel Layers or Smart Objects \
        note: Shape layers (vector) do not work correctly. \
    """
    try:
        for layer in p.layers:
            if layer.visible:
                if 'image'.lower() in layer.name.lower():
                    try:
                        counter.append(layer)
                        image = layer.as_PIL()
                        print(layer.layers[0].kind)
                        if len(counter) <= 9:  # 01.jpg
                            image.save(f'images\\0{str(len(counter))}.jpg', quality=80, optimize=True)
                        if len(counter) > 9:  # 10.jpg
                            image.save(f'images\\{str(len(counter))}.jpg', quality=80, optimize=True)

                    except AttributeError:
                        pass

                recurse(layer)

    except AttributeError:
        pass


recurse(psd_load)
