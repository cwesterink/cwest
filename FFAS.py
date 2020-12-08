from flask import Flask, render_template, redirect, request


app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def index():
	return render_template("index.html")

@app.route('/test', methods = ['POST','GET'])
def test():
	return 'hello world helloe djvhcveic'

if __name__ == '__main__':
	app.run(debug=True)
