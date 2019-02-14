from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(application)

class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable= False)
  physics = db.Column(db.Integer)
  maths = db.Column(db.Integer)
  chemistry = db.Column(db.Integer)

  def __repr__(self):
    return f"Student('{self.name}','{self.physics}','{self.maths}','{self.chemistry}')"

@application.route('/', methods=["GET"])
def retreive_results():
  data = Student.query.all()

  output = []

  for x in data:
    student_data = {}
    student_data['id'] = x.id
    student_data['name'] = x.name
    student_data['physics'] = x.physics
    student_data['maths'] = x.maths
    student_data['chemistry'] = x.chemistry
    output.append(student_data)

  return jsonify({'student': output})

#curl -i -H "Content-Type: application/json" -X POST -d "{\"name\":\"Sivu\",\"physics\":30,\"maths\":90,\"chemistry\":10}"" http://127.0.0.1:5000/results
@application.route('/results', methods=['POST'])
def add_results():
  data = request.get_json()

  if not data or not 'name' in data:
    abort(400)

  new_student = Student(name = data['name'],physics= data['physics'],maths= data['maths'], chemistry=data['chemistry'])
  db.session.add(new_student)
  db.session.commit()

  return jsonify({'students':'New Student Created'}), 201

@application.route('/results/<int:indexId>',methods=["GET"])
def get_one_student(indexId):

  student = Student.query.filter_by(id = indexId).first()

  if not student:
    return jsonify({'message':'No user found'})

  student_data = {}
  student_data['id'] = student.id
  student_data['name'] = student.name
  student_data['physics'] = student.physics
  student_data['maths'] = student.maths
  student_data['chemistry'] = student.chemistry

  return jsonify({'student':student_data})

@application.route('/results/<int:indexId>', methods=['DELETE'])
def delete_student(indexId):

  student = Student.query.filter_by(id = indexId).first()

  if not student:
    return jsonify({'message':'No user found'})

  db.session.delete(student)
  db.session.commit()

  return jsonify({'message':'Student found and Deleted'})

@application.route('/results/<int:indexId>', methods=['PUT'])
def update_results(indexId):
  
  student = Student.query.filter_by(id = indexId).first()

  if not student:
    return jsonify({'message' : 'No Student found'})

  student.name = request.json['name']
  student.physics = request.json.get('physics', "")
  student.maths = request.json.get('maths', "")
  student.chemistry = request.json.get('chemistry', "") 
  db.session.commit()
  
  return jsonify({'student':'Pass'})
    
if __name__ == '__main__':
  db.create_all()
  application.run(debug= True)
