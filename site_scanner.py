from path import path_scan
from port import host_scan
import sys
import asyncio

async def main():
    """ Execute a port and available directory scanning on a website or host."""
    if len(sys.argv) < 4:
        print("Usage: ./site_scanner.py <IP address or domain> <start port> <end port> [-d] (to start directory scan)")
        print("Example: ./site_scanner.py http://www.example.com 1 65535 -d")
        return

    domain   = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port   = int(sys.argv[3])
    dir_scan_enabled = "-d" in sys.argv

    await host_scan(domain, start_port, end_port)
    print("-" * 30)

    if dir_scan_enabled:
        await path_scan(domain)
        print()
        print("-" * 30)

    print("Scan complete")

if __name__ == "__main__":
    asyncio.run(main())