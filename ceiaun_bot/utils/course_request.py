from unidecode import unidecode

from bot import consts, messages
from bot.consts import SUMMER_REQUEST_COURSES
from utils.validators import clean_course_id, clean_course_name, clean_student_id, clean_student_name


def remove_special_characters(text: str) -> str:
    return "".join(e for e in text if e.isalnum())


def process_course_request(text: str) -> list:
    user_text = text.split("+")

    # Request must be 4 part (student name + student id + course name + course id)
    if len(user_text) != 4:
        raise ValueError(messages.REQ_ERROR_LENGTH, "REQ_ERROR_LENGTH")

    # Remove special chars and Convert persian number to english number
    student_name = user_text[0].strip()
    student_id = remove_special_characters(unidecode(user_text[1]))
    course_name = user_text[2].strip()
    course_id = remove_special_characters(unidecode(user_text[3].strip()))

    # Course name replace
    for words in consts.WORD_REPLACE:
        course_name = course_name.replace(*words)

    # Clean
    clean_student_name(student_name)
    clean_student_id(student_id)
    clean_course_name(course_name)
    clean_course_id(course_id)

    return [student_name, student_id, course_name, course_id]


def generate_summer_request_response(course_status: dict[int, bool]) -> str:
    response = """انتخاب کنید.

درس های انتخابی شما:
{courses}"""

    if not any(value for value in course_status.values()):
        return response.format(courses="شما هنوز هیچ درسی انتخاب نکرده اید!")

    courses = [course.name for course in SUMMER_REQUEST_COURSES if course_status[course.id]]

    return response.format(courses="\n".join(courses))


def process_summer_course_request(text: str) -> list:
    user_text = text.split("+")

    # Request must be 2 part (student name + student id)
    if len(user_text) != 2:
        raise ValueError("درخواست را طبق فرمت ارسال کنید", "REQ_ERROR_LENGTH")

    student_name = user_text[0].strip()
    student_id = remove_special_characters(unidecode(user_text[1]))

    # Clean
    clean_student_name(student_name)
    clean_student_id(student_id)

    return [student_name, student_id]
