from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from text_cleaner import text_cleaner
from vectorize import vectorize
import requests

'''
Hugging face API
'''
API_URL = "https://api-inference.huggingface.co/models/ShreyaR/finetuned-roberta-depression"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def json_to_text(data):
	for item in data:
		highest = item[0]
		highest_label = highest['label']
		if highest_label == 'LABEL_1':
			highest_label = 'Depression'
		elif highest_label == 'LABEL_0':
			highest_label = 'Not Depression'
		else:
			highest_label = 'Unknown'

		highest_score = highest['score']
		
		return f"Most likely: {highest_label}"
     
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    output = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Entry %r>' % self.id

app.app_context().push()
db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            # print(request.form['query'])
            content = request.form['query']
            output = query({"inputs": content})
            output_text = json_to_text(output)
            print(output_text)
            # print(output_text)
            # content = text_cleaner(content)
            # output = vectorize(content)
            new_text = Entry(text=content, output=output_text)

            db.session.add(new_text)
            db.session.commit()

            return output_text
        except Exception as e:
            print("Error: ", e)
            return 'There was an error while processing the content.'
    else:
        entries = Entry.query.all()
        return entries

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = Entry.query.get_or_404(id)
    try:
        db.session.delete(entry)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting the entry.'
if __name__ == '__main__':
    app.run(debug=True)
    
