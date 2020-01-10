""" Module for custom exceptions."""


class AlreadyEnrolledException(Exception):
    """Error for when a student is already enrolled into a course."""
    pass


class InvalidChoiceException(Exception):
    """Error if the choice provided is an invalid value."""
    pass


class InvalidCourseException(Exception):
    """Error if the course provided is an invalid value."""
    pass


class InvalidCourseTeacherException(Exception):
    """Error if the Teacher provided is an invalid value."""
    pass


class InvalidQuestionException(Exception):
    """Error if the Question provided is an invalid value."""
    pass


class InvalidQuizException(Exception):
    """Error if the Quiz provided is an invalid value."""
    pass


class InvalidNumberOfQuestionsException(Exception):
    """Error if the Questions provided are less than 2."""
    pass


class InvalidVerificationException(Exception):
    """Error if the details provided don't match."""
    pass


class InvalidStudentException(Exception):
    """Error if the Student provided is an invalid value."""
    pass


class MultipleChoicesException(Exception):
    """Error when the choices provided are less than 2."""
    pass


class UnassignedQuizException(Exception):
    """Error when the Quiz provided hasnt been assigned."""
    pass


class UnEnrolledCourseException(Exception):
    """Error when the Course provided hasnt been enrolled into."""
    pass


class UnmarkedQuizException(Exception):
    """Error when the Quiz provided hasnt been marked."""
    pass


class UnsubmittedQuizException(Exception):
    """Error when the Quiz provided hasn't been submitted."""
    pass
