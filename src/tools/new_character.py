import csv,os
import json
input_file = "Kuni.csv"
character_name = "kunimitsu"
json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..","json"))
output_file = f'{json_folder}/{character_name}.json'

movelist = []

with open(input_file, encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    for row in csv_reader:
        new_move = {}
        new_move['Command'] = row[1]
        '''
        if row[1]:
            aliases = []
            positions= [pos for pos, char in enumerate(row[1]) if char == "\""]

            for x in range(0, len(positions), 2):
                alias = row[1][int(positions[x] +1): int(positions[x+1])]
                aliases.append(alias)

            new_move['Alias'] = aliases'''

        new_move['Hit level'] = row[2].lower()
        new_move['Damage'] = row[3]
        new_move['Start up frame'] = row[4]
        new_move['Block frame'] = row[5]
        new_move['Hit frame'] = row[6]
        new_move['Counter hit frame'] = row[7]
        new_move['Notes'] = row[8]
        gif_data = ""
        if row[0]:
            gif_data = row[0] + ".gif"

        new_move['Gif'] = gif_data
        for entry in new_move:
            if type(new_move[entry]) != list and (new_move[entry] is None or not new_move[entry].strip()):
                new_move[entry] = "-"

        movelist.append(new_move)
    print(movelist)


with open(output_file, 'w') as c:
    json.dump(movelist, c, sort_keys=True, indent=4, ensure_ascii=True)