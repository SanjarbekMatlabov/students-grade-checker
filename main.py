from fastapi import FastAPI , HTTPException
from models import *

app = FastAPI()

students = {}
tests = {}  
test_results = {}
@app.post("/students/")
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students[student.id] = student
    return student
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]
@app.get("/students/")
def get_all_students():
    return students
@app.post("/tests/")
def create_test(test:Test):
    if test.id in tests:
        raise HTTPException(status_code=400, detail="Test ID already exists")
    tests[test.id] = test
    return test
@app.get("/tests/{test_id}")
def get_test_by_id(test_id:int):
    if test_id not in tests:
        raise HTTPException(status_code=404, detail="Test not found")
    return tests[test_id]
@app.get("/tests/")
def get_all_tests():
    return tests
@app.post("/results/")
def submit_test_result(result: TestResult):
    if result.student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if result.test_id not in tests:
        raise HTTPException(status_code=404, detail="Test not found")
    test = tests[result.test_id]
    if result.score < 0 or result.score > test.max_score:
        raise HTTPException(
            status_code=400, 
            detail=f"Score must be between 0 and {test.max_score}"
        )
    student = students[result.student_id]
    if result.test_id not in student.tests_taken:
        student.tests_taken.append(result.test_id)
    result_key = f"{result.student_id}_{result.test_id}"
    test_results[result_key] = result
    return result
@app.get("/results/student/{student_id}")
def get_student_results(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_results = [result for key, result in test_results.items()
                      if key.startswith(f"{student_id}_")]
    return student_results
@app.get("/results/test/{test_id}")
def get_test_results(test_id: int):
    if test_id not in tests:
        raise HTTPException(status_code=404, detail="Test not found")    
    test_specific_results = [result for key, result in test_results.items() 
                            if result.test_id == test_id]
    return test_specific_results
@app.get("/results/test/{test_id}/average")
def get_test_average(test_id: int):
    if test_id not in tests:
        raise HTTPException(status_code=404, detail="Test not found")
    test_scores = [result.score for result in test_results.values() if result.test_id == test_id]
    if not test_scores:
        return {"average": 0.0}
    average = sum(test_scores) / len(test_scores)
    return {"average": round(average, 2)}
@app.get("/results/test/{test_id}/highest")
def get_test_highest(test_id: int):
    if test_id not in tests:
        raise HTTPException(status_code=404, detail="Test not found")
    test_scores = [result.score for result in test_results.values() if result.test_id == test_id]
    if not test_scores:
        return {"highest": 0}
    highest = max(test_scores)
    return {"highest": highest}
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]   
    return ResponseMessage(message=f"Student with ID {student_id} has been deleted")