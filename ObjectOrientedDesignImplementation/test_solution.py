from unittest import TestCase

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


from solution import (
    Course,
    Question,
    Student,
    Teacher
)


class TestSolution(TestCase):

    def setUp(self):
        self.test_teacher = Teacher("John", "Doe", "TR25")
        self.test_student = Student("John", "Snow", "HB256")
        self.test_student_two = Student("Karl", "Drago", "HB250")

        self.test_question_one = Question(
            1,
            choices=["a", "b", "c", "d"]
        )
        self.test_question_two = Question(
            2,
            choices=["i", "ii", "iii"]
        )

        self.test_course_one = Course("Math", "HBZ5", 1, self.test_teacher)
        self.test_course_two = Course("Science", "HBS4", 2, self.test_teacher)
        self.test_course_three = Course("Math", "HBZ5", 2, self.test_teacher)

        self.test_quiz = self.test_teacher.create_quiz(
            quiz_name="Mid-term",
            quiz_code="MT-1",
            course=self.test_course_one,
            questions=[self.test_question_one, self.test_question_two]
        )

        self.test_quiz_two = self.test_teacher.create_quiz(
            quiz_name="Mid-term",
            quiz_code="MT-1",
            course=self.test_course_one,
            questions=[self.test_question_one, self.test_question_two]
        )
        self.test_quiz_three = self.test_teacher.create_quiz(
            quiz_name="Mid-term",
            quiz_code="MT-1",
            course=self.test_course_one,
            questions=[self.test_question_one, self.test_question_two]
        )

        self.test_student.enroll_into_course(self.test_course_one)
        self.test_teacher.assign_quiz(
            self.test_quiz_two,
            self.test_student_two
        )

    def test_teacher_creation(self):
        """Test creation of a teacher."""
        with self.subTest("Teacher creation is successful"):
            self.assertTrue(isinstance(self.test_teacher, Teacher))
            self.assertEqual(self.test_teacher.first_name, "John")
            self.assertEqual(self.test_teacher.last_name, "Doe")
            self.assertEqual(self.test_teacher.teacher_number, "TR25")

        with self.subTest("Teacher creation fails with missing params"):
            self.assertRaises(TypeError, Teacher, "Joe", "Doe")

    def test_student_creation(self):
        """Test creation of a student."""
        with self.subTest("Student creation is successful"):
            self.assertTrue(isinstance(self.test_student, Student))
            self.assertEqual(self.test_student.first_name, "John")
            self.assertEqual(self.test_student.last_name, "Snow")
            self.assertEqual(self.test_student.student_number, "HB256")

        with self.subTest("Student creation fails on missing params"):
            self.assertRaises(TypeError, Student, "John", "Snow")

    def test_course_creation(self):
        """Test creation of a course."""
        with self.subTest("Course creation is successful"):
            self.assertTrue(isinstance(self.test_course_one, Course))
            self.assertEqual(self.test_course_one.course_name, "Math")
            self.assertEqual(self.test_course_one.course_code, "HBZ5")

        with self.subTest("Course creation fails on missing paramaters"):
            self.assertRaises(
                InvalidCourseTeacherException,
                Course,
                "MATH",
                "HBY7",
                2,
                "1234"
            )

    def test_student_enrollment(self):
        """Test if a student can enrol into a course(class)."""
        with self.subTest("Test that a student enrols sucessfully"):
            self.assertEqual(
                self.test_student.enrolled_courses[0].course_name,
                "Math"
            )

        with self.subTest("Test that a enrollment fails with invalid Course"):
            self.assertRaises(
                InvalidCourseException,
                self.test_student.enroll_into_course,
                "1234"
            )

        with self.subTest("Test that enrollment fails if already enrolled"):
            self.assertRaises(
                AlreadyEnrolledException,
                self.test_student.enroll_into_course,
                self.test_course_one
            )

    def test_question_creation(self):
        """Test the creation of a question."""
        with self.subTest("Test question creation is successful"):
            self.assertTrue(isinstance(self.test_question_one, Question))
            self.assertEqual(
                self.test_question_one.choices,
                ["a", "b", "c", "d"]
            )

        with self.subTest("Test creation fails when choices are less than 2"):
            self.assertRaises(MultipleChoicesException, Question, 5)

    def test_quiz_creation(self):
        """Test that a teacher can create a quiz."""
        with self.subTest("Test quiz is created successfully"):
            self.assertEqual(self.test_quiz.quiz_name, "Mid-term")

        with self.subTest("Test quiz creation fails on missing paramater"):
            self.assertRaises(
                TypeError,
                self.test_teacher.create_quiz,
                "MT-1",
                "course",
            )

        with self.subTest("Test quiz creation is course is invalid"):
            self.assertRaises(
                InvalidCourseException,
                self.test_teacher.create_quiz,
                "Mid-term",
                "MT-1",
                "Course",
                [self.test_question_one, self.test_question_two]
            )

        with self.subTest("Test quiz fails when less than 2 qns are provided"):
            self.assertRaises(
                InvalidNumberOfQuestionsException,
                self.test_teacher.create_quiz,
                "Mid-term",
                "MT-1",
                self.test_course_one,
                [self.test_question_one]
            )

        with self.subTest("Test quiz fails if an invalid qn is provided"):
            self.assertRaises(
                InvalidQuestionException,
                self.test_teacher.create_quiz,
                "Mid-term",
                "MT-1",
                self.test_course_one,
                ["question1", "question2", "question3"]
            )

    def test_assigning_quiz(self):
        """Test that a student can be assigned a quiz by a teacher."""
        with self.subTest("Test Assigning a quiz fails with invalid Quiz"):
            self.assertRaises(
                InvalidQuizException,
                self.test_teacher.assign_quiz,
                "Quiz",
                self.test_student
            )

        with self.subTest("Test Assigning a quiz fails with invalid Student"):
            self.assertRaises(
                InvalidStudentException,
                self.test_teacher.assign_quiz,
                self.test_quiz,
                "Student"
            )

        with self.subTest("Test assigning is successful"):
            self.test_teacher.assign_quiz(
                self.test_quiz,
                self.test_student
            )
            self.assertEqual(
                self.test_quiz.student.first_name,
                self.test_student.first_name
            )
            self.assertEqual(
                self.test_quiz.student.last_name,
                self.test_student.last_name
            )

    def test_answer_quiz(self):
        """Test that a stdudent can answer a quiz."""
        with self.subTest("Test answering fails when quiz is invalid"):
            self.assertRaises(
                InvalidQuizException,
                self.test_student.answer_quiz,
                "Quiz",
                [{1: "b"}, {2: "ii"}]
            )

        with self.subTest("Test answering fails when quiz is unassigned"):
            self.assertRaises(
                UnassignedQuizException,
                self.test_student.answer_quiz,
                self.test_quiz_three,
                [{1: "b"}, {2: "ii"}]
            )

        with self.subTest(
            "Test answering fails when quiz is assigned to another student"
        ):
            self.assertRaises(
                InvalidVerificationException,
                self.test_student.answer_quiz,
                self.test_quiz_two,
                [{1: "b"}, {2: "ii"}]
            )

        with self.subTest(
            "Test answering fails when answer is not amongst the choices"
        ):
            self.test_teacher.assign_quiz(
                self.test_quiz,
                self.test_student
            )
            self.assertRaises(
                InvalidChoiceException,
                self.test_student.answer_quiz,
                self.test_quiz,
                [{1: "II"}, {2: "x"}]
            )
            self.assertEqual(self.test_question_one.answer, None)
            self.assertEqual(self.test_question_two.answer, None)

        with self.subTest("Test that answering is successful"):
            self.test_student.answer_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "ii"}]
            )

            self.assertEqual(self.test_question_one.answer, "b")
            self.assertEqual(self.test_question_two.answer, "ii")

    def test_submit_quiz(self):
        """Test that a student can submit a quiz."""
        with self.subTest("Test quiz submission fails if quiz is invalid"):
            self.assertRaises(
                InvalidQuizException,
                self.test_student.submit_quiz,
                "Quiz"
            )

        with self.subTest(
            "Test quiz submission fails if the quiz is unassigned"
        ):
            self.assertRaises(
                UnassignedQuizException,
                self.test_student.submit_quiz,
                self.test_quiz_three
            )

        with self.subTest(
            "Test quiz submission fails if quiz belongs to another student"
        ):
            self.assertRaises(
                InvalidVerificationException,
                self.test_student.submit_quiz,
                self.test_quiz_two
            )

        with self.subTest("Test quiz submission is successful"):
            self.test_teacher.assign_quiz(
                self.test_quiz,
                self.test_student
            )
            self.test_student.submit_quiz(self.test_quiz)
            self.assertEqual(
                self.test_quiz.submitted,
                True
            )

    def test_mark_quiz(self):
        """Test that a teacher can mark a quiz."""
        with self.subTest("Test marking fails on invalid quiz"):
            self.assertRaises(
                InvalidQuizException,
                self.test_teacher.mark_quiz,
                "Quiz",
                [{1: "b"}, {2: "ii"}]
            )

        with self.subTest("Test marking fails if the quiz is not submitted"):
            self.assertRaises(
                UnsubmittedQuizException,
                self.test_teacher.mark_quiz,
                self.test_quiz,
                [{1: "b"}, {2: "ii"}]
            )

        with self.subTest("Test that quiz can be marked"):
            self.test_teacher.assign_quiz(
                self.test_quiz,
                self.test_student
            )
            self.test_student.answer_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "ii"}]
            )
            self.test_student.submit_quiz(self.test_quiz)
            self.test_teacher.mark_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "iii"}]
            )
            self.assertEqual(self.test_quiz.questions[0].answer_result, True)
            self.assertEqual(self.test_quiz.questions[1].answer_result, False)
            self.assertEqual(self.test_quiz.marked, True)

    def test_grade_quiz(self):
        """Test that a teacher can grade a quiz."""
        with self.subTest("Test grading fails on invalid quiz"):
            self.assertRaises(
                InvalidQuizException,
                self.test_teacher.grade_quiz,
                "Quiz",
            )

        with self.subTest("Test grading fails if quiz is unmarked"):
            self.assertRaises(
                UnmarkedQuizException,
                self.test_teacher.grade_quiz,
                self.test_quiz
            )

        with self.subTest("Test grading quiz is successful"):
            self.test_teacher.assign_quiz(
                self.test_quiz,
                self.test_student
            )
            self.test_student.answer_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "ii"}]
            )
            self.test_student.submit_quiz(self.test_quiz)
            self.test_teacher.mark_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "iii"}]
            )
            self.test_teacher.grade_quiz(self.test_quiz)
            self. assertEqual(self.test_quiz.grade, 50)
            self. assertEqual(self.test_quiz.teacher_graded, True)

    def test_calculate_total_grade(self):
        """
        Test that a teacher can calculate the
        total grade for student for a course in the semester.
        """
        with self.subTest("Test calculation fails with invalid student"):
            self.assertRaises(
                InvalidStudentException,
                self.test_teacher.calculate_total_grade,
                "Student",
                self.test_course_one
            )

        with self.subTest("Test calculation fails with invalid course"):
            self.assertRaises(
                InvalidCourseException,
                self.test_teacher.calculate_total_grade,
                self.test_student,
                "Course"
            )

        with self.subTest("Test calculation fails with course no enrolled in"):
            self.assertRaises(
                UnEnrolledCourseException,
                self.test_teacher.calculate_total_grade,
                self.test_student,
                self.test_course_two
            )

        with self.subTest("Test calculation fails if semester is different"):
            self.assertRaises(
                UnEnrolledCourseException,
                self.test_teacher.calculate_total_grade,
                self.test_student,
                self.test_course_three
            )

        with self.subTest("Test  grade calculation is successful"):
            self.test_teacher.assign_quiz(
                self.test_quiz,
                self.test_student
            )
            self.test_student.answer_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "ii"}]
            )
            self.test_student.submit_quiz(self.test_quiz)
            self.test_teacher.mark_quiz(
                self.test_quiz,
                [{1: "b"}, {2: "iii"}]
            )
            self.test_teacher.grade_quiz(self.test_quiz)
            self.test_teacher.calculate_total_grade(
                self.test_student,
                self.test_course_one
            )
            self.assertEqual(self.test_course_one.course_grade, "D")
