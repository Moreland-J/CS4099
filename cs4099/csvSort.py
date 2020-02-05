import csv

db = []

def run():
    readDB()
    quickSort(1, (len(db) - 1))
    writeCSV()
    readDB()

def readDB():
    # https://realpython.com/python-csv/
    print()
    with open('database/db.csv') as file:
        reader = csv.reader(file, delimiter = ',')
        count = 0
        for col in reader:
            db.append([])
            if count == 0:
                db[count].append(col[0])
                db[count].append(col[1])
                count += 1
            else:
                db[count].append(col[0])
                db[count].append(col[1])
                print(str(count) + " " + db[count][0] + " " + db[count][1])
                count += 1
    print()
    return

# https://www.geeksforgeeks.org/quick-sort/
def quickSort(low, high):
    if low < high:
        pivot = partition(low, high)
        quickSort(low, pivot - 1)
        quickSort(pivot + 1, high)
    return

# MOVES SMALLER VALUES TO THE LEFT
def partition(low, high):
    pivot = db[high][0]
    i = low - 1

    for j in range(low, high):
        if db[j][0] < pivot:
            i += 1
            db[i][0], db[j][0] = db[j][0], db[i][0]
            db[i][1], db[j][1] = db[j][1], db[i][1]

    db[i + 1][0], db[high][0] = db[high][0], db[i + 1][0]
    db[i + 1][1], db[high][1] = db[high][1], db[i + 1][1]
    return i + 1

def writeCSV():
    file = open('database/db.csv', 'w', newline="")
    with file:
        writer = csv.writer(file)
        writer.writerows(db)
    print("Complete!")

run()