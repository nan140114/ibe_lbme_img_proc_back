
from PIL import Image
from pathlib import Path
import tempfile

# create the file in tmp folder
def create_temp_file(file_content):
    tmp_file_name = tempfile.NamedTemporaryFile().name
    with open(tmp_file_name, "wb+") as file_object:
        file_object.write(file_content)
    return tmp_file_name

def get_image_attr(file_location):
    image = Image.open(file_location)
    width, height = image.size
    file_size = Path(file_location).stat().st_size
    return {
        "size"      : file_size,
        "size_unit" : "bytes",
        "width"     : width,
        "height"    : height 
    }