from flask import Flask, render_template, request
import spacy
import os
from spacy import displacy
from flaskext.markdown import Markdown


nlp = spacy.load('en_core_web_sm')
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


app = Flask(__name__,static_folder='static')
Markdown(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/extract', methods=["GET", "POST"])
def extract():
	if request.method == 'POST':
		raw_text = request.form['rawtext']
		docx = nlp(raw_text)
		html = displacy.render(docx,style="ent")
		html = html.replace("\n\n", "\n")
		result = HTML_WRAPPER.format(html)
	return render_template('result.html', rawtext=raw_text, result=result,home=os.getenv("ROUTE"))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8050, debug=False)