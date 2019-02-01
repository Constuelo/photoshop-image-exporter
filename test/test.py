from psd_tools2 import PSDImage

psd_load = PSDImage.open('test.psd')

a = psd_load
for i in a[0]:
    print(i)