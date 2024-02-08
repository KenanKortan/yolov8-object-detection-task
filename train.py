# pwd
# nvidia-smi
import os
from ultralytics import YOLO
from PIL import Image
from dotenv import load_dotenv
from utils.count_of_files import count_of_files
import yaml
import torch
torch.cuda.empty_cache()

# Load environment variables from .env file
load_dotenv()

# Access sensitive information from environment variables
env_path = os.getenv('ENV_PATH')
data_path = os.getenv('DATA_PATH')

# Check if the config file already exists
config_file_path = 'config.yaml'
if not os.path.exists(config_file_path):
    # Create YAML configuration dictionary
    config_data = {
        'path': data_path,
        'train': 'images/train',  # train images (relative to 'path')
        'val': 'images/val',  # val images (relative to 'path')
        'test': 'images/test',  # val images (relative to 'path')
        'names': {
            0: 'apple'
        }
    }

    # Write the configuration dictionary to a YAML file
    with open(config_file_path, 'w') as yaml_file:
        yaml.dump(config_data, yaml_file, default_flow_style=False)

# !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Train Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load a model
model = YOLO("yolov8n.pt")# load a pre trained model

data_count = count_of_files(config_file_path)
print(f'Size of dataset: {data_count}')
epochs = 100
batch = 16
imgsz = 1000

results = model.train(data= os.path.join(env_path, "config.yaml"), epochs=epochs, batch=batch , imgsz=imgsz, name=f'data_{data_count}_epoch_{epochs}_imgsiz_{imgsz}') # train the model
# EPOCHS = 100
#: !yolo task=detect mode=train model=yolov8n.pt imgsz=1280 data={ROOT_DIR + '/google_colab_config.yaml'} epochs={EPOCHS} batch=16 name=yolov8n_v8_50e

def run_yolo(yolo, image_url, conf=0.25, iou=0.7):
    results = yolo(image_url, conf=conf, iou=iou)
    res = results[0].plot()[:, :, [2,1,0]]
    return Image.fromarray(res)

# yolo = YOLO('runs/detect/train3/weights/best.pt')

#image_url = personal_path + '/data/apple_images/000092.png'
#predicted_img = run_yolo(yolo, image_url)
#predicted_img