import os
import shutil
from extensions import extensions
import re



def dir_exists(path_to_dir: str):
    return os.path.exists(path_to_dir) and is_dir(path_to_dir)


def is_dir(path_to_dir: str):
    return os.path.isdir(path_to_dir)


def file_exists(directory_path: str, file_path: str):
    return os.path.exists(os.path.join(directory_path, os.path.basename(file_path)))


def create_new_file_copy_name(directory_path: str, filename: str):
    strip_copied_filenames = lambda x: x.split(" - ")[0].rstrip()

    copy_count_pattern = re.compile(r'\((?P<number>\d+)\)')
    filename, extension, *_ = filename.split(".")

    stripped_filename = strip_copied_filenames(filename)

    highest_copy = []
    for file in os.listdir(directory_path):
        if strip_copied_filenames(file) == stripped_filename:
            match = re.search(copy_count_pattern, file)
            if match:
                highest_copy.append(int(match.group('number')))

            else:
                """
                In else case, means that we didn't find a match for (filename - Copy (times)), so we append 1
                The outcome of this will be (filename - Copy(2)) , because we always add +1 just before the return
                """
                highest_copy.append(1)

    """
    If the filename has a second copy, then we rename it to (filename - Copy)
    In any other case we rename the file to (filename - Copy(how_many_copies + 1)
    """
    copy_text = "Copy" if not highest_copy else f"Copy ({max(highest_copy) + 1})"

    return os.path.join(directory_path, f"{stripped_filename} - {copy_text}.{extension}")


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

        if file_exists(directory_path, current_file_path):
            directory_path = create_new_file_copy_name(directory_path, file)


        shutil.move(src=current_file_path,
                    dst=directory_path
                    )


sorter()