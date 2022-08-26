import cv2
from PIL import Image

def resize_image_to_pil(image_path, ratio=450):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, _ = image.shape
    r_w = ratio
    r_h = int(h * (r_w / w))
    image = Image.fromarray(image)
    image = image.resize((r_w, r_h))
    return image