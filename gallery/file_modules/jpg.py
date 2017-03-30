import os
import piexif
from wand.image import Image
from wand.color import Color

from gallery.file_modules import FileModule
from gallery.util import hash_file

class JPEGFile(FileModule):

    def __init__(self, file_path):
        print("JPEG CONSTRUCTOR")
        FileModule.__init__(self, file_path)
        self.file_type = "Photo"

        self.load_exif()
        self.generate_thumbnail()


    def load_exif(self):
        print("LOAD EXIF")
        self.exif_dict = piexif.load(self.file_path)


    def generate_thumbnail(self):
        print("GEN THUMB")
        self.thumbnail_uuid = hash_file(self.file_path)

        with Image(filename=self.file_path) as img:
            with img.clone() as image:
                size = image.width if image.width < image.height else image.height
                image.crop(width=size, height=size, gravity='center')
                image.resize(256, 256)
                image.background_color = Color("#EEEEEE")
                image.format = 'jpeg'
                image.save(filename=os.path.join("/gallery-data/thumbnails",
                    self.thumbnail_uuid))
