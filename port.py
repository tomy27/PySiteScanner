import socket
import asyncio


async def get_ip_address(host) -> str:
    socket.setdefaulttimeout(10)
    return socket.gethostbyname(host)


async def detect_protocol(reader, writer, ip, port) -> str:
    """Detect the service on a port based on the banner or HTTP response"""
    # EXPERIMENTAL ONLY
    # TODO
    try:
        # Try to read the banner
        banner = await asyncio.wait_for(reader.read(1024), timeout=2)
        decoded_banner = banner.decode(errors='ignore').strip().lower()
        print("ddd")
        print(f"decoded_banner: {decoded_banner}")

        # Check banner content
        if "ssh-" in decoded_banner:
            return "SSH"

    except asyncio.TimeoutError:
        # If no banner, try sending an HTTP request
        http_request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
        writer.write(http_request.encode())
        await writer.drain()
        try:
            http_response = await asyncio.wait_for(reader.read(1024), timeout=2)
            print(http_response)
            decoded_response = http_response.decode(errors='ignore').strip().lower()
            if decoded_response.startswith("http/"):
                return "HTTP"
        except asyncio.TimeoutError:
            return "Unknown"
        except Exception:
            return "Unknown"

    except Exception as e:
        print(f"Error in detect_protocol on {port}: {e}")
    return "Unknown"
 

async def tcp_scan(ip, port) -> dict | None:
    """Attempts an async TCP connection to check if a port is open"""

    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=5) # to apply a timeout
        port_report = {"port": port, "protocol": None}

        # Determine the service (like ssh, http etc.)
        # TODO
        # service = await detect_protocol(reader, writer, ip, port)
        service = socket.getservbyport(port, "tcp")
        port_report["protocol"] = service

        print(f"{port}\\tcp    open    {service}")

        writer.close()
        await writer.wait_closed()
        return port_report
    except asyncio.TimeoutError:
        # print(f"Timeout (No response) on port: {port}")
        return None
    except Exception as e:
        print(f"Error during tcp scan: {e}")
        return None
        


async def host_scan(host, start_port, end_port, max_concurrent=5, delay=0.5):
    """ Starts a TCP scan on a given IP address """
    # TODO make max_concurrent and delay changable from command line upon start
    """
    Example settings:
        Fast scan (for internal networks) -> max_concurrent=100, delay=0
        Polite scan (for websites, firewalls) -> max_concurrent=5, delay=0.5
        Stealthy scan (to avoid detection) -> max_concurrent=2, delay=1.0
        Human-like scan -> max_concurrent=1, delay=round(random.uniform(0.5, 4),2)
    """

    print(f"Starting TCP port scan on host {host}")
    print("*" *  20)

    if host.startswith("http://"):
        host = host.replace("http://", "")
    elif host.startswith("https://"):
        host = host.replace("https://", "")

    ip = await get_ip_address(host)
    print(f"IP adress: {ip}")
    
    open_ports = []
    # If concurrency limit is needed
    if max_concurrent > 0:
        semaphore = asyncio.Semaphore(max_concurrent)

        async def limited_scan(port):
            async with semaphore:
                await asyncio.sleep(delay)
                result = await tcp_scan(ip, port)
                if result is not None:
                    open_ports.append(result)

        scan_function = limited_scan
    else:
        async def scan_function(port):
            result = await tcp_scan(ip, port)
            if result is not None:
                open_ports.append(result)

    tasks = [asyncio.create_task(scan_function(port)) for port in range(start_port, end_port + 1)]
    await asyncio.gather(*tasks, return_exceptions=True)

    print()
    if not open_ports:
        print("No open port found!")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print('Usage: ./portscanner.py <IP address> <start port> <end port>')
        print('Example: ./portscanner.py 192.168.1.10 1 65535\n')

    elif len(sys.argv) >= 4:
        host   = sys.argv[1]
        start_port = int(sys.argv[2])
        end_port   = int(sys.argv[3])

    if len(sys.argv) == 4:
        asyncio.run(host_scan(host, start_port, end_port))
