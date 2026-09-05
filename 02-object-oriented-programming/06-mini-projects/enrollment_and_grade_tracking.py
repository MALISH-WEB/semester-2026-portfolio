# ============================================================
# QUESTION 5
# UNIVERSITY COURSE ENROLLMENT AND GRADE TRACKING SYSTEM
# ============================================================


# ------------------------------------------------------------
# CONCEPT: NESTED DATA STRUCTURES
# ------------------------------------------------------------
#
# students is a LIST.
#
# Each item in the list is a DICTIONARY.
#
# Each student dictionary contains another DICTIONARY called
# "courses".
#
# Each course contains a LIST of marks.
#
# Structure:
#
# LIST
#   ↓
# DICTIONARY
#   ↓
# courses DICTIONARY
#   ↓
# course
#   ↓
# LIST OF MARKS
#
# Example:
#
# students
#   └── Amos
#        └── courses
#             ├── Math → [75, 80, 78]
#             └── English → [85, 88, 90]
# ------------------------------------------------------------


students = [
    {
        "name": "Amos",
        "courses": {
            "Math": [75, 80, 78],
            "English": [85, 88, 90]
        }
    },

    {
        "name": "Betty",
        "courses": {
            "Math": [60, 58, 62],
            "English": [92, 94, 89]
        }
    },

    {
        "name": "Charles",
        "courses": {
            "Math": [85, 88, 90],
            "Science": [80, 82, 85]
        }
    },

    {
        "name": "Diana",
        "courses": {
            "Math": [45, 48, 50],
            "English": [70, 72, 68]
        }
    }
]


# ============================================================
# FUNCTION 1: CALCULATE AVERAGE
# ============================================================

def calculate_average(marks):

    # sum() adds all marks.
    # len() tells us how many marks exist.

    return sum(marks) / len(marks)


# ============================================================
# FUNCTION 2: ASSIGN GRADE
# ============================================================

def assign_grade(average):

    # --------------------------------------------------------
    # CONDITIONS ARE CHECKED FROM HIGHEST TO LOWEST.
    # --------------------------------------------------------

    if average >= 85:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    else:
        return "F"


# ============================================================
# FUNCTION 3: DETERMINE STUDENT STATUS
# ============================================================

def determine_status(grades):

    # --------------------------------------------------------
    # any() checks whether at least one item satisfies a
    # condition.
    #
    # If a student has at least one F:
    # CRITICAL
    # --------------------------------------------------------

    if "F" in grades:
        return "Critical"


    # --------------------------------------------------------
    # If there is no F but there is at least one C:
    # AT-RISK
    # --------------------------------------------------------

    elif "C" in grades:
        return "At-Risk"


    # --------------------------------------------------------
    # If all grades are A or B:
    # GOOD STANDING
    # --------------------------------------------------------

    else:
        return "Good Standing"


# ============================================================
# FUNCTION 4: ANALYSE STUDENTS
# ============================================================

def analyze_students(students):

    student_results = []


    # --------------------------------------------------------
    # OUTER LOOP
    # --------------------------------------------------------
    # Processes each student.
    # --------------------------------------------------------

    for student in students:

        name = student["name"]

        courses = student["courses"]

        course_results = {}

        grades = []

        improvement_courses = []


        # ----------------------------------------------------
        # NESTED LOOP
        # ----------------------------------------------------
        # Processes every course belonging to this student.
        # ----------------------------------------------------

        for course, marks in courses.items():

            # Calculate course average.
            average = calculate_average(marks)

            # Convert average into letter grade.
            grade = assign_grade(average)

            # Store the grade so we can later determine status.
            grades.append(grade)


            # ------------------------------------------------
            # SEARCH / FILTERING
            # ------------------------------------------------
            # Courses below B require improvement.
            # According to the grading scale, C and F are
            # below B.
            # ------------------------------------------------

            if grade in ["C", "F"]:
                improvement_courses.append(course)


            # Store course information.
            course_results[course] = {
                "marks": marks,
                "average": average,
                "grade": grade
            }


        # ----------------------------------------------------
        # DETERMINE STATUS
        # ----------------------------------------------------

        status = determine_status(grades)


        # ----------------------------------------------------
        # OVERALL AVERAGE
        # ----------------------------------------------------
        # We calculate the average of the course averages.
        # ----------------------------------------------------

        course_averages = []

        for course, result in course_results.items():

            course_averages.append(
                result["average"]
            )

        overall_average = calculate_average(course_averages)


        # ----------------------------------------------------
        # TUTORING RECOMMENDATION
        # ----------------------------------------------------

        if status in ["Critical", "At-Risk"]:
            tutoring = "Recommended"

        else:
            tutoring = "Not required"


        # Store the complete student result.
        student_results.append({
            "name": name,
            "courses": course_results,
            "grades": grades,
            "status": status,
            "overall_average": overall_average,
            "improvement_courses": improvement_courses,
            "tutoring": tutoring
        })


    return student_results


# ============================================================
# FUNCTION 5: COURSE STATISTICS
# ============================================================

