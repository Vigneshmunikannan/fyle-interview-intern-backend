import json
from flask import Blueprint,request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.assignments import GradeEnum


from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    header=request.headers.get('X-Principal')
    header_data = json.loads(header)
    teacher_id = header_data.get('teacher_id')
    teachers_assignments = Assignment.filter(Assignment.teacher_id == teacher_id).all()
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    header=request.headers.get('X-Principal')
    header_data = json.loads(header)
    if incoming_payload['grade'] not in [grade.value for grade in GradeEnum]:
        print("validate")
        return {"error": "ValidationError"}, 400
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    teacher_id = header_data.get('teacher_id')  
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if assignment is None:
        return {"error": "FyleError"}, 404
    if assignment.teacher_id!=teacher_id:
     return  {"error": "FyleError"}, 400
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
