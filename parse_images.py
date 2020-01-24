import os
def generate_images(path):
    image_types  = (".jpg", ".png")
    for rootDir, dirNames, filenames in os.walk(path):
        for filename in filenames:
            ext = filename[filename.rfind("."):].lower()
            if ext.endswith(image_types):
                image_path = os.path.join(rootDir, filename)
                yield image_path

