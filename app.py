from flask import Flask, request, render_template_string
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

HTML = '''
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="image" accept="image/*"><br><br>
  <button type="submit">Extract colours</button>
</form>
{% for hex, pct in colours %}
  <div style="display:inline-block;text-align:center;margin:8px">
    <div style="width:80px;height:60px;background:{{hex}};border-radius:8px"></div>
    <p>{{hex}}<br>{{pct}}%</p>
  </div>
{% endfor %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    colours = []
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file).convert('RGB').resize((100, 100))
        pixels = np.array(img).reshape(-1, 3)
        pixels = (pixels // 16) * 16  # quantise
        unique, counts = np.unique(pixels, axis=0, return_counts=True)
        top10 = unique[np.argsort(-counts)[:10]]
        top_counts = sorted(counts, reverse=True)[:10]
        total = 100 * 100
        for rgb, n in zip(top10, top_counts):
            hex_code = '#{:02X}{:02X}{:02X}'.format(*rgb)
            pct = round((n / total) * 100, 1)
            colours.append((hex_code, pct))
    return render_template_string(HTML, colours=colours)

if __name__ == '__main__':
    app.run(debug=True)