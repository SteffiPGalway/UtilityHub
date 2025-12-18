import os

def rename_files(directory, prefix):
    for i, file in enumerate(os.listdir(directory)):
        # Split filename and extension
        name, ext = os.path.splitext(file)
        # Rename while keeping original extension
        new_name = f"{prefix}_{i}{ext}"
        os.rename(os.path.join(directory, file), os.path.join(directory, new_name))