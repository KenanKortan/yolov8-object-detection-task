import os
import yaml

def count_of_files(config_file_path):
    # Read the configuration from the YAML file
    with open(config_file_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # Use the configuration data as needed
    path_str = config.get('path', '')
    train_str = config.get('train', '')
    val_str = config.get('val', '')
    test_str = config.get('test', '')

    def count(file):
        return len(os.listdir(path_str + '/' + file))

    count_train = count(train_str)
    print(f'Size of train: {count_train}')
    count_val = count(val_str)
    print(f'Size of val: {count_val}')
    count_test = count(test_str)
    print(f'Size of test: {count_test}')

    return count_train + count_val + count_test