import argparse
import os

def patch_wem(orig_wem, input_wem, output_wem):
    """Patches input .wem file using bytes from original .wem and adds padding."""
    try:
        # Check if input files exist
        if not os.path.exists(orig_wem):
            print(f"Error: Original file not found: {orig_wem}")
            return False
        if not os.path.exists(input_wem):
            print(f"Error: Input file not found: {input_wem}")
            return False

        # Read original and input files
        with open(orig_wem, 'rb') as f_orig:
            orig_data = f_orig.read()
        with open(input_wem, 'rb') as f_input:
            input_data = f_input.read()

        # Check if files are long enough
        if len(orig_data) < 0x2c:
            print(f"Error: Original file too short (size: {len(orig_data)} bytes)")
            return False
        if len(input_data) < 0x2c:
            print(f"Error: Input file too short (size: {len(input_data)} bytes)")
            return False

        # Copy bytes 0x28-0x2b from original
        patched_data = bytearray(input_data)
        patched_data[0x28:0x2c] = orig_data[0x28:0x2c]

        # Add zero padding to match original size
        orig_size = len(orig_data)
        input_size = len(patched_data)
        if input_size < orig_size:
            padding = b'\x00' * (orig_size - input_size)
            patched_data.extend(padding)
        elif input_size > orig_size:
            print(f"Warning: Input file larger than original ({input_size} vs {orig_size} bytes), truncating")
            patched_data = patched_data[:orig_size]

        # Write output file
        with open(output_wem, 'wb') as f_output:
            f_output.write(patched_data)

        print(f"Successfully patched: {output_wem}")
        print(f"Bytes at 0x28-0x2b: {patched_data[0x28:0x2c].hex()}")
        print(f"Output size: {len(patched_data)} bytes")
        return True

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        return False

def batch_patch_wem(orig_dir, converted_dir, patched_dir):
    """Processes all .wem files in orig_dir, patching with converted_dir files."""
    # Check if directories exist
    if not os.path.isdir(orig_dir):
        print(f"Error: Original directory not found: {orig_dir}")
        return 0, 0
    if not os.path.isdir(converted_dir):
        print(f"Error: Converted directory not found: {converted_dir}")
        return 0, 0

    # Create patched directory if it doesn't exist
    if not os.path.isdir(patched_dir):
        try:
            os.makedirs(patched_dir)
            print(f"Created patched directory: {patched_dir}")
        except Exception as e:
            print(f"Error: Failed to create patched directory: {str(e)}")
            return 0, 0

    print(f"Starting batch patching of .wem files...")
    print(f"Original directory: {orig_dir}")
    print(f"Converted directory: {converted_dir}")
    print(f"Patched directory: {patched_dir}")
    print()

    processed = 0
    failed = 0

    # Process each .wem file in orig
    found_files = False
    for filename in os.listdir(orig_dir):
        if not filename.lower().endswith('.wem'):
            continue
        found_files = True

        orig_path = os.path.join(orig_dir, filename)
        converted_path = os.path.join(converted_dir, filename)
        output_path = os.path.join(patched_dir, filename)

        print(f"Processing {filename}...")
        success = patch_wem(orig_path, converted_path, output_path)
        if success:
            processed += 1
        else:
            failed += 1
        print()

    if not found_files:
        print(f"No .wem files found in {orig_dir}")

    # Final report
    print("Batch patching completed.")
    print(f"Processed files: {processed}")
    print(f"Failed files: {failed}")

    return processed, failed

def main():
    """Parses command-line arguments and runs batch patching."""
    parser = argparse.ArgumentParser(description="Batch patch .wem files using original and converted directories")
    parser.add_argument('--orig_dir', default='orig', help="Path to original .wem files directory (default: orig)")
    parser.add_argument('--converted_dir', default='converted', help="Path to converted .wem files directory (default: converted)")
    parser.add_argument('--patched_dir', default='patched', help="Path to output patched .wem files directory (default: patched)")

    args = parser.parse_args()

    processed, failed = batch_patch_wem(args.orig_dir, args.converted_dir, args.patched_dir)
    
    # Pause to keep console open
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()