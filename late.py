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
    print(f'{name:40s} {s.r:2.3f}  n= {s.n:2d}/{s.n2:2d}  '
          f'  hy= {s.Hydration:1.0f}  sz= {s.Size:1.0f}  bb= {s.Burns:2.0f}'
          f'     aero={s.a:1.0f} haz={s.z:1.0f} comet={s.c:1.0f}  vf={s.vf:1.0f}  bf={s.bf:1.0f}')
    return


# Burn Factor
BK = 2
# Landing Burn Factor
LK = .5
# Aerobrake
AK = 2
# Hazard Factor
ZK = 2
#Group Prospect Factor
GPK = .2
#Comet Factor
CK = 2

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
        comet = 1
        cf = CK
    else:
        comet = 0
        cf = 1

    if a > 0:
        landing = 0
    else:
        landing = sz * LK * BK

    group = site.Group
    gp = max(site.RaygunGroup, site.BuggyGroup)

    # burn factor
    bf = (bb * BK + a * AK + z * ZK + landing)

    # value factor
    vf = (min(sz,6) + gp * GPK)*((hy+1))


    r = vf / (5 * bf * cf)
    r = sqrt(r)
    r1 = 45 * r
    n = int(r1 / 6)
    n2 = int(r1 - (6 * n))

    update(site,r=r,n=n,n2=n2,a=a,z=z,vf=vf,bf=bf,c=comet)

sorted_list = sorted(sites, key=lambda e: e.Site_Name)
print_list(sorted_list)

print(100*'-')

sorted_list = sorted(sites, key=lambda e: e.r)
print_list(sorted_list)

