import os
import shutil
from extensions import extensions



def dir_exists(path_to_dir: str):
    return os.path.exists(path_to_dir) and os.path.isdir(path_to_dir)


def is_dir(path_to_dir: str):
    return os.path.isdir(path_to_dir)


def sorter():
    base_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')

    all_files = os.listdir(base_path)
    for file in all_files:
        current_file_path = os.path.join(base_path, file)

        if is_dir(current_file_path):
            continue

        file_extension = file.split(".")[-1]
        if file_extension not in extensions:
            continue

        directory_path = os.path.join(base_path, file_extension)
        if not dir_exists(directory_path):
            os.mkdir(directory_path)

        shutil.move(src=current_file_path,
                    dst=directory_path
                    )


sorter()