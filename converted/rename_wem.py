import os

# Work in the current directory
folder_path = os.getcwd()

for filename in os.listdir(folder_path):
    if filename.endswith(".wem") and "_" in filename:
        base = filename.split("_")[0] + ".wem"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, base)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {base}")
