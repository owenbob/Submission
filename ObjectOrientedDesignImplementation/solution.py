from exceptions import (
    AlreadyEnrolledException,
    InvalidChoiceException,
    InvalidCourseException,
    InvalidCourseTeacherException,
    InvalidNumberOfQuestionsException,
    InvalidQuestionException,
    InvalidQuizException,
    InvalidVerificationException,
    InvalidStudentException,
    MultipleChoicesException,
    UnassignedQuizException,
    UnEnrolledCourseException,
    UnmarkedQuizException,
    UnsubmittedQuizException
    )


# Course Grading
COURSE_GRADING_STANDARD = {
    "A": [x for x in range(80, 101)],
    "B": [x for x in range(70, 80)],
    "C": [x for x in range(60, 70)],
    "D": [x for x in range(50, 60)],
    "E": [x for x in range(40, 50)],
    "F": [x for x in range(0, 40)]
}


class Course(object):
    def __init__(self, course_name, course_code, semester, course_teacher):
        """Initialize course object."""
        self.course_name = course_name
        self.course_code = course_code
        self.semester = semester
        self.quizzes = []
        self.course_grade = None

        if not isinstance(course_teacher, Teacher):
            raise InvalidCourseTeacherException(
                "Please provide a valid Teacher."
            )
        self.course_teacher = course_teacher


class Question(object):
    def __init__(self, number, answer=None, choices=[]):
        """Initialize question object."""
        self.number = number
        self.answer = answer

        """
        NOTE: The assumption is an answer is wrong by default hence using
        False to denote that the answer is wrong
        """
        self.answer_result = False
        if len(choices) < 2:
            raise MultipleChoicesException("Pls provide multiple choices.")
        self.choices = choices


class Quiz(object):
    def __init__(self, quiz_name, quiz_code, course, questions=[]):
        """Initialize quiz object."""
        self.quiz_name = quiz_name
        self.quiz_code = quiz_code
        self.course = course
        self.student = None
        self.submitted = False
        self.marked = False
        self.grade = None
        self.teacher_graded = False

        if len(questions) < 2:
            raise InvalidNumberOfQuestionsException(
                "Please add more questions."
            )

        for question in questions:
            if not isinstance(question, Question):
                raise InvalidQuestionException(
                    "Please provide only valid questions."
                )
        self.questions = questions


class Student(object):
    def __init__(self, first_name, last_name, student_number):
        """Initialize a student object."""
        self.first_name = first_name
        self.last_name = last_name
        self.student_number = student_number
        self.grades = {}
        self.enrolled_courses = []
        self.assigned_quizzes = []

    def enroll_into_course(self, course):
        """Enrol a student into a course."""
        self._verify_course(course)
        self.enrolled_courses.append(course)

    def answer_quiz(self, quiz, answers=[]):
        """Enable student to answer a quiz."""

        """
        NOTE: We assume that the student provides a list of answers that
        with dictionaries that correspond to question number as a key and
        students answer as a value.
        """

        self._verify_quiz(quiz)
        for answer in answers:
            for question in quiz.questions:
                if list(answer.keys())[0] == question.number:
                    choice = answer.get(question.number)
                    self._verify_choice(choice, question)
                    question.answer = choice

    def submit_quiz(self, quiz):
        """Enable a student to submit a quiz."""
        self._verify_quiz(quiz)
        quiz.submitted = True

    def _verify_course(self, course):
        """
        Verify a course.

        This is by checking that the course provided is a valid Course object.
        It also check whether the Course has already been enrolled into.
        """
        if not isinstance(course, Course):
            raise InvalidCourseException("Please provide valid Course.")
        if course in self.enrolled_courses:
            raise AlreadyEnrolledException(
                "The student has already enrolled into this course."
            )

    def _verify_quiz(self, quiz):
        """
        Verify a quiz.

        This is by checking that the quiz provide is a valid Quiz object.
        It also checks that the student is assigned to this quiz.
        """
        if not isinstance(quiz, Quiz):
            raise InvalidQuizException("Please provide valid quiz.")
        if not quiz.student:
            raise UnassignedQuizException(
                "Please ensure this quiz is assigned to you first."
            )
        if self.student_number != quiz.student.student_number:
            raise InvalidVerificationException(
                "Please submit the quiz assigned to you."
            )

    def _verify_choice(self, choice, question):
        """
        Verify a choice.

        Verification is done by checking the choice provided is a valid
        choice for the question specified.
        """
        if choice not in question.choices:
            raise InvalidChoiceException(
                "Please provide an answer from available choices"
            )


