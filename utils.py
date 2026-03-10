def rgb_to_hex(rgb):
    r = max(0, min(255, rgb[0]))
    g = max(0, min(255, rgb[1]))
    b = max(0, min(255, rgb[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


def get_clockwise_coordinates(length, width):
    coords = []

    for x in range(width):
        coords.append((x, 0))

    for y in range(1, length - 1):
        coords.append((width - 1, y))

    for x in range(width - 1, -1, -1):
        coords.append((x, length - 1))

    for y in range(length - 2, 0, -1):
        coords.append((0, y))
    return coords