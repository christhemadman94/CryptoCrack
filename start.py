# CryptoCrack - Terminal Hacking Simulation Game
# Created by christhemadman94

# This is the main entry point for the CryptoCrack hacking simulation game.
# The game simulates a network of NPC computers, hacking mechanics, bitcoin economy, live NPC hackers, and player progression.
# For more information, see the README.md file.
#
# Project homepage: https://github.com/christhemadman94/cryptocrack

import sys
import random
import os
import threading
import time

# -----------------------------
# In-game network setup
# -----------------------------
class NPCComputer:
    """
    Represents an NPC computer in the simulated network.
    Each computer has an IP, running services, vulnerabilities, and a simulated file system.
    """
    def __init__(self, ip, services, vulnerabilities=None, files=None):
        self.ip = ip  # IP address of the NPC
        self.services = services  # {port: service_name}
        self.hacked = False  # Whether this NPC has been hacked
        self.exploited_services = set()  # Ports that have been exploited
        self.vulnerabilities = vulnerabilities or {}  # {port: vuln_type}
        self.files = files or {}  # Simulated file system: {filepath: content}

    def __str__(self):
        # String representation for listing NPCs
        return f"{self.ip} (services: {', '.join([f'{p}/{s}' for p, s in self.services.items()])})"

# Example network with two pre-defined NPCs
network = [
    NPCComputer('192.168.1.10', {22: 'ssh', 80: 'http'}, {22: 'weak_password', 80: 'http_rce'},
                {'/home/npc/bitcoin.btc': str(random.randint(1, 10))}),
    NPCComputer('192.168.1.20', {21: 'ftp', 8080: 'http-alt'}, {21: 'ftp_brute', 8080: 'http_upload'},
                {'/var/tmp/bitcoin.btc': str(random.randint(5, 20))}),
]
# Add 1000 more random NPCs to the network
for i in range(1000):
    ip = f'10.0.{i // 256}.{i % 256}'
    services = {}
    vulnerabilities = {}
    files = {}
    # Randomly assign services and vulnerabilities to each NPC
    if random.random() < 0.5:
        services[22] = 'ssh'
        vulnerabilities[22] = random.choice(['weak_password', None])
    if random.random() < 0.5:
        services[80] = 'http'
        vulnerabilities[80] = random.choice(['http_rce', None])
    if random.random() < 0.3:
        services[21] = 'ftp'
        vulnerabilities[21] = random.choice(['ftp_brute', None])
    if random.random() < 0.2:
        services[8080] = 'http-alt'
        vulnerabilities[8080] = random.choice(['http_upload', None])
    # Randomly hide bitcoin.btc in a random directory on some NPCs
    if services and random.random() < 0.2:
        btc_value = str(random.randint(1, 25))
        btc_dir = random.choice(['/home/npc', '/var/tmp', '/tmp', '/root', '/etc'])
        files[f'{btc_dir}/bitcoin.btc'] = btc_value
    if services:
        network.append(NPCComputer(ip, services, vulnerabilities, files))

# -----------------------------
# Player state and progression
# -----------------------------
current_dir = '/home/hacker'  # Player's current working directory
player_bitcoin = 0  # Player's bitcoin balance
player_xp = 0  # Player's experience points
player_level = 1  # Player's level
player_achievements = set()  # Set of achievement names
player_alias = "player"  # Player's alias/handle
player_skill_points = 0  # Unspent skill points
player_skills = {"brute_force": 0, "stealth": 0, "social": 0}  # Player's skill levels
player_home_hacked = False  # Whether the player's home system has been hacked
player_files = {"/home/hacker/readme.txt": "Welcome to your home system!"}  # Player's files
player_defense = {"firewall": 1, "antivirus": 1}  # Player's defense levels
player_trace_risk = 0  # Trace risk percentage
player_botnet = set()  # Set of IPs in player's botnet
player_news = []  # News/event log
player_missions = [
    {"desc": "Hack your first NPC.", "done": False},
    {"desc": "Steal 10 BTC.", "done": False},
    {"desc": "Buy an exploit from the market.", "done": False},
]

def print_prompt():
    print(f"hacker@game:{current_dir}$ ", end='')

def handle_ls(args):
    # Show files in the current directory for the local shell
    if current_dir == '/home/hacker':
        print("bin  home  etc  var  tmp")
    else:
        # Simulate subdirectories and files (for demo, just show subdirs)
        print("bin  home  etc  var  tmp")

