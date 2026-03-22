import yt_dlp
from urllib.parse import urlparse, parse_qs

video_input = input("Entrez l'ID ou le lien complet de la vidéo YouTube : ").strip()

# Supporte ID simple ou lien complet
if len(video_input) == 11 and not any(c in video_input for c in "/?&="):
    url = f"https://www.youtube.com/watch?v={video_input}"
else:
    parsed = urlparse(video_input)
    if "youtu.be" in parsed.netloc:
        video_id = parsed.path.lstrip("/")
    else:
        qs = parse_qs(parsed.query)
        video_id = qs.get("v", [None])[0]
    if not video_id:
        raise ValueError("Impossible d'extraire l'ID de la vidéo")
    url = f"https://www.youtube.com/watch?v={video_id}"

cookies_path = None  # ou "cookies.txt" si nécessaire
output_file = "video.mp4"

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'outtmpl': output_file,
    'ffmpeg_location': r'C:\ffmpeg\bin\ffmpeg.exe',
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'  # assure la sortie en mp4
    }],
    'postprocessor_args': ['-c:a', 'aac'],  # convertit l'audio en AAC
    'cookies': cookies_path,
    'quiet': False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Téléchargement terminé : {output_file}")

except Exception as e:
    print("Erreur :", e)
