from flask import Flask, render_template, Response, jsonify
import gunicorn
from camera import *
from spotify import fetch_playlist_tracks, emotion_playlists  # Importing the functions and dictionary from spotify.py

app = Flask(__name__)

headings = ("Name", "Album", "Artist")
df1 = music_rec()
df1 = df1.head(15)

# Fetch track information for a specific emotion playlist
@app.route('/playlist/<emotion>')
def playlist(emotion):
    if emotion in emotion_playlists:
        playlist_id = emotion_playlists[emotion]
        # Fetch tracks for the playlist (you can modify this to send data to the frontend)
        fetch_playlist_tracks(emotion, playlist_id)
        return jsonify({'status': 'success', 'emotion': emotion, 'playlist_id': playlist_id})
    else:
        return jsonify({'status': 'error', 'message': 'Emotion not found'})

@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
