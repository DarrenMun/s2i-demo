from flask import Flask,render_template, redirect, url_for,request, jsonify, abort
application = Flask(__name__)

students = [
    {
        'id': 1,
        'name': 'Darren',
        'physics': 80,
        'maths': 60,
        'chemistry': 45
    },
    {
        'id': 2,
        'name': 'Jerry',
        'physics': 50, 
        'maths': 45,
        'chemistry': 45
    }
]

@application.route('/', methods=['GET'])
def student():
   return jsonify({'student':students})

@application.route('/results/<int:indexId>',methods=["GET"])
def get_id(indexId):
   studentId = [student for student in students if student['id'] == indexId]
   if len(studentId) == 0:
      abort(404)
   return jsonify({'Student':studentId[0]})

@application.route('/results/<int:indexId>', methods=['PUT'])
def update_results(indexId):
  if request.method == 'PUT':
    studentId = [student for student in students if student['id'] == indexId]
    if len(studentId) == 0:
      abort(404)
    if not request.json:
      abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
      abort(400)
    if 'physics' in request.json and type(request.json['physics']) != int:
      abort(400)
    if 'maths' in request.json and type(request.json['maths']) != int:
      abort(404)
    if 'chemistry' in request.json and type(request.json['chemistry']) != int:
      abort(400)

    studentId[0]['name'] = request.json.get('name',studentId[0]['name'])
    studentId[0]['physics'] = request.json.get('physics',studentId[0]['physics'])
    studentId[0]['maths'] = request.json.get('maths',studentId[0]['maths'])
    studentId[0]['chemistry'] = request.json.get('chemistry',studentId[0]['chemistry'])
    return jsonify({'Updated Student':studentId[0]})

@application.route('/results',methods=['POST'])
def add_results() : 
   if not request.json or not 'name' in request.json:    
      abort(400)

   student = {
         'id': students[-1]['id'] + 1,
         'name': request.json['name'],
         'physics': request.json.get('physics',""),
         'maths': request.json.get('maths',""),
         'chemistry': request.json.get('chemistry',"")
      }
  
   students.append(student)
   return jsonify({'students':student}), 201

@application.route('/results/<int:indexId>', methods=['DELETE'])
def delete_student(indexId):
  if request.method == 'DELETE':
    studentId = [student for student in students if student['id'] == indexId]
    if len(studentId) == 0:
      abort(404)
    students.remove(studentId[0])
    return jsonify({'Removed': True})


if __name__ == "__main__":
    application.run()
