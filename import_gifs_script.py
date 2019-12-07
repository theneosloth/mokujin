import json, os

#import gifs from the source folder into json folders by comparing the moves notation and alias
from src import tkfinder

# the source path = gifs folder from T7 chicken app on your local machine
source_path = 'tc/'
to_path = 'json/'
inentries = os.listdir(source_path)
outentries = os.listdir(to_path)

for entry in inentries:
    with open(source_path + entry, 'r') as chicken_app_json:
        from_data = json.load(chicken_app_json)
    with open(to_path + entry, 'r') as mokujin_json:
        to_data = json.load(mokujin_json)
    for from_move in from_data['movelist']:

        if ('preview_url' in from_move and from_move['preview_url']) :
            for to_move in to_data:

                if not 'Gif' in to_move or not to_move['Gif'] and 'Alias' in to_move:

                    from_notation = tkfinder.move_simplifier(from_move['notation'].lower().strip())
                    to_notation = tkfinder.move_simplifier(to_move['Command'].lower().strip())#

                    if  (to_notation == from_notation or from_notation in map(tkfinder.move_simplifier, to_move['Alias'])) :

                        gif_url = from_move['preview_url'].replace("https://giant.", "https://")
                        gif_url = gif_url.replace('\n','')

                        to_move['Gif'] = gif_url

                        msg = '{};{};{}'.format(from_data['displayName'], from_move['notation'].strip(), gif_url)
                        print(msg)

        chicken_app_json.close()
        mokujin_json.close()

    with open(to_path + entry, 'w') as c:
        json.dump(to_data, c, sort_keys=True, indent=4)


# with open('akuma.json'), 'r' as f: indata = json.load(f)
# with open('akuma.json'), 'w' as f: outdata = json.load(f)
print("done")
