# NierWemPatcher

A tool for patching .wem audio files before packing them into .wsp archives for the game NieR: Automata.

## Overview

The primary tool for working with the game's audio files is **NieR-Audio-Tools**.

Direct replacement of .wem files causes the game to crash. Through detailed analysis, including byte-by-byte comparison in a hex editor with the assistance of **Grok**, the following was determined:

### Key Findings

1. **Byte Values at Positions 0x28 and 0x29**:
   - After processing in Wwise, .wem files have values `0x28 = 01`, `0x29 = 41`.
   - In original .wem files, the values are `0x28 = 04`, `0x29 = 00`.
2. **Padding in Original Files**:
   - Original .wem files contain several `00 00` byte sequences at the end, which are absent in Wwise-processed files.

### Requirements for Successful Patching

To ensure compatibility with NieR: Automata, patched .wem files must meet the following conditions:

1. The total size of the new .wem file must not exceed the size of the original file.
2. The audio data length must not exceed that of the original, which can be verified using the `check_wem_audio_length.py` script.
3. Byte values at positions `0x28` and `0x29` must be set to `0x28 = 04`, `0x29 = 00` using the `patch_wem.py` script.
4. `00 00` byte sequences must be added to the end of the .wem file to match the original file's size and data length, which is handled by the `patch_wem.py` script.

## Workflow

The typical process for replacing audio files in NieR: Automata includes the following steps:

1. Unpack .wsp archives using **NieR-Audio-Tools**.
2. Convert original .wem files to .wav format for reference and audio adjustment.
3. Prepare new .wav files (48.0 kHz, Mono, 16 bits) to replace the originals.
4. Convert new .wav files to .wem format using **Wwise 2016** (Vorbis Quality High, 48.0 kHz, Mono, Vorbis, Quality Level 4).
5. Patch the .wem files for compatibility using the provided scripts.
6. Pack the patched .wem files into .wsp archives using **NieR-Audio-Tools**.

## Usage Instructions

1. Place original .wem files in the `orig` folder.
2. Place Wwise-converted .wem files in the `converted` folder.
3. Verify audio data length using the `check_wem_audio_length.py` script. If necessary, shorten the duration or reduce the bitrate of the audio files.
4. Apply the patch to .wem files using the `patch_wem.py` script. Patched files ready for packing will be saved in the `patched` folder.

## Tools

- `check_wem_audio_length.py`: Verifies that the audio data length in converted .wem files does not exceed that of the originals.
- `patch_wem.py`: Applies necessary byte changes and adds padding to the end of .wem files to match the structure of the original files.

## Additional Resources

- Telegram: [ainyashaprime](https://t.me/ainyashaprime)
- Demonstration video: [YouTube](https://youtube.com/shorts/4wRLVO6P2VY?feature=share)