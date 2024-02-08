import os
import random
import shutil
from dotenv import load_dotenv
from convert_coco_to_yolo_format import convert_coco_to_yolo

# Load environment variables from .env file
load_dotenv()

# Access sensitive information from environment variables
env_path = os.getenv('ENV_PATH')
data_path = os.getenv('DATA_PATH')
ext_path = os.getenv('EXT_PATH')

def count_files_in_folder(folder_path):
    try:
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        return len(files)
    except FileNotFoundError:
        print(f"The folder at path {folder_path} does not exist.")
        return None

def split_images(source_folder, destination_folder, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, num_files=0, remove_existing=False):
    # Remove existing folders if specified
    if remove_existing:
        shutil.rmtree(destination_folder, ignore_errors=True)
    
    # Create destination folders
    train_folder = os.path.join(destination_folder, 'train')
    val_folder = os.path.join(destination_folder, 'val')
    test_folder = os.path.join(destination_folder, 'test')
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    # List all files in the source folder
    files = sorted(os.listdir(source_folder))
    #random.shuffle(files)

    # Calculate split indices
    if num_files == 0:
        num_files = len(files)
    #num_files = len(files)
    train_split = int(train_ratio * num_files)
    val_split = int((train_ratio + val_ratio) * num_files)
    test_split = int(((train_ratio + val_ratio) + test_ratio) * num_files)

    # Copy files to the respective folders
    for i, file in enumerate(files):
        source_path = os.path.join(source_folder, file)
        destination_path = 'Default'
        if i < train_split:
            destination_path = os.path.join(train_folder, file)
        elif i < val_split:
            destination_path = os.path.join(val_folder, file)
        elif i < test_split:
            destination_path = os.path.join(test_folder, file)
        #TODO: else: destination_path = os.path.join(destination_folder, file)
        shutil.copy(source_path, destination_path)

    # Verification step
    for folder in [train_folder, val_folder, test_folder]:
        file_count = count_files_in_folder(folder)
        if file_count is not None and file_count > 0:
            print(f"Files copied successfully to {folder}.")
        else:
            print(f"Error: No files copied to {folder}.")

def split_labels(source_folder, destination_folder, class_mapping, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, num_files=0, remove_existing=False):
    # Remove existing folders if specified
    if remove_existing:
        shutil.rmtree(destination_folder, ignore_errors=True)

    # Create destination folders
    train_folder = os.path.join(destination_folder, 'train')
    val_folder = os.path.join(destination_folder, 'val')
    test_folder = os.path.join(destination_folder, 'test')
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    # List all files in the source folder
    files = sorted(os.listdir(source_folder))
    # random.shuffle(files)

    # Calculate split indices
    if num_files == 0:
        num_files = len(files)
    # num_files = len(files)
    train_split = int(train_ratio * num_files)
    val_split = int((train_ratio + val_ratio) * num_files)
    test_split = int(((train_ratio + val_ratio) + test_ratio) * num_files)

    # Copy files to the respective folders
    for i, file in enumerate(files):
        source_path = os.path.join(source_folder, file)
        destination_path = 'Default'
        file = str(file)[:-4] + '.txt'
        if i < train_split:
            destination_path = os.path.join(train_folder, file)
        elif i < val_split:
            destination_path = os.path.join(val_folder, file)
        elif i < test_split:
            destination_path = os.path.join(test_folder, file)
        # TODO: else: destination_path = os.path.join(destination_folder, file)
        #shutil.copy(source_path, destination_path)

        # XML to TXT conversion
        convert_coco_to_yolo(source_path, destination_path, class_mapping)

    # Verification step
    for folder in [train_folder, val_folder, test_folder]:
        file_count = count_files_in_folder(folder)
        if file_count is not None and file_count > 0:
            print(f"Files copied successfully to {folder}.")
        else:
            print(f"Error: No files copied to {folder}.")

class_mapp = {'Apple':0}

def split_dataset(num_files, remove_existing=False):
    # Example usage
    split_images(source_folder=ext_path + '/images',
                 destination_folder=data_path + '/images',
                 num_files=num_files,
                 remove_existing=remove_existing)
    split_labels(
        source_folder=ext_path + '/annotations_filtered',
        destination_folder=data_path + '/labels',
        class_mapping=class_mapp,
        num_files=num_files,
        remove_existing=remove_existing)

# Execution
split_dataset(50,True)


