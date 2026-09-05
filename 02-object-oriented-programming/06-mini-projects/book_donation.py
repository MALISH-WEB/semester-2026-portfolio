# COMMUNITY LIBRARY BOOK DONATION MANAGER


# LIST OF TUPLES
# Each tuple represents:
# (donor_name, genre, number_of_books)


donations = [
    ("Alice", "Fiction", 3),
    ("Brian", "Technology", 6),
    ("Carol", "History", 2),
    ("Alice", "Technology", 3),
    ("Daniel", "Fiction", 7),
    ("Grace", "Science", 5)
]



# FUNCTION

def generate_donation_report(donations):

    # Dictionary for total books donated by each donor.
    donor_totals = {}

    # Dictionary for total books received in each genre.
    genre_totals = {}



    # FOR LOOP + TUPLE UNPACKING
   

    for donor, genre, number_of_books in donations:


        # AGGREGATION
       
        if donor not in donor_totals:
            donor_totals[donor] = 0

        donor_totals[donor] += number_of_books



        # AGGREGATION BY GENRE

        if genre not in genre_totals:
            genre_totals[genre] = 0

        genre_totals[genre] += number_of_books


    # TOTAL NUMBER OF BOOKS

    overall_books = sum(donor_totals.values())



    # GOLD DONORS
   

    gold_donors = {}

    for donor, total in donor_totals.items():

        if total >= 5:
            gold_donors[donor] = total


    # MOST POPULAR GENRE
    
    most_popular_genre = max(
        genre_totals,
        key=genre_totals.get
    )



    # SORTING / RANKING
   
    top_donors = sorted(
        donor_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )


    # REPORT
   

    print("=" * 60)
    print("          COMMUNITY LIBRARY DONATION REPORT")
    print("=" * 60)


    print("\n1. TOTAL BOOKS BY DONOR")
    print("-" * 60)

    for donor, total in donor_totals.items():
        print(f"{donor}: {total} books")


    print("\n2. TOTAL BOOKS BY GENRE")
    print("-" * 60)

    for genre, total in genre_totals.items():
        print(f"{genre}: {total} books")


    print("\n3. GOLD DONORS")
    print("-" * 60)

    for donor, total in gold_donors.items():
        print(f"{donor}: {total} books")


    print("\n4. OVERALL BOOKS DONATED")
    print("-" * 60)

    print(f"Total: {overall_books} books")


    print("\n5. MOST POPULAR GENRE")
    print("-" * 60)

    print(
        f"{most_popular_genre}: "
        f"{genre_totals[most_popular_genre]} books"
    )


    print("\n6. TOP 3 DONORS")
    print("-" * 60)

    for position, (donor, total) in enumerate(top_donors[:3], start=1):
        print(f"{position}. {donor} - {total} books")


    print("=" * 60)


# FUNCTION CALL
generate_donation_report(donations)