# Copyright (C) 2022, Pyronear.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import json

# import french departement list
with open("src/static/departements-region.json") as f:
    dpt = json.load(f)

deps = [f"{d['num_dep']} - {d['dep_name']}" for d in dpt]
