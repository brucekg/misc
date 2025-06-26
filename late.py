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

# Burn Factor
BK = 1.5
# Landing Burn Factor
LK = .5
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
        print_site(s)


    print('\n=============================\n')
    return

def print_site(s):
    name = s.Site_Name
    print(f'{name:40s} {s.r:2.3f}  n= {s.n:2d}/{s.n2:2d}  '
          f'  hy= {s.Hydration:1.0f}  sz= {s.Size:1.0f}  b= {s.Burns:2.0f}')
    return


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
    else:
        comet = 0

    if a > 0:
        landing = 0
    else:
        landing = sz * LK

    group = site.Group
    gp = max(site.RaygunGroup, site.BuggyGroup)

    # print(json.dumps(site.__dict__, indent=4))
    # print(gp, bb, a, z, landing, comet)

    r = (min(sz,6) + gp * GPK)*(hy+1) / (5 * (bb * BK + a * AK + z * ZK + landing))
    r = sqrt(r)
    r1 = 45 * r
    n = int(r1 / 6)
    n2 = int(r1 - (6 * n))

    update(site,r=r,n=n,n2=n2)

sorted_list = sorted(sites, key=lambda e: e.Site_Name)
print_list(sorted_list)

print(100*'-')

sorted_list = sorted(sites, key=lambda e: e.r)
print_list(sorted_list)