def handle_cd(args):
    global current_dir
    if not args:
        current_dir = '/home/hacker'
        return
    path = args[0]
    # Only allow cd into valid directories
    valid_dirs = ['/home/hacker', '/bin', '/home', '/etc', '/var', '/tmp']
    if path in valid_dirs:
        current_dir = path
    else:
        print(f"cd: {path}: No such file or directory")

def handle_nmap(args):
    if not args:
        print("Usage: nmap <ip>")
        return
    ip = args[0]
    for npc in network:
        if npc.ip == ip:
            for port, service in npc.services.items():
                print(f"{ip}:{port} open ({service})")
            return
    print(f"Host {ip} not found.")

def handle_cat(args):
    if not args:
        print("Usage: cat <file>")
        return
    filename = args[0]
    if filename == 'readme.txt':
        print("Welcome to the hacking game! Your mission: hack all NPCs.")
    else:
        print(f"cat: {filename}: No such file or directory")

def handle_touch(args):
    if not args:
        print("Usage: touch <file>")
        return
    print(f"Created file: {args[0]}")

def handle_echo(args):
    print(' '.join(args))

def handle_whoami(args):
    print("hacker")

def remote_shell(npc):
    print(f"Connected to {npc.ip}. Type 'exit' to disconnect.")
    remote_dir = '/home/npc'
    while True:
        cmd = input(f"npc@{npc.ip}:{remote_dir}$ ").strip()
        if cmd == 'exit':
            print(f"Disconnected from {npc.ip}.")
            break
        elif cmd == 'ls':
            files = [os.path.basename(f) for f in npc.files if f.startswith(remote_dir)]
            print('  '.join(files) if files else "bin  home  etc  var  tmp")
        elif cmd.startswith('cd'):
            parts = cmd.split()
            if len(parts) > 1 and parts[1].startswith('/'):
                remote_dir = parts[1]
            else:
                remote_dir = '/home/npc'
        elif cmd.startswith('cat'):
            parts = cmd.split()
            if len(parts) > 1:
                file_path = parts[1] if parts[1].startswith('/') else f'{remote_dir}/{parts[1]}'
                if file_path in npc.files:
                    print(npc.files[file_path])
                else:
                    print(f"cat: {parts[1]}: No such file or directory")
            else:
                print("Usage: cat <file>")
        elif cmd.startswith('check'):
            parts = cmd.split()
            if len(parts) > 1 and parts[1] == 'bitcoin.btc':
                for path, value in npc.files.items():
                    if path.endswith('bitcoin.btc'):
                        print(f"bitcoin.btc value: {value}")
                        break
                else:
                    print("bitcoin.btc not found.")
            else:
                print("Usage: check bitcoin.btc")
        elif cmd.startswith('take'):
            parts = cmd.split()
            if len(parts) > 1 and parts[1] == 'bitcoin.btc':
                for path in list(npc.files.keys()):
                    if path.endswith('bitcoin.btc'):
                        value = int(npc.files[path])
                        global player_bitcoin
                        player_bitcoin += value
                        print(f"Took {value} BTC from {path}. Your total: {player_bitcoin} BTC.")
                        del npc.files[path]
                        break
                else:
                    print("bitcoin.btc not found.")
            else:
                print("Usage: take bitcoin.btc")
        elif cmd == 'whoami':
            print("npc")
        else:
            print(f"Command not found: {cmd}")

def handle_ssh(args):
    if not args:
        print("Usage: ssh <ip>")
        return
    ip = args[0]
    for npc in network:
        if npc.ip == ip:
            if 22 in npc.services:
                if not npc.hacked:
                    print(f"Trying to hack {ip}... Success!")
                    npc.hacked = True
                else:
                    print(f"Already hacked into {ip}.")
                remote_shell(npc)
            else:
                print(f"SSH not available on {ip}.")
            return
    print(f"Host {ip} not found.")

# -----------------------------
# Script marketplace setup
# -----------------------------
class ExploitScript:
    """
    Represents an exploit script available in the marketplace.
    Scripts have a name, target service, vulnerability type, and a price in BTC.
    """
    def __init__(self, name, target_service, vuln_type, price):
        self.name = name
        self.target_service = target_service
        self.vuln_type = vuln_type
        self.price = price
    def __str__(self):
        return f"{self.name} (for {self.target_service}/{self.vuln_type}) - {self.price} BTC"

