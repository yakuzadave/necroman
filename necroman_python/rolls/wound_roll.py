def wound_roll(strength, toughness):
    # Necromunda wound chart approximation
    if strength >= toughness + 2:
        return 2  # 2+ to wound
    elif strength > toughness:
        return 3  # 3+ to wound
    elif strength == toughness:
        return 4  # 4+ to wound
    elif strength + 1 == toughness:
        return 5  # 5+ to wound
    else:
        return 6  # 6+ to wound
