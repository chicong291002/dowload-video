import logging
import math
import os
import shutil
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from html import unescape
import requests
from pytube import YouTube


def download_video(youtube, dir_name):
    try:
        # Lấy video
        video_stream = youtube.streams.order_by('resolution').desc().first()
        if video_stream is not None:
            # sử dụng đường dẫn tuyệt đối để tạo tệp tạm thời
            with tempfile.TemporaryDirectory(dir=dir_name) as tmpdir:
                logging.info(f'tmp_dir: {tmpdir}')
                video_path = video_stream.download(output_path=tmpdir,filename=f'video_{video_stream.resolution}_{video_stream.default_filename}'
                )
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False, dir=tmpdir) as tf_audio:
                    audio_stream = youtube.streams.filter(only_audio=True).first()
                    audio_stream.stream_to_buffer(tf_audio)
                    audio_path = tf_audio.name
                    logging.info(f'audio_tmp {tf_audio.name}')

                # Sử dụng ffmpeg để nối video và audio, ghi ra tệp tạm thời
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False, dir=tmpdir) as tmp_video_file:
                    ffmpeg_path = os.path.join("/usr","bin", "ffmpeg")
                    logging.info(f'FFMPEG path: {ffmpeg_path}')
                    command = [ffmpeg_path, '-i', video_path, '-i', audio_path,'-c:v', 'copy', '-c:a', 'libmp3lame', '-y', tmp_video_file.name]
                    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Sao chép tệp tin từ thư mục tạm thời vào thư mục đích
                shutil.copy(tmp_video_file.name, video_path)
                logging.info(f'Video path 1: {video_path}')
                # sử dụng đường dẫn tuyệt đối để sao chép tệp tin
                shutil.copy2(video_path, os.path.join(
                    dir_name, os.path.basename(video_path)))
                logging.info(
                    f'Video_path 2: {os.path.join(dir_name, os.path.basename(video_path))}')
                # Xóa các tệp tin tạm thời
                os.remove(tmp_video_file.name)
                os.remove(tf_audio.name)
            logging.info('Downloading video successful')
        else:
            logging.error('Error downloading video')
    except Exception as e:
        logging.error(f'Error downloading video {str(e)}')


def download_audio(youtube, dir_name):
    # Lấy audio
    audio = youtube.streams.filter(only_audio=True).order_by('abr').desc().first()
    if audio is not None:
        audio.download(output_path=dir_name,filename=f'audio_{audio.default_filename}')
        logging.info('Downloading audio successful')
    else:
        logging.error('Error downloading audio')


def download_thumbnail(youtube, youtube_dir, dir_name):
    # Lấy thumbnail video
    thumbnail = youtube.thumbnail_url
    if thumbnail:
        response = requests.get(thumbnail)
        with open(os.path.join(dir_name, f'thumbnail_{youtube_dir}.jpg'), 'wb') as f:
            f.write(response.content)
        logging.info('Downloading thumbnail successful')
    else:
        logging.error('Error downloading thumbnail')

# Recode 2 functions in pytube's Caption class because it is faulty
def float_to_srt_time_format(d: float) -> str:
    fraction, whole = math.modf(d)
    time_fmt = time.strftime("%H:%M:%S,", time.gmtime(whole))
    ms = f"{fraction:.3f}".replace("0.", "")
    return time_fmt + ms


def xml_caption_to_srt(xml_captions: str) -> str:
    segments = []
    root = ET.fromstring(xml_captions)
    for i, child in enumerate(root.findall('.//p[@t][@d]')):
        if child.findall('.//s'):
            text = ""
            for child_s in child.findall('.//s'):
                text += child_s.text or ""
        else:
            text = child.text or ""
        caption = unescape(text.replace("\n", " ").replace("  ", " "),)
        duration = float(child.get('d'))/1000
        start = float(child.get('t'))/1000
        end = start + duration
        sequence_number = i + 1  # convert from 0-indexed to 1.
        line = f'{sequence_number}\n{float_to_srt_time_format(start)} --> {float_to_srt_time_format(end)}\n{caption}\n'
        segments.append(line)
    return "\n".join(segments).strip()


def get_youtube_streams(url):
    try:
        youtube = YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=True
        )
    except Exception:
        return f'Error link "{url}"!'
    return youtube
