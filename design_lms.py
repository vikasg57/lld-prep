# 1. Learning Management System (LMS)
# Design a basic Learning Management System for managing courses, users, and content.
# How would you implement a feature for tracking and storing students' progress?
# How would you design a grading system that supports different types of assessments
# (e.g., quizzes, assignments, exams)?


class User:
    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role  # 'student', 'instructor'


class Course:
    def __init__(self, course_id, title, description):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.modules = []  # List of Module objects


class Module:
    def __init__(self, module_id, course_id, title):
        self.module_id = module_id
        self.course_id = course_id
        self.title = title
        self.lessons = []  # List of Lesson objects


class Lesson:
    def __init__(self, lesson_id, module_id, title, content):
        self.lesson_id = lesson_id
        self.module_id = module_id
        self.title = title
        self.content = content


class Progress:
    def __init__(self, progress_id, user_id, course_id, module_id, lesson_id, status):
        self.progress_id = progress_id
        self.user_id = user_id
        self.course_id = course_id
        self.module_id = module_id
        self.lesson_id = lesson_id
        self.status = status  # 'completed', 'in-progress'


class Assessment:
    def __init__(self, assessment_id, course_id, type, max_score):
        self.assessment_id = assessment_id
        self.course_id = course_id
        self.type = type  # 'quiz', 'assignment', 'exam'
        self.max_score = max_score


class Grade:
    def __init__(self, grade_id, user_id, assessment_id, score, comments=""):
        self.grade_id = grade_id
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.score = score
        self.comments = comments


class LMS:
    def __init__(self):
        self.users = {}  # Map user_id -> User
        self.courses = {}  # Map course_id -> Course
        self.progress = []  # List of Progress objects
        self.grades = []

    def add_user(self, user):
        self.users[user.user_id] = user

    def add_course(self, course):
        self.courses[course.course_id] = course

    def update_progress(self, user_id, course_id, module_id, lesson_id, status):
        progress = Progress(len(self.progress) + 1, user_id, course_id, module_id, lesson_id, status)
        self.progress.append(progress)

    def get_user_progress(self, user_id, course_id):
        return [p for p in self.progress if p.user_id == user_id and p.course_id == course_id]

    def add_assessment(self, assessment):
        course = self.courses.get(assessment.course_id)
        if course:
            course.assessments.append(assessment)

    def add_grade(self, grade):
        self.grades.append(grade)

    def calculate_final_grade(self, user_id, course_id):
        grades = [g for g in self.grades if g.user_id == user_id and self.get_course_id_from_assessment(g.assessment_id) == course_id]
        total_score = sum(g.score for g in grades)
        total_max_score = sum(self.get_max_score_from_assessment(g.assessment_id) for g in grades)
        return total_score / total_max_score * 100 if total_max_score > 0 else 0

    def get_course_id_from_assessment(self, assessment_id):
        # Assuming assessments have unique IDs across all courses
        for course in self.courses.values():
            for assessment in course.assessments:
                if assessment.assessment_id == assessment_id:
                    return course.course_id
        return None

    def get_max_score_from_assessment(self, assessment_id):
        course_id = self.get_course_id_from_assessment(assessment_id)
        course = self.courses.get(course_id)
        if course:
            for assessment in course.assessments:
                if assessment.assessment_id == assessment_id:
                    return assessment.max_score
        return 0
