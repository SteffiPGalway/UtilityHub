import os

def rename_files(directory, prefix):
    for i, file in enumerate(os.listdir(directory)):
        os.rename(os.path.join(directory, file), os.path.join(directory, f"{prefix}_{i}.txt"))
