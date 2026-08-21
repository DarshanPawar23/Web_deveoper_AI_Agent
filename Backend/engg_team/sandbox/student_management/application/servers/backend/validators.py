from pydantic import BaseModel class StudentSchema(BaseModel):
 name: str
 age: int

def validate_student_data(student: dict | None = None) -> None:
for item in ['name', 'age']:
 ...