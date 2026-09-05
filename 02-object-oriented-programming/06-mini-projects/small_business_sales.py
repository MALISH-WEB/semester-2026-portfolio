# SMALL BUSINESS SALES PERFORMANCE MONITOR
sales = [
    ("Monday", "Alex", "Samsung", 1200000),
    ("Monday", "Sikina", "Tecno", 850000),
    ("Tuesday", "Alex", "iPhone", 2500000),
    ("Tuesday", "Malish", "Samsung", 1100000),
    ("Wednesday", "Sikina", "Infinix", 900000),
    ("Wednesday", "Alex", "Samsung", 1600000),
    ("Thursday", "Malish", "Tecno", 700000),
    ("Friday", "Sikina", "Samsung", 2300000)
]



# CONSTANT

SLOW_DAY_LIMIT = 2000000



# FUNCTION


def generate_sales_report(sales):

    # Total sales for every salesperson.
    salesperson_totals = {}

    # Total revenue for every phone brand.
    brand_totals = {}

    # Total sales for every day.
    daily_totals = {}



    # LOOP THROUGH ALL SALES

    for day, salesperson, brand, amount in sales:

        # SALESPERSON AGGREGATION
       

        if salesperson not in salesperson_totals:
            salesperson_totals[salesperson] = 0

        salesperson_totals[salesperson] += amount



        # BRAND AGGREGATION

        if brand not in brand_totals:
            brand_totals[brand] = 0

        brand_totals[brand] += amount


        # DAILY AGGREGATION

        if day not in daily_totals:
            daily_totals[day] = 0

        daily_totals[day] += amount



    # FIND THE HIGHEST SALES VALUE

    highest_sales = max(salesperson_totals.values())


   
    # FIND ALL TOP PERFORMERS
    
    top_performers = []

    for salesperson, total in salesperson_totals.items():

        if total == highest_sales:
            top_performers.append(salesperson)


    # BONUS CALCULATION
  
    bonuses = {}

    for salesperson in salesperson_totals:

        if salesperson in top_performers:
            bonuses[salesperson] = 50000
        else:
            bonuses[salesperson] = 20000



    # HIGHEST REVENUE BRAND

    highest_brand = max(
        brand_totals,
        key=brand_totals.get
    )


   
    # SLOW DAYS
    # A slow day is below 2,000,000 UGX.
  

    slow_days = {}

    for day, total in daily_totals.items():

        if total < SLOW_DAY_LIMIT:
            slow_days[day] = total


  
    # REPORT
    
    print("=" * 65)
    print("             WEEKLY SALES PERFORMANCE REPORT")
    print("=" * 65)


    print("\n1. SALES BY SALESPERSON")
    print("-" * 65)

    for salesperson, total in salesperson_totals.items():

        print(
            f"{salesperson}: "
            f"{total:,} UGX"
        )


    print("\n2. TOP PERFORMER(S)")
    print("-" * 65)

    for salesperson in top_performers:

        print(
            f"{salesperson}: "
            f"{salesperson_totals[salesperson]:,} UGX"
        )


    print("\n3. BONUSES")
    print("-" * 65)

    for salesperson, bonus in bonuses.items():

        print(
            f"{salesperson}: "
            f"{bonus:,} UGX"
        )


    print("\n4. REVENUE BY PHONE BRAND")
    print("-" * 65)

    for brand, total in brand_totals.items():

        print(
            f"{brand}: "
            f"{total:,} UGX"
        )


    print("\n5. HIGHEST-REVENUE PHONE BRAND")
    print("-" * 65)

    print(
        f"{highest_brand}: "
        f"{brand_totals[highest_brand]:,} UGX"
    )


    print("\n6. TOTAL SALES BY DAY")
    print("-" * 65)

    for day, total in daily_totals.items():

        print(
            f"{day}: "
            f"{total:,} UGX"
        )


    print("\n7. SLOW BUSINESS DAYS")
    print("-" * 65)

    if slow_days:

        for day, total in slow_days.items():

            print(
                f"{day}: "
                f"{total:,} UGX"
            )

    else:
        print("No slow business days.")


    print("=" * 65)


# FUNCTION CALL

generate_sales_report(sales)