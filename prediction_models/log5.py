

def log_five_prediction(wp1, wp2):
    if wp1 == 0 and wp2 == 0:
        return 0.5
    return (wp1 - (wp1 * wp2)) / (wp1 + wp2 - 2 * wp1 * wp2)
