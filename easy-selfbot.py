import os
import asyncio
import aiohttp

# ASCII umění pro Pr0xyArmy
ascii_art = """
  _____            ___                                                       
 |  __ \\          / _ \\                     /\\                               
 | |__) |  _ __  | | | | __  __  _   _     /  \\     _ __   _ __ ___    _   _ 
 |  ___/  | '__| | | | | \\ \\/ / | | | |   / /\\ \\   | '__| | '_ ` _ \\  | | | |
 | |      | |    | |_| |  >  <  | |_| |  / ____ \\  | |    | | | | | | | |_| |
 |_|      |_|     \\___/  /_/\\_\\  \\__, | /_/    \\_\\ |_|    |_| |_| |_|  \\__, |
                                  __/ |                                 __/ |
                                 |___/                                 |___/  
"""

# První příkaz pro vyčištění konzole (cls na Windows, clear na Linux/Mac)
os.system('cls' if os.name == 'nt' else 'clear')

print(ascii_art)

token = input("Zadejte Discord user token: ")
message = input("Zadejte zprávu: ")

# Přidání nového vstupu pro počet opakování
repeat_count = int(input("Zadejte počet opakování pro odeslání zprávy: "))

# Druhý příkaz pro vyčištění konzole před spuštěním hlavní části
os.system('cls' if os.name == 'nt' else 'clear')

sem = asyncio.Semaphore(5)  # Maximální počet současných požadavků (nastavte podle potřeby)

async def get_channels():
    async with aiohttp.ClientSession(headers={"Authorization": token}) as session:
        async with session.get("https://discord.com/api/v10/users/@me/channels") as response:
            channels = await response.json()
            return channels

async def send_message(channel_id, message):
    async with sem:
        async with aiohttp.ClientSession(headers={"Authorization": token}) as session:
            payload = {"content": message}
            async with session.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", json=payload) as response:
                if response.status == 200:
                    print(f"Zpráva byla úspěšně odeslána do kanálu s ID {channel_id}")
                else:
                    print(f"Nepodařilo se odeslat zprávu do kanálu s ID {channel_id}")

async def main():
    channels = await get_channels()

    choice = input("Chcete poslat zprávu do všech dostupných kanálů? (ano/ne): ").lower()

    tasks = []
    if choice == "ano":
        for channel in channels:
            channel_id = channel["id"]
            tasks.extend([send_message(channel_id, message) for _ in range(repeat_count)])
    elif choice == "ne":
        selected_channels = input("Zadejte ID kanálů oddělených mezerou: ").split()
        tasks.extend([send_message(channel_id, message) for channel_id in selected_channels for _ in range(repeat_count)])
    else:
        print("Neplatná volba. Program skončí.")

    await asyncio.gather(*tasks)

    # Čekání na stisknutí klávesy před výstupem
    input("\nPro pokračování stiskněte Enter...")

    # Závěrečný výstup
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Made by script669 & extr0nus 'Personal Pr0xy'")
    print("-"*45)
    print("https://dsc.gg/Pr0xyArmy")
    print("discord.gg/Pr0xyArmyFans")
    print("https://dsc.gg/green-harvest")
    print("-"*45)

    # Čekání na stisknutí klávesy před výstupem
    input("\nPro konec stiskněte Enter...")

if __name__ == '__main__':
    asyncio.run(main())
