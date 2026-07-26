bs_months = [
    "Baisakh","Jestha","Ashadh","Shrawan",
    "Bhadra","Ashwin","Kartik","Mangsir",
    "Poush","Magh","Falgun","Chaitra"
]

customers = [
    {"name":"Ramesh Thapa","date":"1985-06-24","cal":"AD","need":"BS","style":"full"},
    {"name":"Sunita Karki","date":"2055-09-10","cal":"BS","need":"AD","style":"iso"},
    {"name":"Bikash Rai","date":"1998-11-30","cal":"AD","need":"BS","style":"nepali"},
    {"name":"Anjali Gurung","date":"2040-01-05","cal":"BS","need":"AD","style":"full"}
]

def convert_date(date_str, from_cal, to_cal):

    year, month, day = date_str.split("-")

    year = int(year)
    month = int(month)
    day = int(day)

    if from_cal == to_cal:
        return date_str

    if from_cal == "AD" and to_cal == "BS":
        year += 56

    elif from_cal == "BS" and to_cal == "AD":
        year -= 56

    if to_cal == "BS":
        month_name = bs_months[month - 1]
        return str(day) + "th " + month_name + ", " + str(year) + " BS"

    else:
        return str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + " AD"


for customer in customers:

    new_date = convert_date(customer["date"], customer["cal"], customer["need"])

    print(customer["name"],
          "| Original:", customer["date"], customer["cal"],
          "| Converted:", new_date)