# Marketplace with predefined exploit scripts
marketplace = [
    ExploitScript('SSH Brute Forcer', 'ssh', 'weak_password', 100),
    ExploitScript('HTTP RCE Exploit', 'http', 'http_rce', 150),
    ExploitScript('FTP Brute Forcer', 'ftp', 'ftp_brute', 80),
    ExploitScript('Webshell Uploader', 'http-alt', 'http_upload', 120),
]

player_scripts = set()  # Set of exploit scripts owned by the player

def award_xp(amount):
    global player_xp, player_level, player_skill_points
    player_xp += amount
    if player_xp >= player_level * 100:
        player_xp -= player_level * 100
        player_level += 1
        player_skill_points += 1
        print(f"[LEVEL UP] You are now level {player_level}! Skill point awarded.")

def check_achievements():
    if "first_hack" not in player_achievements and any(npc.hacked for npc in network):
        player_achievements.add("first_hack")
        print("[ACHIEVEMENT] First hack!")
    if "10btc" not in player_achievements and player_bitcoin >= 10:
        player_achievements.add("10btc")
        print("[ACHIEVEMENT] 10 BTC collected!")
    if "bought_exploit" not in player_achievements and any(script in player_scripts for script in [s.vuln_type for s in marketplace]):
        player_achievements.add("bought_exploit")
        print("[ACHIEVEMENT] First exploit purchased!")

def handle_status(args):
    print(f"Alias: {player_alias}")
    print(f"Level: {player_level}  XP: {player_xp}/ {player_level*100}")
    print(f"Skill points: {player_skill_points}")
    print(f"Skills: {player_skills}")
    print(f"BTC: {player_bitcoin}")
    print(f"Achievements: {', '.join(player_achievements) if player_achievements else 'None'}")
    print(f"Missions:")
    for m in player_missions:
        print(f" - {'[X]' if m['done'] else '[ ]'} {m['desc']}")
    print(f"Trace risk: {player_trace_risk}%")
    print(f"Botnet size: {len(player_botnet)}")
    print(f"Defense: {player_defense}")
    print(f"Home hacked: {'YES' if player_home_hacked else 'NO'}")

def handle_market(args):
    global player_bitcoin
    print(f"Your balance: {player_bitcoin} BTC")
    print("Available scripts:")
    for idx, script in enumerate(marketplace):
        owned = '(owned)' if script.vuln_type in player_scripts else ''
        print(f"{idx+1}. {script} {owned}")
    print("Type 'buy <number>' to purchase a script.")
    while True:
        cmd = input("market> ").strip()
        if cmd == 'exit':
            break
        elif cmd.startswith('buy'):
            parts = cmd.split()
            if len(parts) < 2 or not parts[1].isdigit():
                print("Usage: buy <number>")
                continue
            idx = int(parts[1]) - 1
            if idx < 0 or idx >= len(marketplace):
                print("Invalid script number.")
                continue
            script = marketplace[idx]
            if script.vuln_type in player_scripts:
                print("You already own this script.")
                continue
            if player_bitcoin < script.price:
                print("Not enough bitcoin.")
                continue
            player_bitcoin -= script.price
            player_scripts.add(script.vuln_type)
            print(f"Purchased {script.name}!")
        else:
            print("Unknown command. Type 'exit' to leave the market.")

def handle_hack(args):
    if len(args) < 2:
        print("Usage: hack <ip> <port>")
        return
    ip, port_str = args[0], args[1]
    try:
        port = int(port_str)
    except ValueError:
        print("Port must be a number.")
        return
    for npc in network:
        if npc.ip == ip:
            if port in npc.services:
                if port in npc.exploited_services:
                    print(f"Service {port}/{npc.services[port]} already exploited on {ip}.")
                    return
                vuln = npc.vulnerabilities.get(port)
                if vuln in player_scripts:
                    if vuln == 'weak_password':
                        print(f"Brute-forcing SSH password on {ip}:{port}... Success!")
                    elif vuln == 'http_rce':
                        print(f"Exploiting HTTP RCE on {ip}:{port}... Shell access granted!")
                    elif vuln == 'ftp_brute':
                        print(f"Brute-forcing FTP login on {ip}:{port}... Success!")
                    elif vuln == 'http_upload':
                        print(f"Uploading webshell to {ip}:{port}... Success!")
                    npc.exploited_services.add(port)
                    npc.hacked = True
                elif vuln:
                    print(f"You need to buy an exploit script for {npc.services[port]} ({vuln}) from the market.")
                else:
                    print(f"No known exploit for {npc.services[port]} on {ip}:{port}.")
                return
            else:
                print(f"Port {port} not open on {ip}.")
                return
    print(f"Host {ip} not found.")

