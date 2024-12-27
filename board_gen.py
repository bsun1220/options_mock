from options import *
from random_gen import *

def generate_board_one(info_dict = None):
    S, sigma, rc, T, Ks = None, None, None, None, None

    if info_dict is None:
        S = generate_random_S()
        sigma = generate_random_sigma()
        rc = generate_random_rc()
        T = generate_random_T()
        Ks = generate_K(S)
    else:
        S = info_dict['S']
        sigma = info_dict['sigma']
        rc = info_dict['rc']
        T = info_dict['T']
        Ks = info_dict['Ks']

    option_price_A = BsOption(S, Ks[0], T, rc, sigma).price('B')
    option_price_B = BsOption(S, Ks[1], T, rc, sigma).price('B')
    option_price_C = BsOption(S, Ks[2], T, rc, sigma).price('B')
    option_price_D = BsOption(S, Ks[3], T, rc, sigma).price('B')
    option_price_E = BsOption(S, Ks[4], T, rc, sigma).price('B')
    
    A_BW = np.round(option_price_A['put'] + rc, 2)
    A_B_CV = np.round(option_price_A['call'] - option_price_B['call'], 2)
    C_Straddle = np.round(option_price_C['call'] + option_price_C['put'], 2)
    D_E_CV = np.round(option_price_D['call'] - option_price_E['call'], 2)
    E_PS = np.round(option_price_E['call'] - rc, 2)

    combo_res = {}
    combo_res[f"{Ks[0]} BW"] = A_BW
    combo_res[f"{Ks[0]}-{Ks[1]} CV"] = A_B_CV
    combo_res[f"{Ks[2]} Straddle"] = C_Straddle
    combo_res[f"{Ks[3]}-{Ks[4]} CV"] = D_E_CV
    combo_res[f"{Ks[4]} PS"] = E_PS

    options_char = {}
    options_char = {'S':S, 'T':np.round(T, 2), 'Ks':Ks, 'rc':rc}

    ans = {}
    for K in Ks:
        option_price = BsOption(S, K, T, rc, sigma).price('B')
        call_delta = np.round(BsOption(S, K, T, rc, sigma).delta_call(), 2)
        put_delta = np.round(call_delta - 1, 2)
        ans[K] = {'C':(np.round(option_price['call'], 2), call_delta), 'P':(np.round(option_price['put'], 2), put_delta)}

        if option_price['call'] < 0 or option_price['put'] < 0:
            return generate_board_one()

    return combo_res, options_char, ans

def generate_board_two(info_dict = None):
    S, sigma, rc, T, Ks = None, None, None, None, None

    if info_dict is None:
        S = generate_random_S()
        sigma = generate_random_sigma()
        rc = generate_random_rc()
        T = generate_random_T()
        Ks = generate_K(S)
    else:
        S = info_dict['S']
        sigma = info_dict['sigma']
        rc = info_dict['rc']
        T = info_dict['T']
        Ks = info_dict['Ks']

    option_price_A = BsOption(S, Ks[0], T, rc, sigma).price('B')
    option_price_B = BsOption(S, Ks[1], T, rc, sigma).price('B')
    option_price_C = BsOption(S, Ks[2], T, rc, sigma).price('B')
    option_price_D = BsOption(S, Ks[3], T, rc, sigma).price('B')
    option_price_E = BsOption(S, Ks[4], T, rc, sigma).price('B')
    
    A_BW = np.round(option_price_A['put'] + rc, 2)
    A_B_PV = np.round(option_price_B['put'] - option_price_A['put'], 2)
    B_D_RR = np.round(option_price_B['call'] - option_price_D['put'], 2)
    C_Straddle = np.round(option_price_C['call'] + option_price_C['put'], 2)
    C_E_CV = np.round(option_price_C['call'] - option_price_E['call'], 2)

    combo_res = {}
    combo_res[f"{Ks[0]} BW"] = A_BW
    combo_res[f"{Ks[1]}-{Ks[0]} PV"] = A_B_PV
    combo_res[f"{Ks[2]} Straddle"] = C_Straddle
    combo_res[f"{Ks[1]}-{Ks[3]} RR"] = B_D_RR
    combo_res[f"{Ks[2]}-{Ks[4]} CV"] = C_E_CV

    options_char = {}
    options_char = {'S':S, 'T':np.round(T, 2), 'Ks':Ks, 'rc':rc}

    ans = {}
    for K in Ks:
        option_price = BsOption(S, K, T, rc, sigma).price('B')
        call_delta = np.round(BsOption(S, K, T, rc, sigma).delta_call(), 2)
        put_delta = np.round(call_delta - 1, 2)
        ans[K] = {'C':(np.round(option_price['call'], 2), call_delta), 'P':(np.round(option_price['put'], 2), put_delta)}

        if option_price['call'] < 0 or option_price['put'] < 0:
            return generate_board_two()

    return combo_res, options_char, ans

