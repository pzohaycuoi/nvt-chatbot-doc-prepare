import os

from fastapi import UploadFile


def _ensure_temp_dir():
    """
    Ensures that a temporary directory exists.

    Returns:
        str: The absolute path of the temporary directory.
    """
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        temp_path = '../.temp/'
        abs_temp_dir = os.path.join(dir_path, temp_path)
        if not os.path.exists(abs_temp_dir):
            try:
                os.makedirs(abs_temp_dir)
            except Exception as err:
                print(err)
    except Exception as err:
        raise err
    return abs_temp_dir


def write_to_file(file_name, file_bytes: UploadFile):
    """
    Writes the uploaded file to a temporary directory.

    Args:
        file_name (str): The name of the file to be written.
        file_bytes (UploadFile): The uploaded file object.

    Returns:
        str: The path of the written file.
    """
    try:
        temp_path = _ensure_temp_dir()
        file_path = os.path.join(temp_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'wb') as file:
            file.write(file_bytes.file.read())
            file.close()
    except Exception as err:
        raise err
    return file_path


def get_size(file_path, unit='bytes'):
    """
    Gets the size of a file.

    Args:
        file_path (str): The path of the file.
        unit (str, optional): The unit to return the size in. Defaults to 'bytes'.

    Returns:
        float: The size of the file in the specified unit.
    """
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)
