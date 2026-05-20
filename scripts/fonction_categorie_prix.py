def categorize_price(x):
    if x < 500000:
        return "Économique"
    elif x < 1000000:
        return "Moyen"
    elif x < 2000000:
        return "Haut standing"
    else:
        return "Luxe"