def handle_online(args):
    print("Online NPCs:")
    for npc in network:
        print(npc)

def handle_clear(args):
    # Clear the terminal screen (cross-platform)
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_help(args):
    print("Available commands: ls, cd, nmap, ssh, hack, cat, touch, echo, whoami, online, market, take, check, clear, find, irc, status, save, load, skills, news, missions, botnet, defend, trace, home, avatar, blackmarket, phish, log, ddos, help, exit")

def handle_find(args):
    if not args:
        print("Usage: find <filename>")
        return
    filename = args[0]
    found = False
    # Search local (player) file system (demo: only readme.txt exists)
    if filename == 'readme.txt':
        print("/home/hacker/readme.txt")
        found = True
    # Search all NPCs' files
    for npc in network:
        for path in npc.files:
            if os.path.basename(path) == filename:
                print(f"{npc.ip}:{path}")
                found = True
    if not found:
        print(f"{filename} not found.")

# -----------------------------
# Live NPC hacker logic
# -----------------------------
class NPCHacker(threading.Thread):
    """
    Represents an NPC hacker that can hack player or NPC systems.
    Runs in a separate thread and performs hacks at random intervals.
    """
    def __init__(self, name, interval=10):
        super().__init__(daemon=True)
        self.name = name
        self.interval = interval
        self.running = True
    def run(self):
        while self.running:
            time.sleep(self.interval)
            # Randomly pick a player/NPC to attack
            target = random.choice(network)
            if not target.hacked:
                # Simulate attack
                port = random.choice(list(target.services.keys()))
                vuln = target.vulnerabilities.get(port)
                if vuln:
                    target.hacked = True
                    print(f"\n[ALERT] {self.name} hacked {target.ip} on port {port} using {vuln}! Type 'online' to check status.")
    def stop(self):
        self.running = False

# Start a few live NPC hackers
npc_hackers = [NPCHacker(f"NPC-Hacker-{i+1}", interval=random.randint(8, 20)) for i in range(3)]
for hacker in npc_hackers:
    hacker.start()

# -----------------------------
# IRC chat setup
# -----------------------------
irc_messages = []
irc_nicknames = [f"NPC-Hacker-{i+1}" for i in range(3)] + ["player"]

def handle_irc(args):
    print("--- IRC Channel: #hackers ---")
    print("Type your message and press Enter. Type '/exit' to leave the chat.")
    # Print last 10 messages
    for msg in irc_messages[-10:]:
        print(msg)
    player_reputation = 0
    npc_personas = [
        {"name": n, "aggressive": random.random() < 0.5, "braggy": random.random() < 0.5, "friendly": random.random() < 0.5}
        for n in irc_nicknames[:-1]
    ]
    def npc_reply(player_msg, rep):
        responses = []
        for persona in npc_personas:
            npc = persona["name"]
            # If player brags, NPCs may challenge or mock
            if any(word in player_msg.lower() for word in ["pwned", "hacked", "bitcoin", "rich", "best", "king"]):
                if persona["aggressive"]:
                    responses.append(f"<{npc}> You think you're good? Let's see you hack my box!")
                elif persona["braggy"]:
                    responses.append(f"<{npc}> That's nothing, I just took over 10 servers today!")
                elif persona["friendly"]:
                    responses.append(f"<{npc}> Nice job, {irc_nicknames[-1]}! Maybe we can team up.")
            # If player asks for help
            elif any(word in player_msg.lower() for word in ["help", "how", "tip", "advice"]):
                if persona["friendly"]:
                    responses.append(f"<{npc}> Try scanning with nmap, then use the right exploit. Good luck!")
                elif persona["aggressive"]:
                    responses.append(f"<{npc}> Figure it out yourself, newbie.")
            # If player insults or taunts
            elif any(word in player_msg.lower() for word in ["noob", "loser", "slow", "bad"]):
                if persona["aggressive"]:
                    responses.append(f"<{npc}> Watch your mouth or I'll DDoS you!")
                elif persona["braggy"]:
                    responses.append(f"<{npc}> You're just jealous of my skills.")
            # If player is humble or asks about others
            elif any(word in player_msg.lower() for word in ["anyone here", "hi", "hello", "who", "nice"]):
                if persona["friendly"]:
                    responses.append(f"<{npc}> Hey {irc_nicknames[-1]}, welcome to #hackers!")
                elif persona["braggy"]:
                    responses.append(f"<{npc}> I'm the best hacker here, obviously.")
            # Random chance for NPCs to brag or challenge
            elif random.random() < 0.1:
                if persona["braggy"]:
                    responses.append(f"<{npc}> I just found a new 0day!")
                elif persona["aggressive"]:
                    responses.append(f"<{npc}> Anyone want a hacking duel?")
        return responses
    while True:
        # Simulate NPC hackers occasionally sending messages
        if random.random() < 0.15:
            persona = random.choice(npc_personas)
            npc = persona["name"]
            if persona["braggy"] and random.random() < 0.5:
                msg = random.choice([
                    "I just pwned another box!",
                    "No one can stop me!",
                    "My exploits are the best.",
                    "Who's next to get hacked?",
                    "I'm the king of 0days!",
                    "You call that security? LOL!",
                    "I have more bitcoin than all of you!",
                    "Try to catch me if you can!"
                ])
            elif persona["aggressive"]:
                msg = random.choice([
                    "You all are too slow for me!",
                    "I bet none of you can hack my server!",
                    "Step up your game, script kiddies!"
                ])
            else:
                msg = random.choice([
                    "Anyone want to team up for a big score?",
                    "Hacking is more fun with friends!",
                    "Stay safe out there, hackers."
                ])
            irc_messages.append(f"<{npc}> {msg}")
            print(f"<{npc}> {msg}")
        user_input = input("[IRC] ").strip()
        if user_input == '/exit':
            print("Left IRC channel.")
            break
        if user_input:
            irc_messages.append(f"<player> {user_input}")
            print(f"<player> {user_input}")
            # NPCs react to player message
            npc_responses = npc_reply(user_input, player_reputation)
            for resp in npc_responses:
                irc_messages.append(resp)
                print(resp)

