# PySiteScanner: A Simple Port and Directory Scanner

PySiteScanner is a lightweight, async Python script that combines **port scanning (like Nmap)** and **directory brute-forcing (like Dirb)** into a single command-line tool. It allows you to scan open ports on a target and discover hidden directories or paths on a web server.

## Features

- 🔍 **Port Scanning**: Detects open ports on a target domain name.
- 🌐 **Directory Scanning**: Finds hidden directories and files on a web server using a wordlist.
- ⚡ **Easy to Use**: A single command to perform both scans at once.

## Installation

```bash
git clone https://github.com/tomy27/PySiteScanner.git
cd PySiteScanner
chmod +x site_scanner.py  # (Optional for Linux/macOS)
```

## Usage

Run the script from the command line:

```bash
python site_scanner.py <domain> <start_port> <end_port> [-d (to enable directory scan, optional)]
```

### Examples

#### Scan ports only

```bash
python site_scanner.py http://www.example.com 1 1000
```

#### Scan ports and perform directory brute-forcing

```bash
python site_scanner.py http://www.example.com 1 1000 -d
```

## How It Works

1. **Port Scanning:**

   - Iterates through the given port range and checks if each port is open.
   - Uses non-blocking sockets for faster scanning.

2. **Directory Scanning:** (Only if `-d` is specified)

   - Reads a wordlist file and appends each word as a possible directory to scan.
   - Sends HTTP requests to check for valid directories.
   - Feel free to add more words to the wordlist.

## Requirements

- Python 3.x
- Internet connection (for scanning remote targets)

## Disclaimer

This tool is for **educational and security testing purposes only**. Use it **only on systems you have permission to test**. The author is not responsible for misuse.

This tool is still **under development, use it with caution!**

## License

MIT License - Feel free to modify and distribute.

---

**Happy Scanning**🚀 
