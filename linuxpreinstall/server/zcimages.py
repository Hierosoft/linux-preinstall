#!/usr/bin/env python3
'''
zcimages
--------
Convert images in projects/images/ to 3 sizes usable by ZenCart and
place them in images/.

This script is part of <https://github.com/Hierosoft/linux-preinstall>.

Run this script in an offline Zen Cart directory (or online one where
the projects directory is hidden from the public) containing both the
source projects/images and the destination images/ to convert images in
projects/images (non-recursively, ignoring filenames starting with ".")
into 3 sizes of images usable by Zen Cart. In other words, this module
accomplishes a similar task as Image Handler's upload feature when the
feature isn't working: The following 3 images will be generated:
- images/$name.jpg
- images/medium/$name_MED.jpg
- images/large/$name_LRG.jpg
'''
import sys
import os
# import Image
from PIL import Image
# Image requires Pillow such as via: python3 -m pip install --user Pillow

if __name__ == "__main__":
    SUBMODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    MODULE_DIR = os.path.dirname(SUBMODULE_DIR)
    sys.path.insert(0, os.path.dirname(MODULE_DIR))

from linuxpreinstall import (
    echo0,
)
from linuxpreinstall.logging2 import getLogger

from linuxpreinstall.find_pycodetool import pycodetool  # edits sys.path

from pycodetool.parsing import (  # noqa: E401
    find_slice,
)

logger = getLogger(__name__)

src_dirs = []
src_dirs.append(os.path.join("projects", "images"))
src_dirs.append(os.path.join(src_dirs[0], "medium"))
src_dirs.append(os.path.join(src_dirs[0], "large"))

dst_dirs = []
dst_dirs.append("images")
dst_dirs.append(os.path.join(dst_dirs[0], "medium"))
dst_dirs.append(os.path.join(dst_dirs[0], "large"))

sizes = [(120, 120), (400, 400), (1200, 1200)]
# ^ Images on shop.tcsdcc.com predating this script are generally:
# [300, 1600, 3843] or so. However, the width was used instead of the
# max dimension, so the actual numbers used appear to be 120, 400, 1200
# (narrow images are that wide).
suffixes = ["", "_MED", "_LRG"]
size_names = ['regular', 'medium', 'large']
bad_ends = ["Final Product Image", "Final Production Image",
            "Final Image", "Product Image", "Production Image", "Render"]
replacements = [
    ("Final_Face", "face"),
]
SIZE_IDX_REGULAR = 0
SIZE_IDX_MEDIUM = 1
SIZE_IDX_LARGE = 2


def has_transparency(img):
    # From <https://stackoverflow.com/a/58567453/4541104>
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True


