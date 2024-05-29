from flask import Flask, render_template, request, redirect
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

def getAverageL(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w*h))

def convertImageToAscii(image, cols, scale, moreLevels):
    global gscale1, gscale2

    image = image.convert('L')
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale
    rows = int(H/h)

    if cols > W or rows > H:
        return "Image too small for specified cols!"
    
    aimg = []
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        if j == rows - 1:
            y2 = H
        aimg.append("")
        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            if i == cols - 1:
                x2 = W
            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))
            if moreLevels:
                gsval = gscale1[int((avg * 64) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]
            aimg[j] += gsval

    return "\n".join(aimg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['Post'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        image = Image.open(file.stream)
        ascii_art = convertImageToAscii(image, 160, 0.43, True)
        return render_template('result.html', ascii_art=ascii_art)
    
if __name__ == '__main__':
    app.run(debug=True)