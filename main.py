#!/usr/bin/env python3
"""
Sistem Slot dengan Save/Load + Quick Bet Buttons
Sistem adalah ilusi
"""

import random, time, os, sys
import json
from datetime import datetime

# ---------- CONFIG ----------
START_BALANCE = 1000
MIN_BET = 1
SYMBOLS = ["🍒", "🔔", "7"]
WEIGHTS = [50, 30, 10]
PAYOUT_3 = {"🍒": 5, "🔔": 10, "7": 50}
PAYOUT_2 = {"🍒": 1.5, "🔔": 2, "7": 5}
SPIN_SPEED = 0.08
HIGHSCORE_FILE = "slot_highscore.txt"
SAVE_FILE = "slot_save.json"

# ---------- COLOR CODES ----------
class Colors:
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[97m'
    GOLD, ORANGE, RESET, BOLD = '\033[38;5;220m', '\033[38;5;214m', '\033[0m', '\033[1m'

SYMBOL_COLORS = {"🍒": Colors.RED + Colors.BOLD, "🔔": Colors.YELLOW + Colors.BOLD, "7": Colors.GOLD + Colors.BOLD}

# ---------- QUICK BET SYSTEM (FIXED) ----------
QUICK_BETS = [
    {"name": "10", "value": 10, "type": "fixed"},
    {"name": "50", "value": 50, "type": "fixed"},
    {"name": "100", "value": 100, "type": "fixed"},
    {"name": "500", "value": 500, "type": "fixed"},
    {"name": "1K", "value": 1000, "type": "fixed"},
    {"name": "5K", "value": 5000, "type": "fixed"},
    {"name": "10K", "value": 10000, "type": "fixed"},
    {"name": "HALF", "value": 0.5, "type": "percentage"},
    {"name": "ALL-IN", "value": 1.0, "type": "percentage"}
]

def format_large_number(number):
    """Format angka besar menjadi lebih readable"""
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}K"
    else:
        return str(number)

def calculate_quick_bet(choice_index, current_balance):
    """
    Calculate bet amount based on quick bet choice
    """
    if choice_index < 0 or choice_index >= len(QUICK_BETS):
        return None
    
    bet_option = QUICK_BETS[choice_index]
    
    if bet_option["type"] == "fixed":
        return bet_option["value"]
    elif bet_option["type"] == "percentage":
        calculated_bet = int(current_balance * bet_option["value"])
        return max(MIN_BET, calculated_bet)  # Ensure at least MIN_BET

def show_quick_bet_menu(current_balance, current_bet):
    """
    Display quick bet selection menu (FIXED)
    """
    print(f"\n{Colors.CYAN}{Colors.BOLD}⚡ QUICK BET MENU:{Colors.RESET}")
    print(f"{Colors.WHITE}Saldo Saat Ini: {Colors.GREEN}{format_large_number(current_balance)}{Colors.RESET}")
    print(f"{Colors.WHITE}Taruhan Saat Ini: {Colors.YELLOW}{format_large_number(current_bet)}{Colors.RESET}")
    print()
    
    # Tampilkan dalam grid 3x3 untuk better layout
    for i, bet_option in enumerate(QUICK_BETS, 1):
        if bet_option["type"] == "fixed":
            display_value = bet_option["value"]
        else:
            display_value = calculate_quick_bet(i-1, current_balance)
        
        # Format display value
        formatted_display = format_large_number(display_value)
        
        # Highlight jika ini adalah current bet
        is_current = (display_value == current_bet)
        bet_color = Colors.GREEN + Colors.BOLD if is_current else Colors.WHITE
        
        # Tampilkan dengan grid layout
        if i <= 3:
            # Baris pertama
            print(f"{bet_color}{i}. {bet_option['name']}: {formatted_display:>6}{Colors.RESET} {'✓' if is_current else ' ':2}", end="  ")
        elif i <= 6:
            # Baris kedua  
            if i == 4:
                print()  # New line
            print(f"{bet_color}{i}. {bet_option['name']}: {formatted_display:>6}{Colors.RESET} {'✓' if is_current else ' ':2}", end="  ")
        else:
            # Baris ketiga
            if i == 7:
                print()  # New line
            print(f"{bet_color}{i}. {bet_option['name']}: {formatted_display:>6}{Colors.RESET} {'✓' if is_current else ' ':2}", end="  ")
    
    print(f"\n\n{Colors.YELLOW}10. Custom Bet (Input Manual){Colors.RESET}")
    print(f"{Colors.YELLOW}0. Kembali ke Menu Utama{Colors.RESET}")
    print(f"{Colors.BLUE}{'-'*50}{Colors.RESET}")

