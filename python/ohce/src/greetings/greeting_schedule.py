def find_greeting(time):
    if time >= 20 or (0 <= time < 6):
        return "¡Buenas noches {}!"
    elif 0 <= time < 12:
        return "¡Buenos días {}!"
    elif 12 <= time < 20:
        return "¡Buenas tardes {}!"
