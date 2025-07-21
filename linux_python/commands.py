# commands.py

import os
import shutil
import logging
#=====================================================

# Configure logger for the commands module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#=====================================================

def mv_last(src_directory, des_directory):
    try:
        logger.info(f"Source Directory: {src_directory}")
        logger.info(f"Destination Directory: {des_directory}")

        if not os.path.exists(src_directory):
            error_message = f"Source directory {src_directory} does not exist."
            logger.error(error_message)
            return error_message

        if not os.path.exists(des_directory):
            logger.info(f"Destination directory {des_directory} does not exist. Creating directory.")
            os.makedirs(des_directory)

        files = [os.path.join(src_directory, f) for f in os.listdir(src_directory)]
        files = [f for f in files if os.path.isfile(f)]

        if not files:
            warning_message = f"No files to move in {src_directory}"
            logger.warning(warning_message)
            return warning_message

        latest_file = max(files, key=os.path.getmtime)
        logger.info(f"Latest File to Move: {latest_file}")

        shutil.move(latest_file, des_directory)
        success_message = f"Moved {latest_file} to {des_directory}"
        logger.info(success_message)
        return None
    except PermissionError as e:
        error_message = f"Permission error: {e}"
        logger.error(error_message)
        return error_message
    except FileNotFoundError as e:
        error_message = f"File not found error: {e}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error moving file: {e}"
        logger.error(error_message)
        return error_message

#=====================================================

def categorize(directory, threshold_size):
    try:
        small_dir = os.path.join(directory, 'small_files')
        large_dir = os.path.join(directory, 'large_files')
        os.makedirs(small_dir, exist_ok=True)
        os.makedirs(large_dir, exist_ok=True)

        threshold_size = parse_size(threshold_size)

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                if os.path.getsize(filepath) < threshold_size:
                    destination = os.path.join(small_dir, filename)
                else:
                    destination = os.path.join(large_dir, filename)

                if os.path.exists(destination):
                    base, extension = os.path.splitext(destination)
                    counter = 1
                    new_destination = f"{base}_{counter}{extension}"
                    while os.path.exists(new_destination):
                        counter += 1
                        new_destination = f"{base}_{counter}{extension}"
                    destination = new_destination

                shutil.move(filepath, destination)
        logger.info(f"Categorized files in {directory} by size {threshold_size} bytes")
        return None
    except Exception as e:
        error_message = f"Error categorizing files: {e}"
        logger.error(error_message)
        return error_message
#=====================================================

def count_files(directory):
    try:
        count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        logger.info(f"Counted {count} files in {directory}")
        return count
    except Exception as e:
        error_message = f"Error counting files: {e}"
        logger.error(error_message)
        return error_message

#=====================================================

def delete_file(filename, directory):
    try:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Deleted {filename} from {directory}")
            return None
        else:
            warning_message = f"File {filename} not found in {directory}"
            logger.warning(warning_message)
            return warning_message
    except Exception as e:
        error_message = f"Error deleting file: {e}"
        logger.error(error_message)
        return error_message
#=====================================================


def rename_file(old_name, new_name, directory):
    try:
        old_filepath = os.path.join(directory, old_name)
        new_filepath = os.path.join(directory, new_name)
        if os.path.exists(old_filepath):
            os.rename(old_filepath, new_filepath)
            logger.info(f"Renamed {old_name} to {new_name} in {directory}")
            return None
        else:
            warning_message = f"File {old_name} not found in {directory}"
            logger.warning(warning_message)
            return warning_message
    except Exception as e:
        error_message = f"Error renaming file: {e}"
        logger.error(error_message)
        return error_message

#=====================================================

def list_files(directory):
    try:
        files = os.listdir(directory)
        logger.info(f"Files in {directory}: {files}")
        return files
    except Exception as e:
        error_message = f"Error listing files: {e}"
        logger.error(error_message)
        return error_message

#=====================================================

def sort_files(directory, criteria):
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f))]
        if criteria == 'name':
            files.sort(key=lambda x: os.path.basename(x))
        elif criteria == 'date':
            files.sort(key=lambda x: os.path.getmtime(x))
        elif criteria == 'size':
            files.sort(key=lambda x: os.path.getsize(x))
        else:
            warning_message = f"Unsupported sorting criteria: {criteria}"
            logger.warning(warning_message)
            return warning_message

        sorted_files = [os.path.basename(f) for f in files]
        logger.info(f"Sorted files in {directory} by {criteria}: {sorted_files}")
        return sorted_files
    except Exception as e:
        error_message = f"Error sorting files: {e}"
        logger.error(error_message)
        return error_message

#=====================================================

def parse_size(size_str):
    size_units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}
    size, unit = float(size_str[:-2]), size_str[-2:].upper()
    return int(size * size_units[unit])
