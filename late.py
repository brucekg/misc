from math import sqrt
from trad.aobj import AObj

# Burn Factor
BK = 1
# Landing Burn Factor
LK = 3
# Aerobrake
AK = 2
# Hazard Factor
ZK = 4
#Group Prospect Factor
GPK = .5
#Comet Factor
CK = 4

def print_list(li):
    i = 0
    for s in li:
        i += 1
        if i >= 5:
            i = 0
            print()
        print(f'{s.name:20s} {s.mods:3s} {s.r:2.3f}  n= {s.n:2d}/{s.n2:2d}  '
              f'  hy= {s.hy:1.0f}  sz= {s.sz:1.0f}  b= {s.b:2.0f} {s.path}')
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

        # hydration
        hy = int(tokens.pop(0))

        # size (max. 6)
        sz = int(tokens.pop(0))

        # burns base (before alternative paths)
        bb = int(tokens.pop(0))

        #TODO: comets
        c = 0

        gp = 0

        path = None
        delta = 0

        mods = ''

        while tokens:
            token = tokens.pop(0)

            if token in ('gp'):
                mods += token.upper()
                gp = 1
                continue

            if token == 'c':
                mods += token.upper()
                c += 1
                continue

            paths = token.split('/')
            while paths:
                apath = paths.pop(0)
                b = 0
                l = 0.0
                a = 0
                z = 0
                for char in apath:
                    if char == 'b':
                        b += 1
                    elif char == 'l':
                        l += 1.0
                    elif char == 'h':
                        l += 0.5
                    elif char == 'a':
                        a += 1
                    elif char == 'a':
                        a += 1
                    elif char == 'z':
                        z += 1
                adelta = b * BK + l * LK + a * AK + z * ZK
                if (path is None) or (adelta < delta):
                    path = apath
                    delta = adelta


        site.update_(hy=hy, sz=sz, b=bb, path=(path or '').upper(), delta=delta, mods=mods, gp=gp, c=c)

        r = (sz + gp * GPK) / ((5 - hy) * (bb * BK + delta))
        r = sqrt(r)
        r1 = 45 * r
        n = int(r1 / 6)
        n2 = int(r1 - (6 * n))

        site.r = r
        site.n = n
        site.n2 = n2

        site_list.append(site)


sorted_list = sorted(site_list, key=lambda e: e.name)
print_list(sorted_list)

print(100*'-')

sorted_list = sorted(site_list, key=lambda e: e.r)
print_list(sorted_list)

