DEFAULT_TRESHOLD = .1

def sign_treshold(x, treshold=DEFAULT_TRESHOLD):
    if x < -treshold:
        return -1
    elif x > treshold:
        return 1
    return 0

