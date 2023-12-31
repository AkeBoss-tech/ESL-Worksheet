from flask import Flask, render_template_string, render_template, request
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
    worksheet = util.keep_trying_rearrange_worksheet(10)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    return render_template('default.html', markdown_content=html)

@app.route('/generate/vocab_worksheet', methods=['GET'])
def generate_vocab_worksheet():
    worksheet = util.generate_vocab_worksheet(util.random_story(), 20)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    with open("output.html", "w") as f:
        f.write(html)
    return render_template('default.html', markdown_content=html)

# add routes that return worksheets for different levels using random_story_level(level)
@app.route('/generate/worksheet/<level>', methods=['GET'])
def generate_full_worksheet2(level):
    if level not in ['1', '2', '3', '4', '5', '6']:
        return render_template('index.html')
    worksheet = f"# Level {level}\n\n" + util.generate_full_worksheet(util.random_story_level(level))
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    with open("output.html", "w") as f:
        f.write(html)
    return render_template('default.html', markdown_content=html)

# also add rearrange and vocab routes for different levels
@app.route('/generate/rearrange_worksheet/<level>', methods=['GET'])
def generate_rearrange_worksheet2(level):
    if level not in ['1', '2', '3', '4', '5', '6']:
        return render_template('index.html')
    worksheet = f"# Level {level}\n\n" + util.generate_rearrange_worksheet(util.random_story_level(level), 10)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    return render_template('default.html', markdown_content=html)

@app.route('/generate/vocab_worksheet/<level>', methods=['GET'])
def generate_vocab_worksheet2(level):
    if level not in ['1', '2', '3', '4', '5', '6']:
        return render_template('index.html')
    worksheet = f"# Level {level}\n\n" + util.generate_vocab_worksheet(util.random_story_level(level), 20)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    with open("output.html", "w") as f:
        f.write(html)
    return render_template('default.html', markdown_content=html)

@app.route('/generate/custom', methods=['GET'])
def generate_custom():
    # get the story from the form
    story = request.args.get('story')
    
    story = story.split('\n')
    print("hey bro", story)
    worksheet = util.generate_full_worksheet(story)
    html = markdown.markdown(worksheet, extensions=['markdown.extensions.tables'])
    return render_template('default.html', markdown_content=html)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)