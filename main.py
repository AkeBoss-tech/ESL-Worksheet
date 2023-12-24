from flask import Flask, render_template_string, render_template
import util
import markdown

app = Flask(__name__)

@app.route('/generate/fill_worksheet', methods=['GET'])
def generate_fill_worksheet():
    worksheet = util.generate_fill_worksheet(10)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    with open("output.html", "w") as f:
        f.write(html)
    return render_template('default.html', markdown_content=html)

@app.route('/generate/worksheet', methods=['GET'])
def generate_full_worksheet():
    worksheet = util.generate_full_worksheet(util.random_story())
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    return render_template('default.html', markdown_content=html)

@app.route('/generate/rearrange_worksheet', methods=['GET'])
def generate_rearrange_worksheet():
    worksheet = util.generate_rearrange_worksheet(util.random_story(), 10)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    return render_template('default.html', markdown_content=html)

@app.route('/generate/vocab_worksheet', methods=['GET'])
def generate_vocab_worksheet():
    worksheet = util.generate_vocab_worksheet(util.random_story(), 20)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    with open("output.html", "w") as f:
        f.write(html)
    return render_template('default.html', markdown_content=html)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)