def quick_bet_interface(current_balance, current_bet):
    """
    Handle quick bet selection interface (FIXED)
    """
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}=== ⚡ QUICK BET SELECTION ==={Colors.RESET}")
        show_quick_bet_menu(current_balance, current_bet)
        
        choice = smart_input(
            f"{Colors.WHITE}Pilih taruhan cepat {Colors.CYAN}[0-10]{Colors.WHITE}: {Colors.RESET}",
            options=['0','1','2','3','4','5','6','7','8','9','10'],
            input_type=str
        )
        
        if choice is None or choice == '0':
            return current_bet  # Return unchanged
            
        if choice == '10':  # Custom bet
            print(f"\n{Colors.CYAN}Custom Bet Selection{Colors.RESET}")
            custom_bet = smart_input(
                f"{Colors.WHITE}Masukkan taruhan manual (min {MIN_BET}, max {format_large_number(current_balance)}): {Colors.RESET}",
                input_type=int,
                min_val=MIN_BET,
                max_val=current_balance
            )
            if custom_bet is not None:
                if custom_bet > current_balance:
                    print(f"{Colors.RED}❌ Taruhan {format_large_number(custom_bet)} melebihi saldo {format_large_number(current_balance)}!{Colors.RESET}")
                    time.sleep(2)
                else:
                    print(f"{Colors.GREEN}✅ Taruhan diatur: {format_large_number(custom_bet)}{Colors.RESET}")
                    time.sleep(1.5)
                    return custom_bet
            continue
        
        # Quick bet selection (1-9)
        choice_index = int(choice) - 1
        new_bet = calculate_quick_bet(choice_index, current_balance)
        
        if new_bet is not None:
            if new_bet > current_balance:
                print(f"{Colors.RED}❌ Taruhan {format_large_number(new_bet)} melebihi saldo {format_large_number(current_balance)}!{Colors.RESET}")
                time.sleep(2)
            else:
                print(f"{Colors.GREEN}✅ Taruhan diatur: {format_large_number(new_bet)}{Colors.RESET}")
                time.sleep(1.5)
                return new_bet
        else:
            print(f"{Colors.RED}❌ Pilihan tidak valid!{Colors.RESET}")
            time.sleep(1.5)

# ---------- SAVE/LOAD SYSTEM ----------
def save_game(balance, history, current_bet, stats=None):
    """
    Save game progress ke file JSON
    """
    try:
        save_data = {
            "balance": balance,
            "current_bet": current_bet,
            "history": history[-20:],  # Simpan 20 history terakhir saja
            "stats": stats or {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.2"
        }
        
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"{Colors.RED}Error saving game: {e}{Colors.RESET}")
        return False

def load_game():
    """
    Load game progress dari file JSON
    Returns: (balance, history, current_bet, stats) atau None jika gagal
    """
    try:
        if not os.path.exists(SAVE_FILE):
            return None
            
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            save_data = json.load(f)
        
        # Validasi data
        if all(key in save_data for key in ["balance", "current_bet", "history"]):
            print(f"{Colors.GREEN}✓ Game loaded (Saved: {save_data.get('timestamp', 'Unknown')}){Colors.RESET}")
            time.sleep(1)
            return (
                save_data["balance"],
                save_data["history"],
                save_data["current_bet"],
                save_data.get("stats", {})
            )
        else:
            print(f"{Colors.RED}Save file corrupted{Colors.RESET}")
            return None
            
    except Exception as e:
        print(f"{Colors.RED}Error loading game: {e}{Colors.RESET}")
        return None

def delete_save_file():
    """
    Hapus file save
    """
    try:
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
            return True
    except:
        pass
    return False

# ---------- UTILS ----------
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

def read_highscore():
    try: return int(open(HIGHSCORE_FILE, "r", encoding="utf-8").read().strip())
    except: return 0

def write_highscore(v):
    try: open(HIGHSCORE_FILE, "w", encoding="utf-8").write(str(int(v)))
    except: pass

