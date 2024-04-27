from core.apis.responses import APIResponse
from flask import Blueprint
from core import db
from sqlalchemy import or_
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.models.teachers import Teacher

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    assignments = Assignment.query.filter(or_(Assignment.state == 'SUBMITTED', Assignment.grade.isnot(None))).all()
    schema = AssignmentSchema(many=True)
    assignment_data = schema.dump(assignments)
    return APIResponse.respond(data=assignment_data)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.query.all()
    teacher_data = []
    # Serialize each teacher object into a dictionary
    for teacher in teachers:
        teacher_data.append({
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at,
            'updated_at': teacher.updated_at
        })
    return APIResponse.respond(data=teacher_data)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    # Load the incoming payload
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    # Search for the assignment by ID
    # assignment = Assignment.query.get(grade_assignment_payload.id)
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if assignment.state=="DRAFT":
        return {"error": "Assignment state is None"}, 400

    # Check if the assignment status is 'DRAFT'
    # if assignment.status == 'DRAFT':
    #     abort(400, description="Cannot grade a draft assignment")

    # Mark the grade for the assignment
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    
    # Commit the changes to the database
    db.session.commit()
    
    # Serialize the graded assignment
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    
    # Return the response
    return APIResponse.respond(data=graded_assignment_dump)