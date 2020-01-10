
Feature: There are Teachers
    Scenario: Teacher creation is successful
    Given a Teacher
    When I assign the first name, last name and teacher number
    Then a valid Teacher should be created

Feature: There are Students
    Scenario: Student creation is successful
    Given a Student
    When I assign the first name, last name and student number
    Then a valid Student should be created

Feature: There are Classes(Courses)
    Scenario: Class(Course) creation is successful
    Given a Class(Course)
    When I assign the course name, course code, semester and course teacher
    And the course teacher is a valid Teacher
    Then a valid Course should be created

Feature: Students are in classes that teachers teach
    Scenario: Student enrolls into a class successfully
    Given a Class(Course)
    And and this class is valid 
    And taught by a Teacher
    And the student is not already enrolled
    Then a Student should be able to enroll into this class

Feature: Questions for quizzes that teacher create (each question is multiple choice)
    Scenario: Question creation is successful
    Given a Question
    When I assign a question number and choices
    And these choices are more than one
    Then a valid Question should be created

Feature: Teachers can create multiple quizzes with many questions 
    Scenario: Teacher creates a quiz successfully
    Given a Teacher
    And a Quiz
    When this teacher assigns a quiz name, a quiz code, a course and questions
    And this course is valid
    And these questions are valid
    Then a valid Quiz should be created

Feature: Teachers can assign quizzes to students
    Scenario: Teacher successfully assigns a quiz to a student
    Given a Teacher
    And a valid Student
    And a valid Quiz
    Then this Teacher can assign this quiz to this student

Feature: Students solve/answer questions to complete the quiz.
    Scenario: A student can answer a quiz successfully
    Given a Student
    And a valid Quiz
    And this quiz is assigned to this Student
    Then this student should be able to assign valid answers to the quiz questions

Feature: Students can submit quizzes (these can be partially answered)
    Scenario: A student can submit a quiz successfully
    Given a Student
    And a valid Quiz
    And this quiz has been assigned to this student
    And this quiz has been answered by this student whether fully or partially answered
    Then this Student should be able to submit this quiz

Feature: Teachers can mark quizzes
    Scenario: A teacher can mark a quiz successfully
    Given a Teacher 
    And a valid Quiz
    And this Quiz has been submitted
    Then the teacher should be able to mark the questions in the quiz correct or incorrect

Feature: Teachers can grade quizzes
    Scenario: A teacher can grade a quiz successfully
    Given a Teacher
    And a valid quiz
    And this quiz has been marked
    Then a teacher should be able to grade this quiz by getting the percentage of correct answers
    And assigning this percentageof correct answers as the grade of this quiz

Feature: Teachers can calculate each students total grade for their classes
    Scenario: A teacher can calculate the total grade for the semester for a student in their class
    Given a Teacher
    And a valid student
    And a this student is enrolled into this teacher's valid class(course)
    Then the teacher should be able to get all the graded quizzes for that semester
    And calculate the average percentage of the whole semester as average grade
    Then  the teacher should match this average grade to a value from the course grading standard
    And  this value from the course grading standard should then be taken as the course grade for the semester.

    




