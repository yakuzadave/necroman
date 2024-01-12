# Using the House Cawdor equipment list obtained from Necrovox, we will generate a 1000 points gang.
# We will randomly select gang members, assign them roles, and equip them with weapons and gear.
# The goal is to create a balanced and thematic gang within the point limit.

import random

# House Cawdor equipment list
equipment_list = {
    "Weapons": {
        "Autogun": 25,
        "Autopistol": 15,
        "Blunderbuss": 30,
        "Hand Flamer": 35,
        "Reclaimed Autogun": 5,
        "Reclaimed Autopistol": 10,
        "Stub Gun": 5,
        "Fighting Knife": 10,
        "Axe": 15,
        "Chainsword": 25,
        "Two-Handed Axe": 20,
        "Two-Handed Hammer": 20
    },
    "Gear": {
        "Frag Grenades": 30,
        "Krak Grenades": 40,
        "Mesh Armour": 15,
        "Flak Armour": 10,
        "Gas Mask": 10
    }
}

# House Cawdor gangers cost
ganger_costs = {
    "Leader": 120,
    "Champion": 95,
    "Ganger": 45,
    "Juve": 25
}

# Gang composition rules: At least 50% of the gang must be Gangers
def create_gang(budget):
    gang = []
    budget_remaining = budget

    # Add a Leader
    gang.append({"Type": "Leader", "Cost": ganger_costs["Leader"], "Equipment": []})
    budget_remaining -= ganger_costs["Leader"]

    # Ensure at least 50% Gangers
    while budget_remaining > 0:
        if len([g for g in gang if g["Type"] == "Ganger"]) < len(gang) / 2:
            member_type = "Ganger"
        else:
            member_type = random.choice(["Champion", "Ganger", "Juve"])
        member_cost = ganger_costs[member_type]

        if member_cost <= budget_remaining:
            gang.append({"Type": member_type, "Cost": member_cost, "Equipment": []})
            budget_remaining -= member_cost

    # Equip the gang members
    for member in gang:
        while True:
            item, item_cost = random.choice(list(equipment_list["Weapons"].items()) + list(equipment_list["Gear"].items()))
            if member["Cost"] + item_cost <= budget:
                member["Equipment"].append(item)
                member["Cost"] += item_cost
                budget_remaining -= item_cost
            if budget_remaining <= 0 or random.random() < 0.5:
                break

    return gang, budget_remaining

# Generate the gang
cawdor_gang, remaining_points = create_gang(1000)
cawdor_gang, remaining_points