from math import sqrt
from aobj import AObj

with open('late.data', 'r') as f:
    site_list = list()
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        tokens = line.split()
        # print(tokens)

        site = AObj()
        name = tokens.pop(0)
        site.name = name
        values = list()
        while tokens:
            token = tokens[0]
            if token.strip('0') == '.5':
                values.append(.5)
            elif token.isdigit():
                values.append(float(token))
            else:
                break
            tokens.pop(0)
        while len(values) < 5:
            values.append(0.0)

        hy, sz, b, l, hz = values
        site.update_(hy=hy, sz=sz, b=b, l=l, hz=hz, gp=0)
        gp = 0

        while tokens:
            token = tokens.pop(0)
            for c in token:
                if c in 'gp':
                    assert gp == 0, f'GP error in line: {line}'
                    if c == 'g':
                        gp = 2
                    else:
                        gp = 1
                    site.gp = gp

        # r = sqrt((1 + sz + g) / ((6 - hy) * (b + 4 * l + 4 * hz)))
        r = sqrt(sz + gp) / sqrt((6 - hy) * (b + 1 + 4 * l + 4 * hz))
        n = int(10 * r)
        # print(f'{name:10s} {" PG"[gp]} {r:7.3f}   n = {n:2d}')

        site.r = r
        site.n = n

        site_list.append(site)

print('=============================\n')

sorted_list = sorted(site_list, key=lambda e: e.r)
for site in sorted_list:
    print(f'{site.name:10s} {" PG"[site.gp]} {site.r:7.3f}   n = {site.n:2d}')
