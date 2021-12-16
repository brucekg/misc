from math import sqrt
from aobj import AObj

# Landing Burn Factor
LK = 4
# Aerobrake/Hazard Factor
AZK = 2

def print_list(li):
    for s in li:
        print(f'{s.name:12s} {s.mods:5s} {s.r:7.3f}   n = {s.n:2d} ><'
              f'  hy= {s.hy:1.0f}  sz= {s.sz:1.0f}  b= {s.b:2.0f}   l= {s.l:.1f}   hz= {s.hz:1.0f}')
    print('\n=============================\n')
    return

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
        gp = 0
        az = 0
        mods = ''
        site.update_(hy=hy, sz=sz, b=b, l=l, hz=hz, gp=gp, az=az, mods=mods)

        az_limit = l * LK / AZK
        while tokens:
            token = tokens.pop(0)
            for c in token:
                if c in 'gp':
                    assert gp == 0, f'GP error in line: {line}'
                    if c == 'g':
                        gp = 2 # group
                        mods += 'G'
                    if c == 'p':
                        gp = 1 # prospect
                        mods += 'P'
                    site.gp = gp
                    site.mods = mods

                if c == 'a': # aerobrake cancelled landing burn
                    l -= 1
                    az = 1
                    mods += 'A'
                if c =='z': # extra hazard on aerobrake path
                    az += 1
                    mods += 'Z'
                if c in 'az':
                    site.az = az
                    site.mods = mods

        az = min(az, az_limit)
        r = sqrt(sz + gp) / sqrt((6 - hy) * (b + 1 + LK * l + AZK * az))
        n = int(10 * r)

        site.r = r
        site.n = n

        site_list.append(site)


sorted_list = sorted(site_list, key=lambda e: e.name)
print_list(sorted_list)

sorted_list = sorted(site_list, key=lambda e: e.r)
print_list(sorted_list)