def smart_input(prompt, options=None, input_type=str, min_val=None, max_val=None):
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.lower() in ('q', 'quit', 'exit', 'keluar'): return None
            
            if options and input_type == str:
                if user_input in options: 
                    return user_input
                print(f"{Colors.RED}Perintah tidak valid. Pilihan: {', '.join(options)}{Colors.RESET}")
                time.sleep(1.5)
                return "back"
            
            elif input_type == int:
                value = int(user_input)
                if min_val and value < min_val: 
                    print(f"{Colors.RED}Minimal: {min_val}{Colors.RESET}")
                    continue
                elif max_val and value > max_val: 
                    print(f"{Colors.RED}Maksimal: {max_val}{Colors.RESET}")
                    continue
                else: 
                    return value
        except ValueError: 
            print(f"{Colors.RED}Harap masukkan angka.{Colors.RESET}")
        except KeyboardInterrupt: 
            return None

def colored_symbol(symbol): return SYMBOL_COLORS.get(symbol, Colors.WHITE) + symbol + Colors.RESET

# ---------- GAME LOGIC ----------
def spin_reels(): return tuple(random.choices(SYMBOLS, weights=WEIGHTS, k=3))

def evaluate(result, bet):
    a, b, c = result
    if a == b == c:
        mult = PAYOUT_3.get(a, 0)
        return int(bet * mult), f"{Colors.GOLD if a == '7' else Colors.GREEN}Tiga {a}! {Colors.BOLD}JACKPOT! ({mult}x){Colors.RESET}"
    elif a == b or a == c or b == c:
        sym = a if a == b or a == c else b
        mult = PAYOUT_2.get(sym, 0)
        return int(bet * mult), f"{Colors.GREEN}Dua {sym}! Menang kecil ({mult}x){Colors.RESET}"
    return 0, f"{Colors.RED}Tidak ada yang cocok{Colors.RESET}"

def animate_spin(duration=0.9):
    t0 = time.time()
    try:
        while time.time() - t0 < duration:
            reels = [random.choice(SYMBOLS) for _ in range(3)]
            colored_reels = [colored_symbol(sym) for sym in reels]
            sys.stdout.write("\r" + Colors.CYAN + "[ " + Colors.RESET + " | ".join(colored_reels) + Colors.CYAN + " ]" + Colors.RESET + "   ")
            sys.stdout.flush()
            time.sleep(SPIN_SPEED)
        sys.stdout.write("\r" + " " * 50 + "\r")
    except KeyboardInterrupt: sys.stdout.write("\n")

