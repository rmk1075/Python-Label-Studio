def str2color(name: str) -> str:
    hash = 0
    for char in name: hash = ord(char) + ((hash << 5) - hash)
    color = '#'
    for i in range(3):
        value = (hash >> (i * 8)) & 0xFF
        color += '%.02x' % value
    return color