def calculate_course_statistics(student_results):

    # --------------------------------------------------------
    # Dictionary where each course will store statistics.
    # --------------------------------------------------------

    course_data = {}


    # --------------------------------------------------------
    # NESTED LOOPS
    # --------------------------------------------------------

    for student in student_results:

        for course, result in student["courses"].items():

            # Create the course if it doesn't exist.
            if course not in course_data:

                course_data[course] = {
                    "total_marks": 0,
                    "students": 0,
                    "passing_students": 0
                }


            # ------------------------------------------------
            # ACCUMULATE COURSE AVERAGES
            # ------------------------------------------------

            course_data[course]["total_marks"] += result["average"]

            course_data[course]["students"] += 1


            # ------------------------------------------------
            # PASSING STUDENT
            # ------------------------------------------------
            # Passing means not receiving F.
            # ------------------------------------------------

            if result["grade"] != "F":

                course_data[course]["passing_students"] += 1


    # --------------------------------------------------------
    # CALCULATE FINAL COURSE STATISTICS
    # --------------------------------------------------------

    for course, data in course_data.items():

        data["overall_average"] = (
            data["total_marks"] / data["students"]
        )


    return course_data


# ============================================================
# FUNCTION 6: GENERATE PRIORITY LIST
# ============================================================

def generate_priority_list(student_results):

    # --------------------------------------------------------
    # Define priority values.
    #
    # Lower number = higher priority.
    # --------------------------------------------------------

    priority_order = {
        "Critical": 1,
        "At-Risk": 2,
        "Good Standing": 3
    }


    # --------------------------------------------------------
    # SORTING
    # --------------------------------------------------------
    #
    # First sort by status priority.
    #
    # Then sort by overall average in descending order within
    # the same status.
    # --------------------------------------------------------

    priority_list = sorted(
        student_results,
        key=lambda student: (
            priority_order[student["status"]],
            -student["overall_average"]
        )
    )


    return priority_list


# ============================================================
# FUNCTION 7: GENERATE REPORT
# ============================================================

def generate_report(student_results, course_statistics):

    print("=" * 70)
    print("       UNIVERSITY COURSE PERFORMANCE REPORT")
    print("=" * 70)


    # --------------------------------------------------------
    # PART A: INDIVIDUAL STUDENT PERFORMANCE
    # --------------------------------------------------------

    print("\n1. INDIVIDUAL STUDENT PERFORMANCE")
    print("-" * 70)


    for student in student_results:

        print(f"\nStudent: {student['name']}")

        print(f"Overall Average: {student['overall_average']:.2f}")

        print(f"Status: {student['status']}")

        print(f"Tutoring: {student['tutoring']}")


        print("Courses:")

        for course, result in student["courses"].items():

            print(
                f"  {course}: "
                f"Average = {result['average']:.2f}, "
                f"Grade = {result['grade']}"
            )


        # ----------------------------------------------------
        # IMPROVEMENT COURSES
        # ----------------------------------------------------

        if student["improvement_courses"]:

            print(
                "Requires improvement in: "
                + ", ".join(student["improvement_courses"])
            )

        else:

            print("No course requires improvement.")


    # --------------------------------------------------------
    # PART B: COURSE STATISTICS
    # --------------------------------------------------------

    print("\n2. COURSE STATISTICS")
    print("-" * 70)


    for course, data in course_statistics.items():

        print(f"\nCourse: {course}")

        print(
            f"Overall Average: "
            f"{data['overall_average']:.2f}"
        )

        print(
            f"Students Enrolled: "
            f"{data['students']}"
        )

        print(
            f"Students Passing: "
            f"{data['passing_students']}"
        )


    # --------------------------------------------------------
    # FIND COURSE WITH LOWEST AVERAGE
    # --------------------------------------------------------

    lowest_course = min(
        course_statistics,
        key=lambda course:
        course_statistics[course]["overall_average"]
    )


    print("\n3. COURSE REQUIRING GREATEST ACADEMIC ATTENTION")
    print("-" * 70)

    print(
        f"{lowest_course}: "
        f"{course_statistics[lowest_course]['overall_average']:.2f}"
    )


    # --------------------------------------------------------
    # PART C: INTERVENTION PRIORITY
    # --------------------------------------------------------

    priority_list = generate_priority_list(student_results)


    print("\n4. INTERVENTION PRIORITY LIST")
    print("-" * 70)


    for position, student in enumerate(priority_list, start=1):

        print(
            f"{position}. "
            f"{student['name']} | "
            f"{student['status']} | "
            f"Average: {student['overall_average']:.2f}"
        )


    print("=" * 70)


# ============================================================
# PROGRAM EXECUTION
# ============================================================

# Step 1:
# Analyse every student.

student_results = analyze_students(students)


# Step 2:
# Calculate statistics for each course.

course_statistics = calculate_course_statistics(
    student_results
)


# Step 3:
# Generate the complete report.

generate_report(
    student_results,
    course_statistics
)