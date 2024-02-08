import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access sensitive information from environment variables
env_path = os.getenv('ENV_PATH')
data_path = os.getenv('DATA_PATH')
ext_path = os.getenv('EXTRINSIC_PATH')

def convert_coco_to_yolo(xml_file, yolo_file, class_mapping):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    image_width = float(root.find('size/width').text)
    image_height = float(root.find('size/height').text)

    with open(yolo_file, 'w') as yolo_file:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_index = class_mapping[class_name]

            xmin = float(obj.find('bndbox/xmin').text)
            ymin = float(obj.find('bndbox/ymin').text)
            xmax = float(obj.find('bndbox/xmax').text)
            ymax = float(obj.find('bndbox/ymax').text)

            if xmax < xmin:
                xmin, xmax = xmax, xmin
            if ymax < ymin:
                ymin, ymax = ymax, ymin

            x_center = (xmin + xmax) / (2 * image_width)
            y_center = (ymin + ymax) / (2 * image_height)
            width_yolo = (xmax - xmin) / image_width
            height_yolo = (ymax - ymin) / image_height

            yolo_line = f"{class_index} {x_center} {y_center} {width_yolo} {height_yolo}\n"
            yolo_file.write(yolo_line)

def convert_coco_files_to_yolo(coco_files_direct, yolo_files_direct, class_mapping, num_files=None):
    coco_files = sorted(os.listdir(coco_files_direct))  # Sort files
    if num_files is not None:
        coco_files = coco_files[:num_files] 
        #coco_files = coco_files[(num_files+1):]

    for coco_formatted_file in coco_files:
        yolo_formatted_file = str(coco_formatted_file)[:-4] + '.txt'
        yolo_formatted_file = os.path.join(yolo_files_direct, yolo_formatted_file)
        coco_formatted_file = os.path.join(coco_files_direct, coco_formatted_file)
        convert_coco_to_yolo(coco_formatted_file, yolo_formatted_file, class_mapping)

