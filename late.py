from math import sqrt

import json
from types import SimpleNamespace

from trad.object_methods import update

def json_to_objects(json_input):
    """
    Given a JSON string or list of dicts, return a list of objects with attributes
    for each key (spaces in keys are replaced by underscores).
    """
    # If input is a string, parse it
    if isinstance(json_input, str):
        records = json.loads(json_input)
    else:
        records = json_input

    objects = []

    for record in records:
        # Replace spaces in keys
        clean_record = {k.replace(" ", "_"): v for k, v in record.items()}
        # Create an object with attributes
        obj = SimpleNamespace(**clean_record)
        objects.append(obj)

    return objects


def print_list(li):
    i = 0
    for s in li:
        i += 1
        if i >= 5:
            i = 0
            print()
        print_site(s)


    print('\n=============================\n')
    return

def print_site(s):
    name = s.Site_Name
    if s.Group:
        name += f' / {s.Group}'
    print(f'{s.SolarZone:8s} {name:40s} {s.r:2.3f}  n= {s.n:2d}/{s.n2:2d}  '
          f'  hy= {s.Hydration:1.0f}  sz= {s.Size:1.0f}  bb= {s.Burns:3.1f}  landing={s.landing} escape={s.escape:3.1f} '
          f'     aero={s.a:1.0f} haz={s.z:1.0f} comet={s.c:1.0f}  vf={s.vf:1.1f}  bf={s.bf:1.1f} tf={s.tf}')
    return


# Burn Factor
BK = 3
# Landing Burn Factor
LK = 1
# Escape Factor
EK = 2
# Aerobrake Hazard Factor
AZK = 5/6
#Group Prospect Factor
GPK = .2
#Comet Factor
CK = 2

# Zone Time Factor
ZTF = {
    'Mercury': 3,
    'Venus': 2,
    'Earth': 1,
    'Mars': 2,
    'Ceres': 3,
    'Jupiter': 5,
    'Saturn': 8,
    'Uranus': 14,
    'Neptune': 20,
}

# Hydration Value Factor
HVF = {
    0: 1,
    1: 5,
    2: 20,
    3: 40,
    4: 70
}

with open('high_frontier_sites.json', 'r') as f:
    json_doc = f.read()
sites = json_to_objects(json_doc)

for site in sites:

    hy = site.Hydration
    sz = site.Size
    bb = site.Burns

    a = site.Aerobrakes
    if a is None:
        a = 0

    z = site.Crashes
    if z is None:
        z = 0

    if site.Synodic:
        synodic = 1
        cf = CK
    else:
        synodic = 0
        cf = 1



    if a > 0:
        landing = 0
    else:
        landing = sz * LK
        if sz == 6:
            landing += LK
        elif sz > 6:
            landing += (sz - 6)*LK

    escape = sqrt(sz+1) * EK

    group = site.Group
    gp = max(site.RaygunGroup, site.BuggyGroup)

    # risk
    risk = 1 - (AZK**(a+z))

    # burn factor
    bf = BK * (bb**1.5 + landing) * (1 + risk)

    # time factor
    tf = ZTF[site.SolarZone]

    # value factor
    # todo: add push
    vf = (min(sz,6) + gp * GPK)*(HVF[hy])/(escape*cf*((z+1)*AZK))


    r = vf / (tf * bf * cf)
    r = sqrt(r)
    r1 = 45 * r
    n = int(r1 / 6)
    n2 = int(r1 - (6 * n))

    update(site, r=r, n=n, n2=n2, a=a, z=z, vf=vf, bf=bf, landing=landing, escape=escape, c=synodic, tf=tf)

sorted_list = sorted(sites, key=lambda e: e.Site_Name)
print_list(sorted_list)

print(100*'-')

sorted_list = sorted(sites, key=lambda e: e.r)
print_list(sorted_list)