def zc_make_sized_images(src_path, dst_zen_cart, force=False,
                         im_format="JPEG", force_jpg_for_large=False):
    '''
    Make 3 images in the dst_zen_cart's images directory.

    Sequential arguments:
    src_path -- the image file to resize and convert to jpg.
    dst_zen_cart -- the Zen Cart directory containing the "images"
        directory.

    Keyword arguments:
    force -- Overwrite existing destination image(s).
    '''
    if not os.path.isdir(os.path.join(dst_zen_cart, "images")):
        raise ValueError('"images" doesn\'t exist in the destination {}'
                         ''.format(dst_zen_cart))
    echo0('* input: "{}"'.format(src_path))
    for size_idx in range(len(dst_dirs)):
        dst_dir = os.path.join(dst_zen_cart, dst_dirs[size_idx])
        name = os.path.split(src_path)[1]
        nameNoExt, dotExt = os.path.splitext(name)
        dst_name = nameNoExt
        good_end = "." + im_format.lower()
        complete_end = suffixes[size_idx] + good_end
        old_name = nameNoExt + complete_end
        parStartI, parEndI = find_slice(dst_name, "(", ")")
        if parStartI > -1:
            dst_name = dst_name[:parStartI] + dst_name[parEndI:]
            # ^ There is no need for parEndI+1, because the slice ender
            #   is the same as the character after the paren.
        for bad_end in bad_ends:
            if dst_name.lower().endswith(bad_end.lower()):
                bad_name = dst_name[:len(bad_end)].strip()
                dst_name = dst_name[:-len(bad_end)].strip()
                bad_name = bad_name.replace(" ", "_")
                bad_name += complete_end
                bad_path = os.path.join(dst_dir, bad_name)
                if os.path.isfile(bad_path):
                    sys.stderr.write('removing "{}"...'.format(bad_path))
                    os.remove(bad_path)
        while "  " in dst_name:
            dst_name = dst_name.replace("  ", " ")
        dst_name = dst_name.strip()
        dst_name = dst_name.replace(" ", "_")
        old_name = old_name.replace(" ", "_")
        dst_name += complete_end
        dst_path = os.path.join(dst_dir, dst_name)
        old_path = os.path.join(dst_dir, old_name)
        sys.stderr.write('  * {}: {}...'
                         ''.format(size_names[size_idx], dst_path))
        for replacement in replacements:
            old, new = replacement
            long_name = dst_name
            long_path = dst_path
            dst_name = dst_name.replace(old, new)
            while "__" in dst_name:
                dst_name = dst_name.replace("__", "_")
            if dst_name != long_name:
                dst_path = os.path.join(dst_dir, dst_name)
                if os.path.isfile(long_path):
                    sys.stderr.write('removing "{}"...'.format(long_name))
                    os.remove(long_path)
        # sys.stderr.write('before _ end check, name is "{}"'.format(dst_name))
        bad_end = "_" + good_end
        while dst_name.endswith(bad_end):
            if os.path.isfile(dst_path):
                sys.stderr.write('removing "{}"...'.format(dst_path))
                os.remove(dst_path)
            dst_name = dst_name[:-len(bad_end)] + good_end
            dst_path = os.path.join(dst_dir, dst_name)

        '''
        if dst_name == "LT-50" + complete_end:
            if os.path.isfile(dst_path):
                sys.stderr.write('removing "{}"...'.format(dst_path))
                os.remove(dst_path)
            sys.stderr.write('appended _face to "{}"...'.format(dst_name))
            dst_name = "LT-50_face" + complete_end
            dst_path = os.path.join(dst_dir, dst_name)
        '''

        size = sizes[size_idx]
        if os.path.isfile(old_path):
            sys.stderr.write('removing "{}"...'.format(old_name))
            os.remove(old_path)
        else:
            pass
            # sys.stderr.write('no "{}"...'.format(old_name))
        # See <https://stackoverflow.com/a/273962/4541104>
        ok_msg = "created"

        try:
            im = Image.open(src_path)
            im.thumbnail(size, Image.ANTIALIAS)
            if (size_idx == SIZE_IDX_LARGE) and force_jpg_for_large:
                oldEnd = ".png"
                # if has_transparency(im)
                if dst_path.endswith(oldEnd):
                    # Reduce the file size of large images dramatically
                    #   by changing from png to jpg.
                    # See <https://stackoverflow.com/a/9459208/4541104>
                    rgbIm = Image.new("RGB", im.size, (255, 255, 255))
                    if has_transparency(im):
                        rgbIm.paste(im, mask=im.split()[3])
                        # ^ 3: alpha channel
                    else:
                        rgbIm.paste(im)
                    im.close()
                    im = rgbIm
                    if os.path.isfile(dst_path):
                        sys.stderr.write('removing "{}"...'.format(dst_path))
                        os.remove(dst_path)
                    dst_path = dst_path[:-len(oldEnd)] + ".jpg"
                    im_format = "JPEG"
            if os.path.isfile(dst_path):
                ok_msg = "already exists (skipped)"
                if force:
                    ok_msg = "already exists (overwritten)"
                    os.remove(dst_path)
            if os.path.isfile(dst_path):
                echo0(ok_msg)
                continue

            im.save(dst_path, im_format)
            echo0(ok_msg)
            im.close()
        except IOError as ex:
            logger.error("Cannot create thumbnail for '%s'" % src_path)
            logger.exception("")  # arg is custom msg


def main():
    sys.stdout.write('Looking for "{}"...'.format(src_dirs[0]))
    if not os.path.isdir(src_dirs[0]):
        logger.error(
            'You must run this script from an offline Zen Cart'
            ' directory containing the source images directory.')
        return 1
    else:
        echo0("OK")
    sys.stderr.write('Looking for "{}"...'.format(src_dirs[0]))
    if not os.path.isdir(src_dirs[0]):
        logger.error(
            'You must run this script from an offline Zen Cart'
            ' directory containing the destination images directory.')
        return 1
    else:
        echo0("OK")
    force = False
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg == "--verbose":
            logging.basicConfig(level=logging.INFO)
        elif arg == "--debug":
            logging.basicConfig(level=logging.DEBUG)
        elif arg == "--force":
            force = True
        else:
            logger.error('Unknown argument: "{}"'.format(arg))
            return 1
    for sub in os.listdir(src_dirs[0]):
        subPath = os.path.join(src_dirs[0], sub)
        if sub.startswith("."):
            continue
        if os.path.isdir(subPath):
            continue
        zc_make_sized_images(subPath, ".", force=force,
                             im_format="PNG")
    return 0


if __name__ == "__main__":
    sys.exit(main())
