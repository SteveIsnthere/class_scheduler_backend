import faker
from database.db import db
import asyncio

from database.db import to_dict
from database.methods.class_ import post_class, get_one_week_of_classes_of_a_member, get_one_week_of_classes, \
    delete_class
from database.methods.course import post_course, get_teachers_by_course, get_all_courses, get_students_by_course
from database.methods.member import get_all_members, get_member, delete_member, post_member, replace_member
from database.methods.plan import post_plan, get_plans_by_member
from database.methods.relation import post_relation, get_all_relations, get_relations_by_member, delete_relation
from models.course import Course
from models.time_period import TimePeriod
from models.member import Member
from models.class_plan import ClassPlan
from models.class_instance import ClassInstance
from models.relation import Relation

fake = faker.Faker()

school_courses = [
    "Math",
    "English",
    "Science",
    "History",
    "Art",
    "Music",
    "PE",
    "Computer Science",
    "Foreign Language",
    "Business",
    "Home Economics",
    "Drama",
    "Health",
    "Elective",
]


def dummy_courses():
    # return a Course object with random values with duration of 1 or 1.5 or 2 or 3 hours and saved in hours
    # with price from 40 to 200
    courses = []
    for i in range(len(school_courses)):
        course = Course(
            name=school_courses[i],
            defaultDuration=fake.random_element(elements=[1, 1.5, 2, 3]),
            defaultPrice=fake.random_int(min=40, max=200),
        )
        courses.append(course)
    return courses


def dummy_member():
    # return a Member object with random values
    # courses_taken is picked randomly from courses
    name = fake.name()
    phone = fake.phone_number()
    # nickname is a mix of name and last few digits of phone number
    nickname = name.split(" ")[0] + phone[-4:]
    return Member(
        name=name,
        nickname=nickname,
        email=fake.email(),
        phone=phone,
        password=fake.password(),
        isTeacher=fake.boolean(),
        about=fake.text(),
        noteToAdmin=fake.text(),
        courses=[],
        plans=[],
        unableTimes=[dummy_time_period() for _ in range(fake.random_int(0, 3))],
        preferredTimes=[dummy_time_period() for _ in range(fake.random_int(0, 3))],
    )


def dummy_class_plan(courses, relation, weeks):
    days = str(weeks * 7)
    # return a ClassPlan object with random values
    course_name = relation.courseName
    course = [course for course in courses if course.name == course_name][0]
    # declare a time in next 14 days and between 11am and 6pm
    start_time = fake.date_time_between(start_date="-" + days + "d", end_date="+" + days + "d", tzinfo=None)
    start_time = start_time.replace(hour=fake.random_int(11, 18), minute=0, second=0, microsecond=0)
    plan = ClassPlan(
        weekDay=fake.random_int(1, 7),
        info=relation,
        startTime=start_time,
        duration=course.defaultDuration,
    )

    return plan


def dummy_class_instance(class_plan):
    # return a ClassInstance object with random values
    return ClassInstance(
        startTime=class_plan.startTime,
        duration=class_plan.duration,
        finished=fake.boolean(),
        rating=fake.random_int(1, 5),
        comment=fake.text(),
        isOnline=fake.boolean(),
        info=class_plan.info,
    )


def dummy_relations(courses, members, amount):
    relations = []
    for member in members:
        for i in range(fake.random_int(1, amount)):
            # for each member, pick 1-3 courses
            # return a Relation object with random values
            course = courses[fake.random_int(0, len(courses) - 1)]
            # teacher is a member whose attribute isTeacher = True
            teachers = [member for member in members if member.isTeacher]
            teacher = teachers[fake.random_int(0, len(teachers) - 1)]

            # student is a member whose attribute isTeacher = False
            students = [member for member in members if not member.isTeacher]
            student = students[fake.random_int(0, len(students) - 1)]

            if member.isTeacher:
                teacher = member
            else:
                student = member

            relation = Relation(
                courseName=course.name,
                price=course.defaultPrice,
                salary=int(course.defaultPrice / 2),
                teacher=teacher.nickname,
                student=student.nickname,
                classPerWeek=fake.random_int(1, 4),
                duration=course.defaultDuration,
            )

            unique = True
            for r in relations:
                if r.courseName == relation.courseName and r.teacher == relation.teacher and r.student == \
                        relation.student:
                    unique = False
                    break

            if unique:
                # add relation to teacher and student
                relations.append(relation)

    return relations


def dummy_time_period():
    # return a UnableTime object with random values
    # startTime + duration < midnight
    return TimePeriod(
        startTime=fake.date_time(),
        duration=fake.random_int(0, 10),
        weekDay=fake.random_int(1, 7),
    )


async def generate_dummy_data(database):
    # return a list of dummy data
    weeks_of_data_to_generate = 3
    courses = dummy_courses()
    members = [dummy_member() for _ in range(30)]
    # find a member whose attribute isTeacher = True and change its nickname to "test"
    for member in members:
        if member.isTeacher:
            member.nickname = "Steve1984"
            member.password = "test"
            member.name = "Steve Wang"
            break
    relations = dummy_relations(courses, members, 2)
    # for each relation, create 1-5 class plans
    plans = [dummy_class_plan(courses, relation, weeks_of_data_to_generate) for relation in relations for _ in
             range(fake.random_int(2 * weeks_of_data_to_generate, 8 * weeks_of_data_to_generate))]
    # for each plan, create 0-1 class instance
    classes = [dummy_class_instance(plan) for plan in plans for _ in range(fake.random_int(0, 1))]

    # insert dummy data into database after removing all data
    database.delete_many("courses", {})
    database.delete_many("members", {})
    database.delete_many("relations", {})
    database.delete_many("plans", {})
    database.delete_many("classes", {})

    for course in courses:
        await post_course(to_dict(course))
    for member in members:
        await post_member(to_dict(member))
    for relation in relations:
        await post_relation(to_dict(relation))
    for plan in plans:
        await post_plan(to_dict(plan))
    for c in classes:
        await post_class(to_dict(c))

    # print out the number of each type of data
    print(f"courses: {len(courses)}")
    print(f"members: {len(members)}")
    print(f"relations: {len(relations)}")
    print(f"plans: {len(plans)}")
    print(f"classes: {len(classes)}")

    r = database.find_one("classes", {})

    # members = await get_all_members()
    # relations = await get_all_relations()
    # courses = await get_all_courses()
    # classes_this_week = await get_one_week_of_classes(0)
    #
    # d = await get_plans_by_member(members[0]["nickname"])
    #
    # await delete_relation(str(relations[0]["_id"]))
    # await delete_class(str(classes_this_week[0]["_id"]))
    # await delete_member(members[0]["nickname"])


asyncio.run(generate_dummy_data(db))
