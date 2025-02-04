import os
import httpx
import asyncio

async def check_url(client, url, word):
    """Check a URL with a given word from the wordlist."""
    full_url = f"{url}/{word}"
    try:
        response = await client.get(full_url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Found: {full_url} (Status: 200 OK)")
            return {"url": full_url, "code": "200"}
        elif response.status_code == 403:
            print(f"[-] Forbidden: {full_url} (Status: 403 Forbidden)")
            return {"url": full_url, "code": "403"}
        elif response.status_code in [301, 302]:
            print(f"[+] Redirected: {full_url} (Status: {response.status_code}) ({response.headers.location})")
            return {"url": full_url, "code": "301 or 302"}
    except httpx.RequestError as e:
        print(f"[-] Error accessing {full_url}: {e}")
    except Exception as e:
        print(f"[-] Error: {full_url}: {e} - {response.headers}")

async def start_scan(url, wordlist, max_concurrent=2, delay=0.2):
    """Scan a URL using the wordlist for available resources."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resources_found = []
    async with httpx.AsyncClient(headers=headers, timeout=2, follow_redirects=True) as client:
        semaphore = asyncio.Semaphore(max_concurrent)

        async def limited_task(word):
            async with semaphore:
                await asyncio.sleep(delay)
                result = await check_url(client, url, word)
                if result is not None:
                    resources_found.append(result)

        tasks = [asyncio.create_task(limited_task(word)) for word in wordlist]
        await asyncio.gather(*tasks)
        return resources_found

def load_wordlist(file_path):
    """Load wordlist from file."""
    if not os.path.exists(file_path):
        print(f"Error: Wordlist file {file_path} not found.")
        return []
    
    with open(file_path, 'r') as file:
        wordlist = file.read().splitlines()
    return wordlist

async def path_scan(domain = "www.example.com"):
    print("Starting path scan")
    print("*" *  20)

    target_url = domain
    
    wordlist_path = "wordlist.txt" 
    wordlist = load_wordlist(wordlist_path)

    print("Result:")
    result = await start_scan(target_url, wordlist)

if __name__ == "__main__":
    asyncio.run(path_scan())
