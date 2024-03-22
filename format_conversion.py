import logging
import os
import subprocess

def convert_to_format(input_file, output_path, format):
    name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_path, f'{name}.{format}')
    
    logging.info(f'Input file: {input_file}')
    logging.info(f'Output file: {output_file}')
    
    executable_path = os.path.abspath(__file__)
    executable_dir = os.path.dirname(executable_path)
    ffmpeg_path = os.path.join(executable_dir, "ffmpeg", "bin", "ffmpeg.exe")
    command = [ffmpeg_path, '-i', input_file, '-c:v', 'copy', '-c:a', 'copy','-preset', 'ultrafast', '-y', output_file]
    if format == 'avi' or format == 'mkv' or format == 'mov' or format == 'flv':
        command[4] = 'h264'
        command[6] = 'aac'
    elif format == 'wmv':
        command[4] = 'wmv2'
        command[6] = 'wmav2'
    else:
        raise ValueError("Invalid format: " + format)
    subprocess.run(command, check=True)