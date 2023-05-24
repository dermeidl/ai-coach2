from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [{
  'id': 1,
  'title': 'Data Analyst',
  'location': 'Linz',
  'salary': '5.000€'
}, {
  'id': 2,
  'title': 'Data Engeneer',
  'location': 'Linz',
  'salary': '5.000€'
}, {
  'id': 3,
  'title': 'Frontend Engeneer',
  'location': 'Remote',
  'salary': '5.000€'
}]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name='NeoClarity')


@app.route('/api/jobs')
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