def handle_save(args):
    import pickle
    with open('savegame.pkl', 'wb') as f:
        pickle.dump({
            'player_xp': player_xp,
            'player_level': player_level,
            'player_skill_points': player_skill_points,
            'player_skills': player_skills,
            'player_bitcoin': player_bitcoin,
            'player_achievements': player_achievements,
            'player_alias': player_alias,
            'player_files': player_files,
            'player_defense': player_defense,
            'player_trace_risk': player_trace_risk,
            'player_botnet': player_botnet,
            'player_news': player_news,
            'player_missions': player_missions,
            'network': network,
        }, f)
    print("Game saved.")

def handle_load(args):
    import pickle
    global player_xp, player_level, player_skill_points, player_skills, player_bitcoin, player_achievements, player_alias, player_files, player_defense, player_trace_risk, player_botnet, player_news, player_missions, network
    with open('savegame.pkl', 'rb') as f:
        data = pickle.load(f)
        player_xp = data['player_xp']
        player_level = data['player_level']
        player_skill_points = data['player_skill_points']
        player_skills = data['player_skills']
        player_bitcoin = data['player_bitcoin']
        player_achievements = data['player_achievements']
        player_alias = data['player_alias']
        player_files = data['player_files']
        player_defense = data['player_defense']
        player_trace_risk = data['player_trace_risk']
        player_botnet = data['player_botnet']
        player_news = data['player_news']
        player_missions = data['player_missions']
        network = data['network']
    print("Game loaded.")

def handle_skills(args):
    global player_skill_points
    print(f"Skill points: {player_skill_points}")
    print(f"Current skills: {player_skills}")
    if player_skill_points > 0:
        print("Type 'skills <skill> <amount>' to assign points (brute_force, stealth, social)")
        if len(args) == 2 and args[0] in player_skills and args[1].isdigit():
            amt = int(args[1])
            if amt <= player_skill_points:
                player_skills[args[0]] += amt
                player_skill_points -= amt
                print(f"Assigned {amt} points to {args[0]}.")
            else:
                print("Not enough skill points.")
    else:
        print("No skill points to assign.")

def handle_news(args):
    print("--- News Feed ---")
    for n in player_news[-10:]:
        print(n)
    if not player_news:
        print("No news yet.")

def handle_missions(args):
    print("--- Missions ---")
    for idx, m in enumerate(player_missions):
        print(f"{idx+1}. {'[X]' if m['done'] else '[ ]'} {m['desc']}")

