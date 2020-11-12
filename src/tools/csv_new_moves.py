import csv, os.path
import json
input_file = "s4.csv"

movelist = []

with open(input_file, encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        character_name=row[0].lower()
        json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..","json"))
        output_file = f'{json_folder}/{character_name}.json'

        with open(output_file, encoding='utf-8-sig') as original_json_file:
                movelist = json.load(original_json_file)
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

                new_move['Hit level'] = row[2]
                new_move['Damage'] = row[3]
                new_move['Start up frame'] = row[4]
                new_move['Block frame'] = row[5]
                new_move['Hit frame'] = row[6]
                new_move['Counter hit frame'] = row[7]
                new_move['Notes'] = row[8]
                new_move['Gif'] = row[9]
                '''  
                for move in original_json_reader:
                    if tkfinder.move_simplifier(move['Command']) == tkfinder.move_simplifier(row[0]):
                        new_move['Gif'] = move['Gif']'''
                for entry in new_move:
                    if type(new_move[entry]) != list and (new_move[entry] is None or not new_move[entry].strip()):
                        new_move[entry] = "-"

                movelist.append(new_move)


        with open(output_file, 'w') as c:
            json.dump(movelist, c, sort_keys=True, indent=4, ensure_ascii=True)
