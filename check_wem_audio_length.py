import os
import struct

def find_data_section(file_path):
    """Finds the 'data' section in a .wem file and returns its offset and size."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Check RIFF header
        if len(data) < 12 or data[:4] != b'RIFF':
            print(f"Error: {file_path} is not a valid RIFF file")
            return None, None
        
        # Search for 'data' chunk
        offset = 12  # Skip RIFF header
        while offset < len(data) - 7:
            chunk_id = data[offset:offset+4]
            chunk_size = struct.unpack('<I', data[offset+4:offset+8])[0]
            if chunk_id == b'data':
                return offset + 8, chunk_size
            offset += 8 + chunk_size
            # Align to even boundary
            if chunk_size % 2:
                offset += 1
        
        print(f"Error: 'data' section not found in {file_path}")
        return None, None
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None, None

def get_audio_data_length(file_path):
    """Gets the length of audio data in a .wem file (up to padding)."""
    data_offset, data_size = find_data_section(file_path)
    if data_offset is None:
        return None
    
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            total_size = f.tell()
            f.seek(data_offset)
            data = f.read(total_size - data_offset)
        
        # Find end of audio data (before padding)
        audio_end = len(data)
        for i in range(len(data) - 1, -1, -1):
            if data[i] != 0:
                audio_end = i + 1
                break
        
        return audio_end
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def check_wem_files(orig_dir, converted_dir, output_txt):
    """Checks audio data lengths and lists oversized converted .wem files."""
    oversized_files = []
    
    # Check if directories exist
    if not os.path.isdir(orig_dir):
        print(f"Error: Original directory not found: {orig_dir}")
        return
    if not os.path.isdir(converted_dir):
        print(f"Error: Converted directory not found: {converted_dir}")
        return
    
    print(f"Scanning directories...")
    print(f"Original directory: {orig_dir}")
    print(f"Converted directory: {converted_dir}")
    
    # Process each .wem file in orig
    for filename in os.listdir(orig_dir):
        if not filename.lower().endswith('.wem'):
            continue
        
        orig_path = os.path.join(orig_dir, filename)
        converted_path = os.path.join(converted_dir, filename)
        
        # Check if converted file exists
        if not os.path.exists(converted_path):
            print(f"Warning: Converted file not found for {filename}")
            continue
        
        # Get audio data lengths
        orig_audio_len = get_audio_data_length(orig_path)
        converted_audio_len = get_audio_data_length(converted_path)
        
        if orig_audio_len is None or converted_audio_len is None:
            print(f"Skipping {filename} due to errors")
            continue
        
        print(f"Checking {filename}:")
        print(f"  Original audio length: {orig_audio_len} bytes")
        print(f"  Converted audio length: {converted_audio_len} bytes")
        
        # Check if converted is longer
        if converted_audio_len > orig_audio_len:
            print(f"  Warning: Converted file is longer than original")
            oversized_files.append(converted_path)
        else:
            print(f"  OK: Converted file is not longer")
        
        print()
    
    # Always write to txt file
    try:
        with open(output_txt, 'w', encoding='utf-8') as f:
            if oversized_files:
                f.write("Oversized converted .wem files (audio data longer than original):\n")
                for file in oversized_files:
                    f.write(f"{file}\n")
                print(f"Found {len(oversized_files)} oversized files. List saved to {output_txt}")
            else:
                f.write("No oversized converted .wem files found (all are shorter or equal to original).\n")
                print(f"No oversized converted files found. Empty list saved to {output_txt}")
    except Exception as e:
        print(f"Error writing to {output_txt}: {str(e)}")
    
    print("Processing complete.")

def main():
    """Main function to run the check."""
    orig_dir = "orig"
    converted_dir = "converted"
    output_txt = "oversized_converted_files.txt"
    
    check_wem_files(orig_dir, converted_dir, output_txt)
    
    # Pause to keep console open
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()