# Clamps a number into a certain range
def clamp(n, min_val, max_val):
    return max(min_val, min(n, max_val))

# Formats the argument into XX:XX style
def time_format(seconds: int):
    m = str(int(seconds / 60)).zfill(2)
    s = str(int(seconds % 60)).zfill(2)
    return f"{m}:{s}"