import os
import pdfplumber



ASIN_list = []
Amount_list = []



def find(file_path):
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table[2:]:   #Start iterating from the third row (index 2)
                    if row:
                        first_column = row[0]
                        last_column = row[-1]
                        ASIN_list.append(first_column)
                        Amount_list.append(last_column)


def getASIN():
    return ASIN_list


def getQuantity():
    return Amount_list

