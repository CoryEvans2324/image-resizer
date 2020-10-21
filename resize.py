import os
import sys
import math
import optparse

from PIL import Image


def calc_other(l, size_x, size_y):
    return math.floor(l * (size_x / size_y))


def resize(f, width, height, save_params={}):

    orientation = {
        2: Image.FLIP_LEFT_RIGHT,
        3: Image.ROTATE_180,
        4: Image.FLIP_TOP_BOTTOM,
        5: Image.TRANSPOSE,
        6: Image.ROTATE_270, # -Image.ROTATE_90
        7: Image.TRANSVERSE,
        8: Image.ROTATE_90 # -Image.ROTATE_270
    }

    file_path, file_name = os.path.split(f)

    old_im = Image.open(f)
    tags = old_im.getexif()


    orientation_tag = tags.get(0x0112, None)
    exif_orientation = orientation.get(orientation_tag, None)
    if exif_orientation:
        old_im = old_im.transpose(exif_orientation)

    if width > 0 and height <= 0:
        height = calc_other(width, old_im.size[0], old_im.size[1])
    elif height > 0 and width <= 0:
        width = calc_other(height, old_im.size[1], old_im.size[0])

    size = (
        math.floor(width),
        math.floor(height)
    )

    new_im = old_im.resize(size)

    name, ext = os.path.splitext(file_name)
    new_file = f'{name}_{new_im.width}x{new_im.height}{ext}'
    new_file = os.path.join(file_path, new_file)

    print(f'saving {new_file}')

    new_im.save(new_file, **save_params)


def main():

    save_params = {
        'quality': 75,
        'optimize': True
    }

    parser = optparse.OptionParser()
    parser.add_option('--width', type=int, dest='width', default=0)
    parser.add_option('--height', type=int, dest='height', default=0)
    # parser.add_option('-f', '--file', metavar='FILE', dest='file')

    opt, args = parser.parse_args()
    opt = vars(opt)

    try:
        width = opt['width']
        height = opt['height']
    except Exception as e:
        print(e)
        print('cannot parse width/height')
        return 1

    if width <= 0 and height <= 0:
        print('At least the new width or height needs to be specified')
        return 1

    # return resize(opt['file'], width, height, save_params)
    for fpath in args:
            if not os.path.isfile(fpath):
                print('no file specified or not found')
                continue
            resize(fpath, width, height, save_params)


if __name__ == "__main__":
    sys.exit(main())
