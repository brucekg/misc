from math import sqrt

with open('late.data', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip()
        tokens = line.split(',')
        # print(tokens)
        for i in range(1, len(tokens)):
            tokens[i] = float(tokens[i])
        name, hy, sz, b, l, hz = tokens
        r = sqrt((sz + 1) / ((6 - hy) * (b + 4 * l + 4 * hz)))
        n = int(13 * r)
        print(f'{name:10s} {r:7.3f}   n = {n:2d}')
