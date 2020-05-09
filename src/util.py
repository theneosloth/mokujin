def get_character_name_from_content(content):
    first_line = content[0]
    return first_line.split("Similar moves from ")[1]

def get_moves_from_content(content):
    content.pop(0)
    for i in range(len(content)):
        content[i] = content[i][7:]
    return content