def show_detailed_help(help_type=None):
    """
    Menampilkan help detail dengan pilihan menu
    """
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}=== 📋 HELP & PANDUAN ==={Colors.RESET}")
    
    if help_type is None:
        # Main help menu
        print(f"\n{Colors.YELLOW}Pilih kategori bantuan:{Colors.RESET}")
        print(f"{Colors.WHITE}1. {Colors.CYAN}Perintah Dasar{Colors.RESET}")
        print(f"{Colors.WHITE}2. {Colors.CYAN}Quick Bet System{Colors.RESET}")
        print(f"{Colors.WHITE}3. {Colors.CYAN}Cara Bermain{Colors.RESET}")
        print(f"{Colors.WHITE}4. {Colors.CYAN}Payout & Hadiah{Colors.RESET}")
        print(f"{Colors.WHITE}5. {Colors.CYAN}Semua Bantuan{Colors.RESET}")
        print(f"{Colors.WHITE}0. {Colors.YELLOW}Kembali ke Game{Colors.RESET}")
        print(f"{Colors.BLUE}{'-'*40}{Colors.RESET}")
        
        choice = smart_input(
            f"{Colors.WHITE}Pilih kategori {Colors.CYAN}[0-5]{Colors.WHITE}: {Colors.RESET}",
            options=['0','1','2','3','4','5'],
            input_type=str
        )
        
        if choice == '0' or choice is None:
            return
        elif choice == '1':
            show_detailed_help('basic')
        elif choice == '2':
            show_detailed_help('quickbet')
        elif choice == '3':
            show_detailed_help('gameplay')
        elif choice == '4':
            show_detailed_help('payout')
        elif choice == '5':
            show_detailed_help('all')
        return
    
    # Tampilkan help berdasarkan kategori
    if help_type == 'basic' or help_type == 'all':
        print(f"\n{Colors.GREEN}🎯 {Colors.BOLD}PERINTAH DASAR:{Colors.RESET}")
        basic_commands = [
            ("S / Enter", "Spin - Putar slot dengan taruhan saat ini"),
            ("B", "Quick Bet - Menu taruhan cepat"),
            ("H", "History - Lihat riwayat spin terakhir"),
            ("R", "Reset - Reset saldo ke awal"),
            ("L", "Save - Simpan game manual"),
            ("V", "Stats - Lihat statistik permainan"),
            ("?", "Help - Menu bantuan ini"),
            ("Q", "Quit - Keluar dari game")
        ]
        for cmd, desc in basic_commands:
            print(f"  {Colors.WHITE}{cmd:<12}{Colors.YELLOW}{desc}{Colors.RESET}")
    
    if help_type == 'quickbet' or help_type == 'all':
        print(f"\n{Colors.GREEN}⚡ {Colors.BOLD}QUICK BET SYSTEM:{Colors.RESET}")
        print(f"  {Colors.WHITE}Pilihan taruhan cepat:{Colors.RESET}")
        quick_bet_info = [
            ("1-7", "Taruhan fixed: 10, 50, 100, 500, 1K, 5K, 10K"),
            ("8", "Half - 50% dari saldo saat ini"),
            ("9", "All-in - 100% dari saldo saat ini"),
            ("10", "Custom Bet - Input manual")
        ]
        for key, desc in quick_bet_info:
            print(f"  {Colors.WHITE}{key:<8}{Colors.YELLOW}{desc}{Colors.RESET}")
    
    if help_type == 'gameplay' or help_type == 'all':
        print(f"\n{Colors.GREEN}🎮 {Colors.BOLD}CARA BERMAIN:{Colors.RESET}")
        gameplay_info = [
            ("Goal", "Dapatkan kombinasi simbol yang sama"),
            ("3 Simbol", "Menang besar dengan multiplier tinggi"),
            ("2 Simbol", "Menang kecil dengan multiplier rendah"),
            ("Auto-save", "Game otomatis tersimpan saat penting"),
            ("Win Streak", "Track berapa kali menang berturut-turut")
        ]
        for item, desc in gameplay_info:
            print(f"  {Colors.WHITE}{item:<12}{Colors.YELLOW}{desc}{Colors.RESET}")
    
    if help_type == 'payout' or help_type == 'all':
        print(f"\n{Colors.GREEN}💰 {Colors.BOLD}PAYOUT & HADIAH:{Colors.RESET}")
        print(f"  {Colors.WHITE}3 Simbol sama:{Colors.RESET}")
        for symbol, mult in PAYOUT_3.items():
            colored_sym = colored_symbol(symbol)
            print(f"    {colored_sym} {Colors.WHITE}: {Colors.GOLD}{mult}x{Colors.RESET} taruhan")
        
        print(f"  {Colors.WHITE}2 Simbol sama:{Colors.RESET}")
        for symbol, mult in PAYOUT_2.items():
            colored_sym = colored_symbol(symbol)
            print(f"    {colored_sym} {Colors.WHITE}: {Colors.GREEN}{mult}x{Colors.RESET} taruhan")
    
    print(f"\n{Colors.BLUE}{'-'*50}{Colors.RESET}")
    input(f"{Colors.CYAN}Tekan Enter untuk kembali...{Colors.RESET}")
    
    # Kembali ke menu help utama (kecuali untuk 'all')
    if help_type != 'all':
        show_detailed_help(None)

def show_help():
    """
    Legacy help function untuk kompatibilitas
    """
    show_detailed_help('basic')

