from flask import Flask, render_template, request, redirect, url_for
import cv2
import random
from sock_matcher import compare_socks_from_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('static/sock.jpg', frame)
    cap.release()
    return redirect(url_for('result'))

@app.route('/result')
def result():
    image_path = 'static/sock.jpg'
    similarity, color_diff = compare_socks_from_file(image_path)

    if similarity is None:
        return "Image not found or invalid."

    is_pair = similarity > 0.85 and color_diff < 50

    smell_guess = random.choice(["Left sock smells bad", "Right sock smells bad", "Both smell okay"])

    return render_template('result.html',
                           similarity=round(similarity, 3),
                           color_diff=round(color_diff, 2),
                           is_pair=is_pair,
                           smell_guess=smell_guess)

if __name__ == '__main__':
    app.run(debug=True)