def handle_botnet(args):
    print(f"You control {len(player_botnet)} bots.")
    if player_botnet:
        print("Bots:")
        for ip in player_botnet:
            print(f" - {ip}")
    else:
        print("No bots yet. Hack more NPCs to add to your botnet.")

def handle_defend(args):
    print(f"Your defense: {player_defense}")
    print("Type 'defend <firewall|antivirus> <upgrade>' to upgrade.")
    if len(args) == 2 and args[0] in player_defense and args[1] == 'upgrade':
        cost = 50 * (player_defense[args[0]] + 1)
        global player_bitcoin
        if player_bitcoin >= cost:
            player_bitcoin -= cost
            player_defense[args[0]] += 1
            print(f"Upgraded {args[0]} to level {player_defense[args[0]]}.")
        else:
            print("Not enough BTC.")

def handle_trace(args):
    print(f"Trace risk: {player_trace_risk}%")
    if player_trace_risk > 80:
        print("[WARNING] You are at high risk of being traced!")
    print("Type 'trace clean' to reduce risk (costs 10 BTC)")
    if args and args[0] == 'clean':
        global player_bitcoin
        if player_bitcoin >= 10:
            player_bitcoin -= 10
            player_trace_risk = max(0, player_trace_risk - 50)
            print("Trace risk reduced.")
        else:
            print("Not enough BTC.")

def handle_home(args):
    print("--- Your Home System ---")
    print("Files:")
    for f in player_files:
        print(f" - {f}")
    print(f"Defense: {player_defense}")
    print(f"Home hacked: {'YES' if player_home_hacked else 'NO'}")

def handle_avatar(args):
    global player_alias
    print(f"Your alias: {player_alias}")
    print("Type 'avatar <new_alias>' to change.")
    if args:
        player_alias = args[0]
        print(f"Alias changed to {player_alias}")

def handle_blackmarket(args):
    print("--- Black Market ---")
    print("(Not implemented: would show dynamic pricing, zero-days, etc.)")

def handle_phish(args):
    print("--- Phishing Mini-game ---")
    print("(Not implemented: would simulate phishing/social engineering.)")

def handle_log(args):
    print("--- Event Log ---")
    for n in player_news[-20:]:
        print(n)
    if not player_news:
        print("No events yet.")

def handle_ddos(args):
    print("--- DDoS Mini-game ---")
    print("(Not implemented: would use your botnet to attack targets.)")

def main():
    print("Welcome to CryptoCrack! Type 'help' for commands.")
    try:
        while True:
            print_prompt()
            try:
                cmd = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting game.")
                break
            if not cmd:
                continue
            parts = cmd.split()
            command, args = parts[0], parts[1:]
            if command == 'ls':
                handle_ls(args)
            elif command == 'cd':
                handle_cd(args)
            elif command == 'nmap':
                handle_nmap(args)
            elif command == 'ssh':
                handle_ssh(args)
            elif command == 'cat':
                handle_cat(args)
            elif command == 'touch':
                handle_touch(args)
            elif command == 'echo':
                handle_echo(args)
            elif command == 'whoami':
                handle_whoami(args)
            elif command == 'help':
                handle_help(args)
            elif command == 'exit':
                print("Goodbye!")
                break
            elif command == 'hack':
                handle_hack(args)
            elif command == 'online':
                handle_online(args)
            elif command == 'market':
                handle_market(args)
            elif command == 'clear':
                handle_clear(args)
            elif command == 'find':
                handle_find(args)
            elif command == 'irc':
                handle_irc(args)
            elif command == 'status':
                handle_status(args)
            elif command == 'save':
                handle_save(args)
            elif command == 'load':
                handle_load(args)
            elif command == 'skills':
                handle_skills(args)
            elif command == 'news':
                handle_news(args)
            elif command == 'missions':
                handle_missions(args)
            elif command == 'botnet':
                handle_botnet(args)
            elif command == 'defend':
                handle_defend(args)
            elif command == 'trace':
                handle_trace(args)
            elif command == 'home':
                handle_home(args)
            elif command == 'avatar':
                handle_avatar(args)
            elif command == 'blackmarket':
                handle_blackmarket(args)
            elif command == 'phish':
                handle_phish(args)
            elif command == 'log':
                handle_log(args)
            elif command == 'ddos':
                handle_ddos(args)
            else:
                print(f"Command not found: {command}")
    finally:
        for hacker in npc_hackers:
            hacker.stop()

if __name__ == '__main__':
    main()