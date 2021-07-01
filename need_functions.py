def choose_biggest_size(sizes):
    size = "smxopqryzw"
    return max(sizes, key=lambda s: size.index(s["type"]))
