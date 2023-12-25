import os
import shutil
import zipfile
import re
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from functools import partial

# Transliterates the Cyrillic alphabet into Latin

UKRAINIAN_SYMBOLS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "je",
    "zh",
    "z",
    "y",
    "i",
    "ji",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "ju",
    "ja",
)

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split(".")
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W", "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


images_files = list()
video_files = list()
doc_files = list()
audio_files = list()
archives = list()
folders = list()
others = list()
known_extensions = set()
unknown_extensions = set()

file_extensions = {
    "images": images_files,
    "video": video_files,
    "documents": doc_files,
    "audio": audio_files,
    "archives": archives,
    "others": others,
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].lower()


def remove_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(str(folder_path)):
                os.rmdir(folder_path)


def main():
    if len(sys.argv) != 3:
        logging.info(
            "Usage: python3 cleaner_hw3_1.py <source_folder> <destination_folder>"
        )
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]

    os.makedirs(os.path.join(destination_folder, "images"), exist_ok=True)
    os.makedirs(os.path.join(destination_folder, "video"), exist_ok=True)
    os.makedirs(os.path.join(destination_folder, "documents"), exist_ok=True)
    os.makedirs(os.path.join(destination_folder, "audio"), exist_ok=True)
    os.makedirs(os.path.join(destination_folder, "archives"), exist_ok=True)
    os.makedirs(os.path.join(destination_folder, "others"), exist_ok=True)

    process_folder(source_folder, destination_folder)
    remove_empty_folders(source_folder)

    logging.info(f"Images: {images_files}\n")
    logging.info(f"Video: {video_files}\n")
    logging.info(f"Documents: {doc_files}\n")
    logging.info(f"Audio: {audio_files}\n")
    logging.info(f"Archives: {archives}\n")
    logging.info(f"Unknown Extensions: {unknown_extensions}\n")
    logging.info(f"Others: {others}\n")
    logging.info(f"Known Extensions: {known_extensions}\n")


def process_folder(folder, destination_folder):
    with ThreadPoolExecutor() as executor:
        executor.map(
            partial(process_subfolder, destination_folder=destination_folder),
            [os.path.join(folder, item) for item in os.listdir(folder)],
        )


def process_subfolder(item_path, destination_folder):
    if os.path.isfile(item_path):
        extension = get_extensions(item_path)

        if extension in ("jpeg", "png", "jpg", "svg"):
            images_files.append(item_path)
            known_extensions.add(extension)
            shutil.move(
                item_path,
                os.path.join(
                    destination_folder, "images", normalize(os.path.basename(item_path))
                ),
            )

        elif extension in ("avi", "mp4", "mov", "mkv"):
            video_files.append(item_path)
            known_extensions.add(extension)
            shutil.move(
                item_path, os.path.join(destination_folder, "video", normalize(os.path.basename(item_path)))
            )

        elif extension in ("doc", "docx", "txt", "pdf", "xlsx", "pptx"):
            doc_files.append(item_path)
            known_extensions.add(extension)
            shutil.move(
                item_path,
                os.path.join(destination_folder, "documents", normalize(os.path.basename(item_path))),
            )

        elif extension in ("mp3", "ogg", "wav", "amr"):
            audio_files.append(item_path)
            known_extensions.add(extension)
            shutil.move(
                item_path, os.path.join(destination_folder, "audio", normalize(os.path.basename(item_path)))
            )

        elif extension in ("zip", "gz", "tar"):
            archives.append(item_path)
            known_extensions.add(extension)
            archive_folder = os.path.join(destination_folder, "archives", normalize(os.path.basename(item_path).rsplit(".", 1)[0])
            )
            if zipfile.is_zipfile(item_path):
                with zipfile.ZipFile(item_path, "r") as zip_ref:
                    zip_ref.extractall(archive_folder)

            else:
                logging.info(f"Skipping {item_path}: Not a valid zip file")
            os.remove(item_path)

        else:
            unknown_extensions.add(extension)
            others.append(item_path)
            shutil.move(
                item_path,
                os.path.join(destination_folder, "others", normalize(os.path.basename(item_path))),
            )

    elif os.path.isdir(item_path):
        process_folder(item_path, destination_folder)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    main()
