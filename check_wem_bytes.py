import argparse
import os
import glob

def check_wem_file(file_path):
    """Checks bytes at positions 0x28 and 0x29 in a .wem file."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read(0x2a)  # Read up to 0x29 inclusive
            
            # Check if enough data is available
            if len(data) < 0x2a:
                return False, f"File too short to read 0x28 and 0x29 (size: {len(data)} bytes)"
            
            # Check bytes
            byte_0x28 = data[0x28]
            byte_0x29 = data[0x29]
            
            if byte_0x28 == 0x04 and byte_0x29 == 0x00:
                return True, None
            else:
                return False, f"Invalid bytes: 0x28={byte_0x28:02x}, 0x29={byte_0x29:02x}"
                
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def check_wem_files_in_folder(folder_path, output_txt):
    """Checks all .wem files in the folder and its subfolders, writes invalid ones to txt."""
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder does not exist: {folder_path}")
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(f"Folder does not exist: {folder_path}\n")
        return
    
    # Collect all .wem files recursively
    wem_files = glob.glob(os.path.join(folder_path, "**", "*.wem"), recursive=True)
    if not wem_files:
        print(f"No .wem files found in folder or subfolders: {folder_path}")
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write("No .wem files found in the specified folder or its subfolders.\n")
        return
    
    print(f"Found {len(wem_files)} .wem files in folder and subfolders: {folder_path}")
    
    # List of invalid files
    invalid_files = []
    
    # Check each file
    for file_path in wem_files:
        is_valid, error_msg = check_wem_file(file_path)
        if not is_valid:
            relative_path = os.path.relpath(file_path, folder_path)
            invalid_files.append((relative_path, error_msg))
            print(f"Invalid file: {relative_path} - {error_msg}")
        else:
            print(f"Valid file: {os.path.relpath(file_path, folder_path)}")
    
    # Write results to txt
    with open(output_txt, 'w', encoding='utf-8') as f:
        if not invalid_files:
            f.write("All .wem files have correct bytes at 0x28=04 and 0x29=00.\n")
            print("All files are valid!")
        else:
            f.write(f"Found {len(invalid_files)} invalid .wem files with incorrect bytes at 0x28 or 0x29:\n\n")
            for file_path, error_msg in invalid_files:
                f.write(f"File: {file_path}\n")
                f.write(f"Error: {error_msg}\n\n")
            print(f"Found {len(invalid_files)} invalid files. Results written to {output_txt}")

def main():
    """Parses command-line arguments and runs the check."""
    parser = argparse.ArgumentParser(description="Check .wem files for bytes at 0x28=04 and 0x29=00.")
    parser.add_argument('--folder', default='orig', help="Path to folder containing .wem files (default: orig)")
    parser.add_argument('--output_txt', default="invalid_wem_files.txt", help="Path to output txt file (default: invalid_wem_files.txt)")
    
    args = parser.parse_args()
    
    check_wem_files_in_folder(args.folder, args.output_txt)
    
    # Pause to keep console open
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()