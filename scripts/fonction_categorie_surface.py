def categorize_surface(x):
    if x < 80:
        return "Petit"
    elif x <= 150:
        return "Moyen"
    else:
        return "Grand"