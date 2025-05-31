# CryptoCrack

A fully-featured, Linux terminal-inspired hacking simulation game written in Python. Hack into a procedurally generated network of NPC computers, collect bitcoin, buy exploits, and compete with live NPC hackers in a dynamic world!

---

**Created by christhemadman94**

---

## Features

- **Linux-like Terminal**: Use familiar commands (`ls`, `cd`, `nmap`, `ssh`, `cat`, `touch`, `echo`, `whoami`, etc.)
- **In-Game Network**: 1000+ NPC computers, each with unique IPs, open ports, services, and vulnerabilities
- **Hacking Mechanics**: Scan, exploit, and hack NPCs using purchased scripts
- **Bitcoin Economy**: Find and steal `bitcoin.btc` files hidden in NPC file systems, use BTC to buy new exploits
- **Live NPC Hackers**: Compete against AI hackers who attack the network and chat in IRC
- **IRC Channel**: Chat with NPC hackers in a simulated IRC, with dynamic, persona-driven responses
- **Player Progression**: Gain XP, level up, earn skill points, and unlock new abilities
- **Achievements & Missions**: Complete missions and earn achievements for hacking milestones
- **Botnet Management**: Build your own botnet by hacking NPCs
- **Defense & Trace Risk**: Upgrade your firewall/antivirus, manage your trace risk, and defend your home system
- **Save/Load**: Save and resume your progress at any time
- **Black Market, Phishing, DDoS (stubs)**: Planned features for future expansion

## Getting Started

1. **Requirements**: Python 3.7+
2. **Run the Game**:
   ```sh
   python start.py
   ```
3. **Type `help` in the game for a list of commands.**

## Example Commands

- `nmap <ip>` — Scan an NPC for open ports
- `hack <ip> <port>` — Exploit a vulnerable service (if you own the right script)
- `ssh <ip>` — Connect to a hacked NPC's shell
- `find bitcoin.btc` — Locate bitcoin files across the network
- `market` — Buy new exploits with your BTC
- `irc` — Chat with NPC hackers
- `status` — View your stats, skills, and achievements
- `save` / `load` — Save or load your game

## In Game

```
hacker@game:/home/hacker$ nmap 192.168.1.10
192.168.1.10:22 open (ssh)
192.168.1.10:80 open (http)
hacker@game:/home/hacker$ hack 192.168.1.10 22
Brute-forcing SSH password on 192.168.1.10:22... Success!
hacker@game:/home/hacker$ ssh 192.168.1.10
Connected to 192.168.1.10. Type 'exit' to disconnect.
npc@192.168.1.10:/home/npc$ ls
bitcoin.btc
npc@192.168.1.10:/home/npc$ check bitcoin.btc
bitcoin.btc value: 7
npc@192.168.1.10:/home/npc$ take bitcoin.btc
Took 7 BTC from /home/npc/bitcoin.btc. Your total: 7 BTC.
```

## Roadmap
- Black market with dynamic pricing and zero-days
- Phishing/social engineering minigames
- DDoS attacks using your botnet
- More advanced NPC AI and world events
- More missions, achievements, and dynamic world events
- Improved NPC IRC chat and player interaction

## License
MIT License

---

*CryptoCrack is a simulation game for educational and entertainment purposes only. Do not use for real hacking.*
