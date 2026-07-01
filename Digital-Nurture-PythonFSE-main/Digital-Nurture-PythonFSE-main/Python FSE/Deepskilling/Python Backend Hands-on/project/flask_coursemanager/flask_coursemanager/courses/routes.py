from flask import Blueprint, jsonify, request
from courses.models import db, Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def make_response_json(data, status_code=200):
    return jsonify({
        'status': 'success',
        'data': data
    }), status_code

# GET ALL COURSES
@courses_bp.route('/', methods=['GET'])
def get_courses():
    all_courses = Course.query.all()
    return make_response_json([course.to_dict() for course in all_courses])

# CREATE COURSE
@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    required = ['name', 'code', 'credits', 'department_id']
    if any(k not in data for k in required):
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400

    new_course = Course(
        name=data['name'],
        code=data['code'],
        credits=int(data['credits']),
        department_id=int(data['department_id'])
    )
    db.session.add(new_course)
    db.session.commit()
    return make_response_json(new_course.to_dict(), 201)

# GET SINGLE COURSE WITH SHORTCUT
@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict())

# UPDATE COURSE
@courses_bp.route('/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json() or {}
    
    course.name = data.get('name', course.name)
    course.code = data.get('code', course.code)
    course.credits = int(data.get('credits', course.credits))
    
    db.session.commit()
    return make_response_json(course.to_dict())

# DELETE COURSE
@courses_bp.route('/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'message': f'Course {course_id} successfully deleted'})

# CUSTOM JOIN SUB-ROUTE (Step 56)
@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_enrolled_students(course_id):
    # Enforce course verification validation check
    Course.query.get_or_404(course_id)
    
    # Execute relational table JOIN via ORM engine query layers
    enrolled_students = db.session.query(Student).\
        join(Enrollment, Student.id == Enrollment.student_id).\
        filter(Enrollment.course_id == course_id).all()
        
    return make_response_json([student.to_dict() for student in enrolled_students])