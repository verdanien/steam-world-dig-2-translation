import os
import zlib
from pathlib import Path

from swd2.core.extlogging import LogTemplates, ExtLogger

def check_files(source_file:Path, target_file:Path, overwrite:bool) -> bool:
    input_violation = check_source_file(source_file)
    target_violation = check_target_file(target_file, overwrite)
    if input_violation is not None:
        ExtLogger.error(input_violation)
        return False
    if target_violation is not None:
        ExtLogger.error(target_violation)
        return False
    return True

def check_source_file(file:Path) -> str:
    if not file.exists():
        return f'Source not exists: {LogTemplates.variable(file)} !'
    elif not file.is_file():
        return f'It is not a file: {LogTemplates.variable(file)} !'
    elif not os.access(file, os.W_OK):
        return f'No permission to source file: {LogTemplates.variable(file)} !'
    else:
        return None;


def check_target_file(file:Path, overwrite:bool) -> str:
    if file.exists():
        if not overwrite:
            return f'Target already exists and cannot be overwritten: {LogTemplates.variable(file)} !'
        elif not file.is_file():
            return f'It is not a file: {LogTemplates.variable(file)} !'
        elif not os.access(file, os.W_OK):
            return f'No permission to target file: {LogTemplates.variable(file)} !'
    else:
        return None;


def decompress(input_file: Path, output_file: Path, overwrite: bool = False):
    if not check_files(input_file, output_file, overwrite):
        ExtLogger.error(f'Decompression of file {LogTemplates.variable(input_file)} failed!')
        return

    try:
        ExtLogger.info(f'Reading source file: {LogTemplates.variable(input_file)}')
        with open(input_file, 'rb') as f:
            compressed_data = f.read()

        # Skip the custom header (first 4 bytes) and decompress the rest
        decompressed_data = zlib.decompress(compressed_data[4:])

        ExtLogger.info(f'Write decompressed file: {LogTemplates.variable(output_file)}')
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)
        ExtLogger.info(f'Decompression completed. Output file: {LogTemplates.variable(output_file)}')
    except FileNotFoundError:
        ExtLogger.error(f'Decompression failed! File not exists: {LogTemplates.variable(input_file)} !')
    except PermissionError:
        ExtLogger.error(f'Decompression failed! Lack permission to source file: {LogTemplates.variable(input_file)} !')


def compress(input_file: Path, output_file: Path, overwrite: bool = False):
    if not check_files(input_file, output_file, overwrite):
        ExtLogger.error(f'Compression of file {LogTemplates.variable(input_file)} failed!')
        return

    try:
        mapping = {
            'ą': 'à',
            'Ą': 'À',
            'ę': 'è',
            'Ę': 'È',
            'ż': 'å',
            'Ż': 'Å',
            'ź': 'á',
            'Ź': 'Á',
            'ń': 'ñ',
            'Ń': 'Ñ',
            'ć': 'é',
            'Ć': 'É',
            'ś': 'ö',
            'Ś': 'Ö',
            'Ł': 'Г'
        }
        translation_table = str.maketrans(mapping)

        ExtLogger.info(f'Reading source file: {LogTemplates.variable(input_file)}')
        with open(input_file, 'rb') as f:
            content = f.read()

        text = content.decode("utf-8")
        translated_text = text.translate(translation_table)
        modified_content = translated_text.encode("utf-8")

        compressor = zlib.compressobj(9, zlib.DEFLATED, 15)
        new_compressed = compressor.compress(modified_content)
        new_compressed += compressor.flush()

        new_header = len(modified_content).to_bytes(4, 'little')
        new_file_data = new_header + new_compressed

        ExtLogger.info(f'Writing target file: {LogTemplates.variable(input_file)}')
        with open(output_file, "wb") as f:
            f.write(new_file_data)
        ExtLogger.info(f'Compression completed. Output file: {LogTemplates.variable(output_file)}')
    except FileNotFoundError:
        ExtLogger.error(f'Compression failed! Source file not exists: {LogTemplates.variable(input_file)} !')
    except PermissionError:
        ExtLogger.error(f'Compression failed! Lack permission to source file: {LogTemplates.variable(input_file)} !')