def generate_board_three(info_dict = None):
    S, sigma, rc, T, Ks = None, None, None, None, None

    if info_dict is None:
        S = generate_random_S()
        sigma = generate_random_sigma()
        rc = generate_random_rc()
        T = generate_random_T()
        Ks = generate_K(S)
    else:
        S = info_dict['S']
        sigma = info_dict['sigma']
        rc = info_dict['rc']
        T = info_dict['T']
        Ks = info_dict['Ks']

    option_price_A = BsOption(S, Ks[0], T, rc, sigma).price('B')
    option_price_B = BsOption(S, Ks[1], T, rc, sigma).price('B')
    option_price_C = BsOption(S, Ks[2], T, rc, sigma).price('B')
    option_price_D = BsOption(S, Ks[3], T, rc, sigma).price('B')
    option_price_E = BsOption(S, Ks[4], T, rc, sigma).price('B')
    
    A_BW = np.round(option_price_A['put'] + rc, 2)
    C_Straddle = np.round(option_price_C['call'] + option_price_C['put'], 2)
    D_E_PV = np.round(option_price_E['put'] - option_price_D['put'], 2)
    B_D_Strangle = np.round(option_price_B['call'] + option_price_D['put'], 2)
    E_PS = np.round(option_price_E['call'] - rc, 2)

    combo_res = {}
    combo_res[f"{Ks[0]} BW"] = A_BW
    combo_res[f"{Ks[1]}-{Ks[3]} Strangle"] = B_D_Strangle
    combo_res[f"{Ks[2]} Straddle"] = C_Straddle
    combo_res[f"{Ks[3]}-{Ks[4]} PV"] = D_E_PV
    combo_res[f"{Ks[4]} PS"] = E_PS

    options_char = {}
    options_char = {'S':S, 'T':np.round(T, 2), 'Ks':Ks, 'rc':rc}

    ans = {}
    for K in Ks:
        option_price = BsOption(S, K, T, rc, sigma).price('B')
        call_delta = np.round(BsOption(S, K, T, rc, sigma).delta_call(), 2)
        put_delta = np.round(call_delta - 1, 2)
        ans[K] = {'C':(np.round(option_price['call'], 2), call_delta), 'P':(np.round(option_price['put'], 2), put_delta)}

        if option_price['call'] < 0 or option_price['put'] < 0:
            return generate_board_three()

    return combo_res, options_char, ans


def generate_board_four(info_dict = None):
    S, sigma, rc, T, Ks = None, None, None, None, None

    if info_dict is None:
        S = generate_random_S()
        sigma = generate_random_sigma()
        rc = generate_random_rc()
        T = generate_random_T()
        Ks = generate_K(S)
    else:
        S = info_dict['S']
        sigma = info_dict['sigma']
        rc = info_dict['rc']
        T = info_dict['T']
        Ks = info_dict['Ks']

    option_price_A = BsOption(S, Ks[0], T, rc, sigma).price('B')
    option_price_B = BsOption(S, Ks[1], T, rc, sigma).price('B')
    option_price_C = BsOption(S, Ks[2], T, rc, sigma).price('B')
    option_price_D = BsOption(S, Ks[3], T, rc, sigma).price('B')
    option_price_E = BsOption(S, Ks[4], T, rc, sigma).price('B')
    
    A_BW = np.round(option_price_A['put'] + rc, 2)
    C_Straddle = np.round(option_price_C['call'] + option_price_C['put'], 2)
    C_D_CV = np.round(option_price_C['call'] - option_price_D['call'], 2)
    B_C_PV = np.round(option_price_C['put'] - option_price_B['put'], 2)
    E_C = np.round(option_price_E['call'] - rc, 2)

    combo_res = {}
    combo_res[f"{Ks[0]} BW"] = A_BW
    combo_res[f"{Ks[2]}-{Ks[3]} CV"] = C_D_CV
    combo_res[f"{Ks[2]} Straddle"] = C_Straddle
    combo_res[f"{Ks[2]}-{Ks[1]} PV"] = B_C_PV
    combo_res[f"{Ks[4]} C"] = E_C

    options_char = {}
    options_char = {'S':S, 'T':np.round(T, 2), 'Ks':Ks, 'rc':rc}

    ans = {}
    for K in Ks:
        option_price = BsOption(S, K, T, rc, sigma).price('B')
        call_delta = np.round(BsOption(S, K, T, rc, sigma).delta_call(), 2)
        put_delta = np.round(call_delta - 1, 2)
        ans[K] = {'C':(np.round(option_price['call'], 2), call_delta), 'P':(np.round(option_price['put'], 2), put_delta)}

        if option_price['call'] < 0 or option_price['put'] < 0:
            return generate_board_four()

    return combo_res, options_char, ans