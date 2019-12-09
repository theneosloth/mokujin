import csv, json

input_file= "leroy.csv"
output_file = "../../json/leroy.json"

movelist = []

with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')

    for row in csv_reader:
        move = {}
        move['Command'] = row[0]
        move['Hit level'] = row[1]
        move['Damage'] = row[2]
        move['Start up frame'] = row[3]
        move['Block frame'] = row[4]
        move['Hit frame'] = row[5]
        move['Counter hit frame'] = row[6]
        move['Notes'] = row[7]
        move['Gif'] = ""

        movelist.append(move)

with open(output_file, 'w') as c:
    json.dump(movelist, c, sort_keys=True, indent=4)