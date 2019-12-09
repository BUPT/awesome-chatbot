"""
A python tool to resize images(如果你不想阅读下面的英文，使用推荐命令[第一条]就可以了)

Usage:
    python fit_image.py --images (image_dir|one image) --width 1920

    if you wanna resize image by setting resolution
    please use this command :
        - python fit_image.py --images xxxx --width 1920
         (RECOMMEND!! you only set width which height can rescale by width change ratio)
        - python fit_image.py --images xxxx  --height 1080 
        (same as above)
        - python fit_image.py --images xxxx --width 1920 --height 1080
        (not recommend,only if you know how change image)

    if you wanna resize image resolution by setting ratio ,
    please use this command(not recommend):
        - python fit_image.py --images xxx --ratio 0.5

"""

import os
from PIL import Image
import argparse
import re
import sys


def chose_proper_resolution(args, old_width, old_height):
    """
    according the ratio or weight and hegiht to chose a proper resolution

    return the proper resolution

    """

    if args.ratio > 0:
        """
        use ratio to resize (0,1) .
        It's very dangerous action which will modify all image ,
        so you need to make sure you wamma do this
        """
        if args.ratio > 1:
            print("make sure ratio between 0 and 1")
            exit()

        print('-->Please check use ratio {} to resize all images!\
            \n If you sure,please input yes/y to argee'.format(args.ratio))
        input_str = sys.stdin.readline().strip().lower()
        if 'yes' == input_str or 'y' == input_str:
            target_width = int(old_width * args.ratio)
            target_height = int(old_height * args.ratio)
        else:
            print('\n-->You need to think about this operation')
            exit(1)
    else:
        # use width or height to resize
        if old_width > args.width > 0 and old_height > args.height > 0:
            # when width and height both are set
            target_width = args.width
            target_height = args.height
        elif old_width > args.width > 0 and args.height == 0:
            # when only width is set
            target_width = args.width
            target_height = int(args.width / old_width * old_height)
        elif args.width and old_height > args.height > 0:
            # when olny height is set
            target_width = int(args.height / old_height * old_width)
            target_height = args.height
        else:
            # other cases, don't modify images
            target_width = old_width
            target_height = old_height

    return target_width, target_height


def resize_image(image_path, args):
    """
    According ratio or resolution to resize image and relpace source image
    """
    img = Image.open(image_path)
    old_width, old_height = img.size
    target_width, target_height = chose_proper_resolution(
        args, old_width, old_height)
    if old_height <= target_height and old_width <= target_width:
        print(
            '-->The resolution has not changed, so this image is not modified:[{}]'.format(image_path))
        return None
    img = img.resize([target_width, target_height], Image.BILINEAR)
    img.save(image_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=str, default="",
                        help="the location of image folder or image")
    parser.add_argument('--width', type=int, default=0,
                        help="the target image width (recommend 1920)")
    parser.add_argument('--height', type=int, default=0,
                        help="the target image hegiht(recommend 1080)")
    parser.add_argument('--ratio', type=float, default=0,
                        help="the ratio to resize image (recommend 0.7)")
    args = parser.parse_args()
    if os.path.isdir(args.images):
        for root, dirs, files in os.walk(args.images):
            for idx, file in enumerate(files):
                if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif'):
                    print('Resize {} image:[{}]'.format(idx + 1, file))
                    resize_image(os.path.join(root, file), args)
        print('Finish resize images')

    elif os.path.isfile(args.images):
        is_img = args.images.endswith('.jpg') or args.images.endswith(
            '.png') or args.images.endswith('.gif')
        print('Resize one image:', args.images)
        resize_image(args.images, args)
        print('Finish resize image')
    else:
        print("Please check the path of images")
