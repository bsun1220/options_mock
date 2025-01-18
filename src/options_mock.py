from src.board_gen import *
import xlwt

class OptionMock():
    def __init__(self):
        self.rand_board = None
        self.init = False
        self.saved_text = ""
        self.net_deltas = 0
        self.cust_order = ''

    def initialize_random_board(self):
        rand_funcs = [generate_board_one, generate_board_two, generate_board_three, generate_board_four]
        length =  len(rand_funcs) - 1
        rand_board = rand_funcs[random.randint(0, length)]()
        self.rand_board = rand_board
        self.saved_text = ""
        self.net_deltas = 0

    def print_clues(self):
        if self.saved_text != "":
            print(self.saved_text)
            return
        if self.rand_board is None:
            return

        txt_str = ""

        #Get Random Stock
        stock_edges = [0.05, 0.1]
        stock_width = stock_edges[random.randint(0, 1)]
        stock_liquidities = [50, 100, 150]
        stock_liquidity = stock_liquidities[random.randint(0, 2)]

        stock_px = self.rand_board[1]['S']
        stock_rc = self.rand_board[1]['rc']
        txt_str += f"Stock: {np.round(stock_px - stock_width, 2)} @ {np.round(stock_px + stock_width, 2)}, {stock_liquidity} up\n"
        self.saved_text = txt_str
        expiry_time = np.round(self.rand_board[1]['T'] * 252)
        txt_str += f"TTE: {int(expiry_time)} Days, RC: {stock_rc}\n"

        stock_strikes = self.rand_board[1]['Ks']
        txt_str += f"Strikes: {stock_strikes}\n"
        txt_str += "\nCOMBOS\n-------------\n"
        for combo in self.rand_board[0]:
            edges = [0, 0.05, 0.1]
            liquidities = [40, 50, 60, 70, 80, 100]
            
            edge = edges[random.randint(0, 2)]
            liquidity = random.choice(liquidities)

            if edge == 0:
                txt_str += f"{combo}: {self.rand_board[0][combo]}\n"
            else:
                px = self.rand_board[0][combo]
                txt_str += f"{combo}: {np.round(px - edge, 2)} @ {np.round(px + edge, 2)}, {liquidity} up\n"

        self.saved_text = txt_str
        print(txt_str)

    def random_bot_order(self, printed = True):
        if self.rand_board is None:
            return
        
        buy_sell = random.randint(0, 1)
        combos = ['call', 'put', 'straddle', 'cv', 'pv','combo']
        selected_combo = random.choice(combos)

        strikes = self.rand_board[1]['Ks']
        selected_strikes = random.sample(strikes, 2)
        random.shuffle(selected_strikes)
        s1 = selected_strikes[0]
        s2 = selected_strikes[1]
        sizes = [50, 50, 60, 60, 70, 70, 80, 80, 90, 100, 150, 200, 300]
        random_size = random.choice(sizes)
        delta_sign = 1 if buy_sell else -1
        verb = 'buy' if buy_sell else 'sell'

        txt = ''
        if selected_combo == 'call':
            txt = f"Cust {verb}s the {s1}-strike call, {random_size} lots"
            self.net_deltas += delta_sign * self.rand_board[2][s1]['C'][1] * random_size
        elif selected_combo == 'put':
            txt = f"Cust {verb}s the {s1}-strike put, {random_size} lots"
            self.net_deltas += delta_sign * self.rand_board[2][s1]['P'][1] * random_size
        elif selected_combo == 'straddle':
            straddle_delta = self.rand_board[2][s1]['P'][1] + self.rand_board[2][s1]['C'][1]
            txt = f"Cust {verb}s the {s1}-strike straddle, {random_size} lots"
            self.net_deltas += delta_sign * straddle_delta * random_size
        elif selected_combo == 'combo':
            txt = f"Cust {verb}s the {s1}-strike combo, {random_size} lots"
            self.net_deltas += delta_sign * random_size
        elif selected_combo == 'pv':
            min_strike = min(s1, s2)
            max_strike = max(s1, s2)
            combo_delta = self.rand_board[2][max_strike]['P'][1] - self.rand_board[2][min_strike]['P'][1]
            txt = f"Cust {verb}s the {max_strike}-{min_strike} strike PV, {random_size} lots"
            self.net_deltas += delta_sign * random_size * combo_delta
        elif selected_combo == 'cv':
            min_strike = min(s1, s2)
            max_strike = max(s1, s2)
            combo_delta = self.rand_board[2][min_strike]['C'][1] - self.rand_board[2][max_strike]['C'][1]
            txt = f"Cust {verb}s the {min_strike}-{max_strike} strike CV, {random_size} lots"
            self.net_deltas += delta_sign * random_size * combo_delta

        if printed:
            print(txt)
        else:
            self.cust_order = txt
        self.net_deltas = np.round(self.net_deltas, 2)

    def print_net_deltas(self):
        print(self.net_deltas)
    
    def get_fairs(self):
        return self.rand_board[2]

    def create_excel(self, file_name = 'options_mock', num_orders = 10):
        if self.rand_board is None:
            return
        
        wb = xlwt.Workbook()
        ws1 = wb.add_sheet('Options Board')

        stock_edges = [0.05, 0.1]
        stock_width = stock_edges[random.randint(0, 1)]
        stock_liquidities = [50, 100, 150]
        stock_liquidity = stock_liquidities[random.randint(0, 2)]

        stock_px = self.rand_board[1]['S']
        stock_rc = self.rand_board[1]['rc']

        stock_txt = f"Stock: {np.round(stock_px - stock_width, 2)} @ {np.round(stock_px + stock_width, 2)}, {stock_liquidity} up"

        expiry_time = np.round(self.rand_board[1]['T'] * 252)
        char_txt = f"TTE: {int(expiry_time)} Days, RC: {stock_rc}"
        ws1.write(1, 3, stock_txt)
        ws1.write(2, 3, char_txt)

        ws1.write(6, 3, 'Call')
        ws1.write(6, 4, 'Put')
        ws1.write(8, 2, self.rand_board[1]['Ks'][0])
        ws1.write(9, 2, self.rand_board[1]['Ks'][1])
        ws1.write(10, 2, self.rand_board[1]['Ks'][2])
        ws1.write(11, 2, self.rand_board[1]['Ks'][3])
        ws1.write(12, 2, self.rand_board[1]['Ks'][4])

        ws1.write(14, 0, "COMBOS")
        ind = 0
        for combo in self.rand_board[0]:
            
            edges = [0, 0.05, 0.1]
            liquidities = [40, 50, 60, 70, 80, 100]
            
            edge = edges[random.randint(0, 2)]
            liquidity = random.choice(liquidities)

            txt = ""
            if edge == 0:
                txt = f"{combo}: {self.rand_board[0][combo]}\n"
            else:
                px = self.rand_board[0][combo]
                txt = f"{combo}: {np.round(px - edge, 2)} @ {np.round(px + edge, 2)}, {liquidity} up\n"

            ws1.write(15+ind, 0, txt)
            ind += 1

        ws1.write(14, 3, "CUST ORDERS")
        ind = 0
        for i in range(num_orders):
            self.random_bot_order(printed = False)
            ws1.write(15+ind, 3, self.cust_order)
            ind += 1 


        ws2 = wb.add_sheet('Answer Key')
        ws2.write(6, 3, 'Call')
        ws2.write(6, 4, 'Put')
        for i in range(5):
            strike = self.rand_board[1]['Ks'][i]
            ws2.write(8 + i, 2, strike)
            call_px = self.rand_board[2][strike]['C'][0]
            put_px = self.rand_board[2][strike]['P'][0]
            ws2.write(8 + i, 3, f'{call_px}')
            ws2.write(8 + i, 4, f'{put_px}')
            delta = self.rand_board[2][strike]['C'][1]
            ws2.write(8 + i, 5, f'Delta: {delta}')

        
        wb.save(f'board/{file_name}.xls')
        
        

        

        

        

        