class Teacher(object):
    def __init__(self, first_name, last_name, teacher_number):
        """Initialize a teacher object."""

        self.first_name = first_name
        self.last_name = last_name
        self.teacher_number = teacher_number

    def create_quiz(self, quiz_name, quiz_code, course, questions=[]):
        """Create a quiz."""
        self._verify_course(course)
        quiz = Quiz(
            quiz_name=quiz_name,
            quiz_code=quiz_code,
            course=course,
            questions=questions
        )
        course.quizzes.append(quiz)
        return quiz

    def assign_quiz(self, quiz, student):
        """Assign a quiz to a student."""
        self._verify_quiz(quiz)
        self._verify_student(student)
        quiz.student = student
        return quiz

    def calculate_total_grade(self, student, course):
        """
        Calculate a students total grade.

        params:
            - student
            - course

        This function calculates the total grade for the semester by
        matching the students average grade for all the quizzes the student did
        for the course to the standard course grading.
        """
        self._verify_student(student)
        self._verify_course(course)
        self._verify_student_enrollment(student, course)
        student_quizzes = [
            quiz for quiz in course.quizzes if quiz.student == student and quiz.teacher_graded  # noqa: E501
        ]
        all_quiz_grades = [quiz.grade for quiz in student_quizzes]

        # calculate the average grade
        average_grade = sum(all_quiz_grades)/len(all_quiz_grades)

        course_grade = self._get_course_grade(int(average_grade))
        course.course_grade = course_grade

    def grade_quiz(self, quiz):
        """
        Grade a quiz.

        params:
            - quiz

        This function assigns a grade to a quiz by calculating the percentage
        of the number of correct answers
        """
        self._verify_quiz(quiz)
        self._verify_quiz_marking(quiz)
        correct_answers = 0
        for question in quiz.questions:
            if question.answer_result:
                correct_answers += 1

        quiz_grade = int(correct_answers/len(quiz.questions)*100)
        quiz.grade = quiz_grade
        quiz.teacher_graded = True

    def mark_quiz(self, quiz, marking_guide):
        """
        Mark all the questions in a submitted quiz.

        params:
            - quiz
            - marking_guide

        This func updates all quiz question answer_result value to determine
        whether the answer submitted is correct(True) or wrong(False).
        By default this value is False as unanswered question if submitted is
        wrong.
        """

        """ NOTE: We assume that the teacher provides a marking guide that
        with dictionaries that correspond to question number as a key and
        correct answer as a value.
        """
        self._verify_quiz(quiz)
        self._verify_quiz_submission(quiz)
        for answer in marking_guide:
            for question in quiz.questions:
                qn_number = list(answer.keys())[0]
                correct_answer = answer.get(qn_number)
                if qn_number == question.number and correct_answer == question.answer:  # noqa: E501
                    question.answer_result = True
                quiz.marked = True

    def _get_course_grade(self, average_grade):
        """
        Return the matching course grade.

        params:
            - average_grade

        This function matches the average grade of all quizzes for the course
        to the standard course grading.
        """
        for score, range_of_grades in COURSE_GRADING_STANDARD.items():
            if average_grade in range_of_grades:
                return score

    def _verify_course(self, course):
        """
        Verify a course.

        params:
             - course

        This function checks whether course provided is a valid course
        object.
        """
        if not isinstance(course, Course):
            raise InvalidCourseException("Please provide valid Course")

    def _verify_student_enrollment(self, student, course):
        """
        Verify student enrollment.

        params:
            - student
            - course

        This function checks if  student is enrolled into the specified
        course.
        """
        if course not in student.enrolled_courses:
            raise UnEnrolledCourseException(
                "Student not enrolled into the specified course"
            )

    def _verify_quiz(self, quiz):
        """
        Verify a quiz.

        params:
             - quiz

        This function checks whether quizprovided is a valid quiz
        object.
        """
        if not isinstance(quiz, Quiz):
            raise InvalidQuizException("Please provide valid Quiz")

    def _verify_quiz_marking(self, quiz):
        """
        Verify that a quiz is marked.

        params:
            - quiz

        This function checks if the quiz is marked by checking if the
        marked attribute is False.
        """
        if not quiz.marked:
            raise UnmarkedQuizException("Please mark this quiz first")

    def _verify_quiz_submission(self, quiz):
        """
        Verify that a quiz is submitted.

        params:
            - quiz

        This function checks if the quiz is submitted by checking if the
        submitted attribute is False.
        """
        if not quiz.submitted:
            raise UnsubmittedQuizException("This quiz has not been submitted")

    def _verify_student(self, student):
        """
        Verify a student.

        params:
             - student

        This function checks whether student provided is a valid student
        object.
        """
        if not isinstance(student, Student):
            raise InvalidStudentException("Please provide valid Student")
