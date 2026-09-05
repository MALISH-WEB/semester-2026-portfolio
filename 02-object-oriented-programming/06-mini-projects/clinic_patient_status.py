# CLINIC PATIENT STATUS CLASSIFICATION SYSTEM

patients = [
    ("Alex", 115, 75),
    ("Brian", 128, 84),
    ("Carol", 145, 95),
    ("Daniel", 165, 105),
    ("Grace", 118, 78)
]



# FUNCTION: CLASSIFY PATIENT

# This function receives systolic and diastolic readings and
# returns one category.


def classify_patient(systolic, diastolic):

   
    # STAGE 2 / URGENT
    # Check the most serious category FIRST.
  

    if systolic >= 160 or diastolic >= 100:
        return "Stage 2 / Urgent"


    
    # STAGE 1
    

    elif systolic >= 140 or diastolic >= 90:
        return "Stage 1"


    
    # ELEVATED
    

    elif systolic >= 120 or diastolic >= 80:
        return "Elevated"



    # NORMAL


    else:
        return "Normal"



# MAIN PROCESSING FUNCTION


def generate_patient_report(patients):

    # Lists are used to store patients belonging to categories.

    normal_patients = []
    at_risk_patients = []
    urgent_patients = []

    # Dictionary stores each patient's classification.
    classifications = {}


    
    # PROCESS EVERY PATIENT
   

    for name, systolic, diastolic in patients:

        category = classify_patient(
            systolic,
            diastolic
        )

        classifications[name] = category


    
        # FILTER PATIENTS INTO COLLECTIONS
        

        if category == "Normal":

            normal_patients.append(name)

        elif category in ["Elevated", "Stage 1"]:

            at_risk_patients.append(name)

        elif category == "Stage 2 / Urgent":

            urgent_patients.append(name)


 
    # CALCULATE AVERAGES
    

    total_systolic = 0
    total_diastolic = 0

    for name, systolic, diastolic in patients:

        total_systolic += systolic
        total_diastolic += diastolic


    average_systolic = total_systolic / len(patients)
    average_diastolic = total_diastolic / len(patients)



    # FOLLOW-UP PATIENTS
    # For this programming exercise, patients who are not
    # Normal are treated as requiring follow-up.


    follow_up_patients = []

    for name, category in classifications.items():

        if category != "Normal":
            follow_up_patients.append(name)


   
    # REPORT
    

    print("=" * 60)
    print("       CLINIC PATIENT STATUS REPORT")
    print("=" * 60)


    print("\n1. PATIENT CLASSIFICATIONS")
    print("-" * 60)

    for name, category in classifications.items():

        print(f"{name}: {category}")


    print("\n2. NORMAL PATIENTS")
    print("-" * 60)

    for name in normal_patients:
        print(name)


    print("\n3. AT-RISK PATIENTS")
    print("-" * 60)

    for name in at_risk_patients:
        print(name)


    print("\n4. URGENT PATIENTS")
    print("-" * 60)

    for name in urgent_patients:
        print(name)


    print("\n5. AVERAGE READINGS")
    print("-" * 60)

    print(f"Average systolic: {average_systolic:.2f}")
    print(f"Average diastolic: {average_diastolic:.2f}")


    print("\n6. ALERTS")
    print("-" * 60)

    if urgent_patients:

        for name in urgent_patients:
            print(f"ALERT: {name} is classified as Stage 2 / Urgent.")

    else:
        print("No urgent patients.")


    print("\n7. FOLLOW-UP PATIENTS")
    print("-" * 60)

    for name in follow_up_patients:
        print(name)


    print("\n8. CATEGORY SUMMARY")
    print("-" * 60)

    print(f"Normal: {len(normal_patients)}")
    print(f"At-Risk: {len(at_risk_patients)}")
    print(f"Urgent: {len(urgent_patients)}")


    print("=" * 60)


# FUNCTION CALL

generate_patient_report(patients)