# ---------- STATISTICS SYSTEM ----------
def init_stats():
    """Initialize player statistics"""
    return {
        "total_spins": 0,
        "total_bet": 0,
        "total_won": 0,
        "biggest_win": 0,
        "current_streak": 0,
        "max_streak": 0,
        "last_save": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def update_stats(stats, bet, payout):
    """Update statistics after each spin"""
    stats["total_spins"] += 1
    stats["total_bet"] += bet
    
    if payout > 0:
        stats["total_won"] += payout
        stats["biggest_win"] = max(stats["biggest_win"], payout)
        stats["current_streak"] += 1
        stats["max_streak"] = max(stats["max_streak"], stats["current_streak"])
    else:
        stats["current_streak"] = 0
    
    return stats

def show_stats(stats):
    """Display player statistics"""
    if not stats or stats["total_spins"] == 0:
        print(f"{Colors.YELLOW}Belum ada statistik{Colors.RESET}")
        return
    
    win_rate = (stats["total_won"] / stats["total_bet"] * 100) if stats["total_bet"] > 0 else 0
    profit = stats["total_won"] - stats["total_bet"]
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 STATISTIK:{Colors.RESET}")
    print(f"{Colors.WHITE}Total Spin: {Colors.YELLOW}{stats['total_spins']}{Colors.RESET}")
    print(f"{Colors.WHITE}Win Rate: {Colors.GREEN if win_rate > 100 else Colors.YELLOW if win_rate == 100 else Colors.RED}{win_rate:.1f}%{Colors.RESET}")
    print(f"{Colors.WHITE}Profit: {Colors.GREEN if profit > 0 else Colors.RED if profit < 0 else Colors.YELLOW}{profit}{Colors.RESET}")
    print(f"{Colors.WHITE}Kemenangan Terbesar: {Colors.GOLD}{format_large_number(stats['biggest_win'])}{Colors.RESET}")
    print(f"{Colors.WHITE}Win Streak: {Colors.GREEN}{stats['current_streak']}{Colors.RESET} | Terbaik: {Colors.GOLD}{stats['max_streak']}{Colors.RESET}")

# ---------- MAIN GAME ----------
def main():
    # Try to load saved game, otherwise start new
    loaded_data = load_game()
    
    if loaded_data:
        balance, history, current_bet, loaded_stats = loaded_data
        stats = loaded_stats if loaded_stats else init_stats()
        print(f"{Colors.GREEN}Game berhasil dimuat!{Colors.RESET}")
    else:
        balance = START_BALANCE
        history = []
        current_bet = MIN_BET
        stats = init_stats()
        print(f"{Colors.YELLOW}Memulai game baru...{Colors.RESET}")
    
    time.sleep(1)
    highscore = max(balance, read_highscore())
    spins = 0

    def header():
        clear_screen()
        balance_color = Colors.GREEN if balance >= START_BALANCE else Colors.YELLOW if balance >= 500 else Colors.RED
        print(f"{Colors.CYAN}{Colors.BOLD}=== 🎰 SLOT GACOR 123.xyz 🎰 ==={Colors.RESET}")
        print(f"{Colors.WHITE}Saldo: {balance_color}{format_large_number(balance)}{Colors.RESET}   Taruhan: {Colors.YELLOW}{format_large_number(current_bet)}{Colors.RESET}   Highscore: {Colors.GOLD}{format_large_number(highscore)}{Colors.RESET}")
        
        # Tampilkan streak jika ada
        if stats["current_streak"] > 0:
            streak_color = Colors.GREEN if stats["current_streak"] >= 3 else Colors.YELLOW
            print(f"{Colors.WHITE}Win Streak: {streak_color}{stats['current_streak']}🔥{Colors.RESET}")
        
        print(f"{Colors.YELLOW}S:Spin  B:Quick Bet  H:History  R:Reset  L:Save  V:Stats  ?:Help  Q:Quit{Colors.RESET}")
        print(f"{Colors.BLUE}{'-'*75}{Colors.RESET}")

    try:
        while True:
            header()
            if balance < MIN_BET:
                print(f"\n{Colors.RED}💀 Saldo habis! Game over.{Colors.RESET}")
                # Auto-save sebelum exit
                save_game(balance, history, current_bet, stats)
                break

            cmd = smart_input(f"{Colors.WHITE}Pilih perintah {Colors.CYAN}[S/B/H/R/L/V/Q/?]{Colors.WHITE}: {Colors.RESET}", 
                            options=['s', 'b', 'h', 'r', 'l', 'v', 'q', '?', ''], input_type=str)
            
            if cmd is None: break
            elif cmd == "back": continue

            if cmd in ('', 's'):  # Spin
                if balance < current_bet:
                    print(f"{Colors.RED}Saldo tidak cukup!{Colors.RESET}")
                    time.sleep(1.5)
                    continue
                    
                balance -= current_bet
                spins += 1
                print(f"\n{Colors.MAGENTA}Memutar dengan taruhan {format_large_number(current_bet)}...{Colors.RESET}")
                animate_spin(0.9)
                
                result = spin_reels()
                colored_result = [colored_symbol(sym) for sym in result]
                print(Colors.CYAN + "[ " + Colors.RESET + " | ".join(colored_result) + Colors.CYAN + " ]" + Colors.RESET)
                
                payout, note = evaluate(result, current_bet)
                balance += payout
                history.append({"bet": current_bet, "result": " ".join(result), "payout": payout, "note": note})
                
                # Update statistics
                stats = update_stats(stats, current_bet, payout)
                
                print(f"Hasil: {note}")
                payout_color = Colors.GREEN if payout > 0 else Colors.RED
                print(f"Payout: {payout_color}{format_large_number(payout)}{Colors.RESET}")
                
                saldo_color = Colors.GREEN if payout > current_bet else Colors.YELLOW if payout > 0 else Colors.RED
                print(f"Saldo sekarang: {saldo_color}{format_large_number(balance)}{Colors.RESET}")

                # Auto-save setelah spin penting (menang besar atau kalah banyak)
                if abs(payout - current_bet) > 100:
                    if save_game(balance, history, current_bet, stats):
                        print(f"{Colors.GREEN}✓ Auto-saved{Colors.RESET}")

                if balance > highscore:
                    highscore = balance
                    write_highscore(highscore)
                    print(f"{Colors.GOLD}{Colors.BOLD}🎉 REKOR BARU!{Colors.RESET}")

                input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.RESET}")

            elif cmd == 'b':  # Quick Bet Menu
                new_bet = quick_bet_interface(balance, current_bet)
                if new_bet is not None and new_bet != current_bet:
                    current_bet = new_bet
                    # Auto-save setelah ganti taruhan
                    save_game(balance, history, current_bet, stats)

            elif cmd == 'h':  # History
                print(f"\n{Colors.CYAN}{Colors.BOLD}-- Riwayat Spin --{Colors.RESET}")
                if not history: print(f"{Colors.YELLOW}Belum ada spin.{Colors.RESET}")
                else:
                    for i, h in enumerate(reversed(history[-10:]), 1):
                        color = Colors.GREEN if h['payout'] > 0 else Colors.RED
                        result_colored = " ".join([colored_symbol(sym) for sym in h['result'].split()])
                        print(f"{Colors.WHITE}{i:2d}. Bet {format_large_number(h['bet']):>6} -> {result_colored} | {color}Payout {format_large_number(h['payout']):>6}{Colors.WHITE} {h['note']}{Colors.RESET}")
                input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.RESET}")

            elif cmd == 'r':  # Reset
                if smart_input(f"{Colors.RED}Reset saldo ke {START_BALANCE}? (y/N): {Colors.RESET}", options=['y', 'n', '']) == 'y':
                    balance, current_bet, history = START_BALANCE, MIN_BET, []
                    stats = init_stats()
                    delete_save_file()
                    print(f"{Colors.GREEN}✓ Game direset & save file dihapus{Colors.RESET}")
                    time.sleep(1.5)

            elif cmd == 'l':  # Save Game
                if save_game(balance, history, current_bet, stats):
                    print(f"{Colors.GREEN}✓ Game berhasil disimpan!{Colors.RESET}")
                else:
                    print(f"{Colors.RED}✗ Gagal menyimpan game{Colors.RESET}")
                time.sleep(1.5)

            elif cmd == 'v':  # Statistics
                show_stats(stats)
                input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.RESET}")

            elif cmd == '?': 
                show_detailed_help(None)  # Panggil help system baru

    except KeyboardInterrupt: 
        print(f"\n{Colors.YELLOW}Auto-saving sebelum keluar...{Colors.RESET}")
        save_game(balance, history, current_bet, stats)
        print(f"{Colors.YELLOW}Dihentikan oleh pengguna.{Colors.RESET}")
    except Exception as e: 
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
    finally:
        # Final save sebelum exit
        save_game(balance, history, current_bet, stats)
        
        profit_loss = balance - START_BALANCE
        pl_color = Colors.GREEN if profit_loss > 0 else Colors.RED if profit_loss < 0 else Colors.YELLOW
        print(f"\n{Colors.CYAN}{Colors.BOLD}🎰 RINGKASAN:{Colors.RESET}")
        print(f"{Colors.WHITE}Total spin: {Colors.YELLOW}{stats['total_spins']}{Colors.RESET}")
        print(f"{Colors.WHITE}Saldo akhir: {Colors.GREEN if balance > START_BALANCE else Colors.YELLOW if balance == START_BALANCE else Colors.RED}{format_large_number(balance)} {pl_color}({'+' if profit_loss > 0 else ''}{format_large_number(profit_loss)}){Colors.RESET}")
        print(f"{Colors.WHITE}Highscore: {Colors.GOLD}{format_large_number(read_highscore())}{Colors.RESET}")
        print(f"{Colors.GREEN}Progress otomatis disimpan!{Colors.RESET}")
        print(f"{Colors.GREEN}Terima kasih sudah bermain! 🎰{Colors.RESET}")
        print(f"{Colors.CYAN}DeepSeek Produk Cina Lebih Bagus 🥶{Colors.RESET}")

if __name__ == "__main__":
    main()
