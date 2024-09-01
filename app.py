import os
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import zipfile
from flask import Flask, request, render_template
import smtplib
from email.message import EmailMessage



# urls = [
#     "https://www.youtube.com/watch?v=tDTN33A_OA0",  # Carrom Board
#     "https://www.youtube.com/watch?v=Kd57YHWqrsI",  # Hostel
#     "https://www.youtube.com/watch?v=JvPhpWDGXsE",  # Oye Hoye Pyar Ho Gaya
#     "https://www.youtube.com/watch?v=hzTg4zPBtDU&pp=ygUSMyBwZWcgc2hhcnJ5IG1hbm4g",  # 3 Peg
#     "https://www.youtube.com/watch?v=kt2Cu_cCPcA&pp=ygUVcm9vaCBzb25nIHNoYXJyeSBtYWFu",  # Rooh
#     "https://www.youtube.com/watch?v=_J0u_bVxIMY&pp=ygUNZGlsIGRhIGRpbWFhZw%3D%3D",  # Dil Da Dimaag
#     "https://www.youtube.com/watch?v=wBlTNeuHOUs&pp=ygUNbXVuZGEgYmhhbCBkaQ%3D%3D",  # Munda Bhal Di
#     "https://www.youtube.com/watch?v=qGFmT1iIm2A&pp=ygUOcHUgZGkgeWFhcml5YW4%3D",  # Yaar te Paisa
#     "https://www.youtube.com/watch?v=_PukEpqzIpk&pp=ygUVZW5kIGJhbmRlIHNoYXJyeSBtYWFu",  # End Bande
#     "https://www.youtube.com/watch?v=qGFmT1iIm2A&pp=ygUOcHUgZGkgeWFhcml5YW4%3D",  # P.U Diyan Yaarian
#     "https://www.youtube.com/watch?v=PDlw1Tn-PVk&pp=ygUKY3V0ZSBtdW5kYQ%3D%3D",  # Cute Munda
#     "https://www.youtube.com/watch?v=h7rrFnGiY1I&pp=ygUIdmFkZGEgYmg%3D",  # Vadda Bai
#     "https://www.youtube.com/watch?v=iiQmg8Sldu8&pp=ygUMeWFhciBhbm11bGxl",  # Yaar Anmulle
#     "https://www.youtube.com/watch?v=zPHms40Ws38&pp=ygURY2hhbmRpZ2FyaCB3YWxpeWU%3D",  # Chandigarh Waliye
#     "https://www.youtube.com/watch?v=e-0YnJlFPeE&pp=ygUUbG92ZSB5b3Ugc2hhcnJ5IG1hYW4%3D",  # Love You
#     "https://www.youtube.com/watch?v=bpgBe1G5If4&pp=ygUVbWVyaSBiZWJlIHNoYXJyeSBtYW5u",  # Meri Bebe
#     "https://www.youtube.com/watch?v=f7cxVDl67Z0&pp=ygUZZ2FhbCBuaSBrYWRuaSBzaGFycnkgbWFhbg%3D%3D",  # yaat jigree
#     "https://www.youtube.com/watch?v=uXFxgx--iE8&pp=ygUYdHJhbnNwb3J0aXllIHNoYXJyeSBtYWFu",  # Transportiye
#     "https://www.youtube.com/watch?v=9Cp-yg0Nzyw&pp=ygUac2hhYWRpIGRvdCBjb20gc2hhcnJ5IG1hYW4%3D",  # Shaadi Dot Com
#     "https://www.youtube.com/watch?v=tR6XkXy-gjY&pp=ygUYamF0dCBkaSBjbGlwIHNoYXJyeSBtYWFu"   # Yankne
# ]


# ydl_opts = {
#     'format': 'best',  # or 'mp4'
#     'outtmpl': 'video_%(autonumber)s.%(ext)s',  # Use autonumber for unique filenames
#     'noplaylist': True,  # Download only the video, not any playlist
# }

# with YoutubeDL(ydl_opts) as ydl:
#     ydl.download(urls)

# for i in range(1, 21):
#     video = VideoFileClip(f"video_{i:05}.mp4")
#     audio = video.audio
#     audio.write_audiofile(f"audio_{i:05}.mp3")

# for i in range(1, 21):
#     audio = AudioSegment.from_file(f"audio_{i:05}.mp3")
#     first_30_seconds = audio[:30000] 
#     first_30_seconds.export(f"audio_{i}_30sec.mp3", format="mp3")

# combined = AudioSegment.empty()

# for i in range(1, 21):
#     audio = AudioSegment.from_file(f"audio_{i}_30sec.mp3")
#     combined += audio
#     combined.export("mashup.mp3", format="mp3")

with zipfile.ZipFile("mashup.zip", 'w') as zf:
    zf.write("mashup.mp3")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_mashup_request', methods=['POST'])
def submit_mashup_request():
  
    num_songs = request.form['num_songs']
    artist_name = request.form['artist_name']
    video_length = request.form['video_length']
    email = request.form['email']

    sender_email = "aagarwal_be22@thapar.edu"
    password = "phdw wnpi wgec xiht"

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Song Mashup Request"

    body = f"""
    Number of Songs: {num_songs}
    Artist Name: {artist_name}
    Video Length (seconds): {video_length}
    """
    msg.set_content(body)

    zip_file_path = 'mashup.zip'
    
    with open(zip_file_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='zip', filename='mashup.zip')

        
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        return "Request submitted successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=False)
