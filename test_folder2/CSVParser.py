import csv


#PATH = r"C:\Personal\csv_file.csv"
PATH = r'C:\FPGA_test_logs\UFSPowerLoggerMeasurement_log.csv'
input_string = 'Raw'
column_name = 'Measurement Type'


def SearchStringInCoulmnOfCSV(csv_file_path, column_name, string_name):
    infile = open(csv_file_path, 'r')
    reader = csv.reader(infile)
    item_found = 0
    item_index
    for row in reader:
        if item_found == 1:
            break
        for row_index in reader:
            if column_name in reader:

                print(row_index)
                column_index = row.index(item)
                print(column_index)
                print("Column "+ item + " present")
                item_found = 1
                print(row_index)
                FindStringInSelectedColumn(csv_file_path, string_name, row_index, column_index,reader)
                break
    if item_found != 1:
        print("measurement type not found")



def FindStringInSelectedColumn(csv_file_path, input_string, StartingRowNumber, column_index,reader):
    output = []
    count = 0
    #with open('csv_file.csv', 'r') as infile:


    for index,row in enumerate(reader):
        print (index)
        print (StartingRowNumber)
        if index >= StartingRowNumber:
            output.append(row[column_index])

    print(output)
    for item in output:
        if item == input_string:
            print("item found")
            return True
    print("item not found")
    return False


if __name__ == "__main__":
    SearchStringInCoulmnOfCSV(PATH, column_name, input_string)


