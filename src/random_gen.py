from src.imports import *

def generate_random_S(min_price = 50, max_price = 150):
    price = np.random.random() * (max_price - min_price) + min_price
    price = np.round(price, 1)
    return float(price)

def generate_random_sigma(min_sigma = 0.05, max_sigma = 0.15):
    sigma = np.random.random() * (max_sigma - min_sigma) + min_sigma
    sigma = np.round(np.random.random(), 2)
    return float(sigma)

def generate_random_rc(min_rc = 0, max_rc = 0.6):
    rc = np.random.random() * (max_rc - min_rc) + min_rc
    rc = np.round(20 * rc)/20
    return np.round(rc, 2)

def generate_random_T(months = [0.75,1,1.25]):
    return random.choice(months) * 30/252

def generate_K(S):
    num_k = 5
    diff = 5 if S < 100 else 10

    def closest_divisibles(s, k):
        closest = []
        base = (s // k) * k
        for i in range(2, 0, -1):
            closest.append(int(base - i * k))
        closest.append(int(base))
        for i in range(1, 3):
            closest.append(int(base + i * k))
        return sorted(closest)

    return closest_divisibles(S, diff)