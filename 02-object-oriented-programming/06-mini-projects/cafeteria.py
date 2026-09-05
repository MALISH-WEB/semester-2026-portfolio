# ============================================================
# QUESTION 1
# SCHOOL CAFETERIA MEAL PLANNING SYSTEM
# ============================================================

# ------------------------------------------------------------
# CONCEPT: LIST
# ------------------------------------------------------------
# A list stores multiple values in one variable.
#
# Here, meal_data is a LIST containing several student records.
#
# ------------------------------------------------------------
# CONCEPT: TUPLE
# ------------------------------------------------------------
# Each record is a TUPLE.
#
# Each tuple contains:
# (student_name, meal_type, daily_price)
#
# Tuples are useful here because each record represents a
# fixed group of related values.
# ------------------------------------------------------------

meal_data = [
    ("John", "Pizza", 2500),
    ("Sarah", "Burger", 2000),
    ("Mike", "Pasta", 2200),
    ("Grace", "Chicken and Rice", 3500),
    ("Peter", "Pizza", 2500)
]


# ------------------------------------------------------------
# CONCEPT: CONSTANTS
# ------------------------------------------------------------
# Instead of writing 5 and 15000 throughout the program,
# we give those rules meaningful names.
#
# SCHOOL_DAYS = number of days in the school week
# HIGH_SPENDING_LIMIT = threshold for unusually high spending
# ------------------------------------------------------------

SCHOOL_DAYS = 5
HIGH_SPENDING_LIMIT = 15000


# ------------------------------------------------------------
# CONCEPT: FUNCTION
# ------------------------------------------------------------
# A function is a reusable block of code designed to perform
# a particular task.
#
# meal_data is a PARAMETER.
#
# We pass the cafeteria data into the function.
# ------------------------------------------------------------

def generate_cafeteria_report(meal_data):

    # --------------------------------------------------------
    # CONCEPT: DICTIONARY
    # --------------------------------------------------------
    # A dictionary stores information as KEY : VALUE pairs.
    #
    # Example:
    # student_expenses["John"] = 12500
    #
    # "John" is the key.
    # 12500 is the value.
    # --------------------------------------------------------

    student_expenses = {}

    # Stores students according to their meal preference.
    # Example:
    # "Pizza" -> ["John", "Peter"]
    meal_students = {}

    # Stores total weekly revenue for each meal.
    meal_revenue = {}

    # Stores how many students selected each meal.
    meal_count = {}


    # --------------------------------------------------------
    # CONCEPT: FOR LOOP
    # --------------------------------------------------------
    # A for loop processes every record in the list.
    #
    # The first record:
    # ("John", "Pizza", 2500)
    #
    # is automatically unpacked into:
    # student_name = "John"
    # meal_type = "Pizza"
    # daily_price = 2500
    #
    # This is called TUPLE UNPACKING.
    # --------------------------------------------------------

    for student_name, meal_type, daily_price in meal_data:

        # ----------------------------------------------------
        # CONCEPT: CALCULATION
        # ----------------------------------------------------
        # Weekly expenditure = daily price × 5 school days.
        # ----------------------------------------------------

        weekly_expense = daily_price * SCHOOL_DAYS

        # Store the student's weekly expense.
        student_expenses[student_name] = weekly_expense


        # ----------------------------------------------------
        # CONCEPT: CONDITIONAL STATEMENT
        # ----------------------------------------------------
        # "if" allows the program to make decisions.
        #
        # If this meal has not appeared before, create an
        # empty list for it.
        # ----------------------------------------------------

        if meal_type not in meal_students:
            meal_students[meal_type] = []

        # Add the student to the appropriate meal group.
        meal_students[meal_type].append(student_name)


        # ----------------------------------------------------
        # CONCEPT: ACCUMULATION
        # ----------------------------------------------------
        # We calculate the weekly revenue for this record.
        # ----------------------------------------------------

        weekly_revenue = daily_price * SCHOOL_DAYS

        # If the meal doesn't exist in the dictionary,
        # start its revenue at zero.
        if meal_type not in meal_revenue:
            meal_revenue[meal_type] = 0

        # Add this student's revenue to the meal's total.
        meal_revenue[meal_type] += weekly_revenue


        # ----------------------------------------------------
        # CONCEPT: COUNTING
        # ----------------------------------------------------
        # Count how many students selected each meal.
        # ----------------------------------------------------

        if meal_type not in meal_count:
            meal_count[meal_type] = 0

        meal_count[meal_type] += 1


    # --------------------------------------------------------
    # CONCEPT: FILTERING
    # --------------------------------------------------------
    # We want students whose weekly expenditure is greater
    # than 15,000 UGX.
    #
    # We examine every student and keep only those who satisfy
    # the condition.
    # --------------------------------------------------------

    high_spenders = {}

    for student_name, expense in student_expenses.items():

        if expense > HIGH_SPENDING_LIMIT:
            high_spenders[student_name] = expense


    # --------------------------------------------------------
    # CONCEPT: SEARCHING / FINDING A MAXIMUM
    # --------------------------------------------------------
    # max() finds the largest value.
    #
    # key=meal_count.get tells Python to compare the dictionary
    # values rather than the dictionary keys.
    #
    # Therefore, we find the meal selected by the most students.
    # --------------------------------------------------------

    most_popular_meal = max(meal_count, key=meal_count.get)


    # --------------------------------------------------------
    # CONCEPT: FORMATTED OUTPUT
    # --------------------------------------------------------

    print("=" * 55)
    print("        SCHOOL CAFETERIA WEEKLY REPORT")
    print("=" * 55)


    print("\n1. STUDENTS BY MEAL PREFERENCE")
    print("-" * 55)

    for meal, students in meal_students.items():
        print(f"{meal}: {', '.join(students)}")


    print("\n2. WEEKLY EXPENDITURE PER STUDENT")
    print("-" * 55)

    for student, expense in student_expenses.items():
        print(f"{student}: {expense:,} UGX")


    print("\n3. STUDENTS SPENDING MORE THAN 15,000 UGX")
    print("-" * 55)

    if high_spenders:

        for student, expense in high_spenders.items():
            print(f"{student}: {expense:,} UGX")

    else:
        print("No students exceeded 15,000 UGX.")


    print("\n4. WEEKLY REVENUE BY MEAL")
    print("-" * 55)

    for meal, revenue in meal_revenue.items():
        print(f"{meal}: {revenue:,} UGX")


    print("\n5. MOST POPULAR MEAL")
    print("-" * 55)

    print(
        f"{most_popular_meal} "
        f"({meal_count[most_popular_meal]} students)"
    )

    print("=" * 55)


# ------------------------------------------------------------
# CONCEPT: FUNCTION CALL
# ------------------------------------------------------------
# This executes the function.
# ------------------------------------------------------------

generate_cafeteria_report(meal_data)


# ------------------------------------------------------------
# EXPECTED IMPORTANT RESULTS
# ------------------------------------------------------------
#
# John   = 12,500 UGX
# Sarah  = 10,000 UGX
# Mike   = 11,000 UGX
# Grace  = 17,500 UGX
# Peter  = 12,500 UGX
#
# High spender:
# Grace = 17,500 UGX
#
# Most popular:
# Pizza = 2 students
#
# Revenue:
# Pizza            = 25,000 UGX
# Burger           = 10,000 UGX
# Pasta            = 11,000 UGX
# Chicken and Rice = 17,500 UGX
# ============================================================