from flask import Flask, jsonify
from config import Config
from courses.models import db, Department, Course

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Automatically set up the database and insert test entries
    with app.app_context():
        db.create_all() # Rebuilds all tables cleanly with correct columns
        
        # Check if data already exists so we don't duplicate it
        if not Department.query.first():
            # 1. Create departments
            dept1 = Department(name="Computer Science", code="CSE")
            dept2 = Department(name="Information Technology", code="IT")
            db.session.add_all([dept1, dept2])
            db.session.commit()

            # 2. Create courses linked to those departments
            c1 = Course(name="Python Web Frameworks", code="CS301", credits=4, department_id=dept1.id)
            c2 = Course(name="Relational Databases", code="CS302", credits=3, department_id=dept1.id)
            c3 = Course(name="Cloud Solutions", code="IT401", credits=3, department_id=dept2.id)
            db.session.add_all([c1, c2, c3])
            db.session.commit()

    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'status': 'error',
            'error': {'code': 'NOT_FOUND', 'message': 'The requested resource could not be found.'}
        }), 404

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)