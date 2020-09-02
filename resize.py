import os
import sys
import math

from PIL import Image


def resize(f, size_scalar, save_params={}):

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

	exif_orientation = orientation.get(tags[0x0112])
	if exif_orientation:
		old_im = old_im.transpose(exif_orientation)

	size = (
		math.floor(old_im.width * size_scalar),
		math.floor(old_im.height * size_scalar)
	)

	new_im = old_im.resize(size)

	name, ext = os.path.splitext(file_name)
	new_file = f'{name}_{new_im.width}x{new_im.height}{ext}'
	new_file = os.path.join(file_path, new_file)

	print(f'saving {new_file}')

	new_im.save(new_file, **save_params)


def print_usage():
	print(sys.argv[0], '<size_scaler> <file> ...')

if len(sys.argv) < 3:
	print_usage()
	sys.exit(1)

try:
	float(sys.argv[1])
except:
	print_usage()
	sys.exit(1)

save_params = {
	'quality': 75,
	'optimize': True
}

size_scalar = float(sys.argv[1])

for infile in sys.argv[2:]:
	resize(infile, size_scalar, save_params)
