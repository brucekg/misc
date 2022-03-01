from math import sqrt
from aobj import AObj

# Landing Burn Factor
LK = 3
# Aerobrake
AK = 2
# Hazard Factor
ZK = 4
#Group Prospect Factor
GPK = .5

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
        a = 0
        z = 0
        mods = ''
        site.update_(hy=hy, sz=sz, b=b, l=l, hz=hz, gp=gp, a=a, z=z, mods=mods)

        l_pre_mods = l
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
                    a = 1
                    mods += 'A'
                    site.a = a
                if c =='z': # extra hazard on aerobrake path
                    z += 1
                    mods += 'Z'
                    site.z = z
                if c in 'az':
                    site.mods = mods

        # select between direct landing burns or aerobrake path
        la = min(l * LK + a * AK + z * ZK, l_pre_mods * LK)

        r = sqrt(sz + gp * GPK) / sqrt((6 - hy) * ((1 + b) * BK + hz * ZK + la))
        n = int(10 * r + .5)

        site.r = r
        site.n = n

        site_list.append(site)


sorted_list = sorted(site_list, key=lambda e: e.name)
print_list(sorted_list)

sorted_list = sorted(site_list, key=lambda e: e.r)
print_list(sorted_list)

