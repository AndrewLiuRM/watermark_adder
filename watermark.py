from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys

# handles watermark with text only
def watermark_text(input_image_path,
                   output_image_path,
                   text, position):
    # Set the scale and font
    scale = 0.1
    font = ImageFont.load_default()
    w_width, w_height = font.getsize(text)
    # Open image
    photo = Image.open(input_image_path)
    width, height = photo.size

    pos = get_position(position, width, height, w_width, w_height)

    # make the image editable
    drawing = ImageDraw.Draw(photo)

    black = (3, 8, 12)

    drawing.text(pos, text, fill=black, font=font)
    photo.show()
    photo.save(output_image_path)

def get_position(mode, width, height, w_width, w_height):
    # initialize scale
    x_scale = 0.01
    y_scale = 0.01

    # modes
    if mode == 0: # left top
        return (int(width * x_scale), int(height * y_scale))
    elif mode == 1: # right top
        return (int(width * (1 - x_scale) - w_width), int(height * y_scale))
    elif mode == 2: # left bottom
        return (int(width * x_scale), int(height * (1 - y_scale) - w_height))
    elif mode == 3: # right bottom
        return (int(width * (1 - x_scale) - w_width), int(height * (1 - y_scale) - w_height))
    return (0,0)

# handles watermark with images
def watermark_with_transparency(input_image_path,
                                output_image_path,
                                watermark_image_path,
                                pos):
    # set up scale
    scale = 0.2
    # open image and water mark
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size
    # calculate water mark size
    size = int(width * scale), int(height * scale)
    # water mark resize
    watermark.thumbnail(size)
    # get size
    w_width, w_height = watermark.size
    position = get_position(pos, width, height, w_width, w_height)

    # paste and mask
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent = transparent.convert('RGB')
    transparent.show()

    transparent.save(output_image_path)

# print the usage information
def print_usage():
    print "Usage: ./watermark.py [type] [int] [inputfile_path] [outputfile_path] [watermark_path]\n"
    print "type:    -t  text watermark\n"
    print "         -i  image watermark\n\n"
    print "int:     0   left top corner\n"
    print "int:     1   right top corner\n"
    print "int:     2   left bottom corner\n"
    print "int:     3   right bottom corner\n"

if __name__ == '__main__':
    # check arguments
    if len(sys.argv) != 6: # wrong number of arguments
        print_usage()
    elif sys.argv[1] == "-t": # text watermark
        watermark_text(sys.argv[3], sys.argv[4],
                       sys.argv[5],
                       int(sys.argv[2]))
    elif sys.argv[1] == "-i": # image watermark
        watermark_with_transparency(sys.argv[3], sys.argv[4],
                       sys.argv[5],
                       int(sys.argv[2]))
    else:
        print_usage()
