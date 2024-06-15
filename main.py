import hashlib
import os
import pandas as pd
import zipfile
from pathlib import Path
from colorama import init, Fore, Style
from datetime import datetime
import readline

init(autoreset=True)

def modify_statistics_file(username, file_path='./reddit-data/statistics.csv'):
    try:
        df = pd.read_csv(file_path)
        df.loc[df['statistic'] == 'account name', 'value'] = username
        df.to_csv(file_path, index=False)
        print(Fore.GREEN + f"\nSuccess edit statistics.csv with username: {username}")
    except Exception as e:
        print(Fore.RED + f"Failed: {e}")
        raise

def get_file_checksum(file_path):
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        checksum = sha256_hash.hexdigest()
        print(Fore.YELLOW + f"New checksum for {file_path}: {checksum}")
        return checksum
    except Exception as e:
        print(Fore.RED + f"Failed: {e}")
        raise

def update_check_file(new_checksum, file_path='./reddit-data/checkfile.csv'):
    try:
        df = pd.read_csv(file_path)
        df.loc[df['filename'] == 'statistics.csv', 'sha256'] = new_checksum
        df.to_csv(file_path, index=False)
        print(Fore.GREEN + "Success updated checkfile.csv with new checksum.")
    except Exception as e:
        print(Fore.RED + f"Failed: {e}")
        raise

def zip_csv_files(username, dir_path='./reddit-data/'):
    try:
        current_date = datetime.now().strftime("%Y%m%d")
        zip_filename = f"export_{username}_{current_date}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(dir_path):
                if file.endswith('.csv'):
                    zipf.write(os.path.join(dir_path, file), file)
        print(Fore.MAGENTA + f"CSV files zipped to {zip_filename}")
    except Exception as e:
        print(Fore.RED + f"Failed: {e}")
        raise

if __name__ == "__main__":
    try:
        banner = """
  ______ ______  _______ _______
 |_____/ |     \ |_____|    |   
 |    \_ |_____/ |     |    |   
                                  
File Bypasser - Github: IM-Hanzou"""
        print(Fore.RED + banner + "\n")
        username = input(f'{Fore.CYAN}Insert reddit username: ')
        if not username:
            print(Fore.RED + 'Username cannot be empty!')
            exit(0)
    
        modify_statistics_file(username)
        checksum = get_file_checksum('./reddit-data/statistics.csv')
        print(Fore.YELLOW + f"New statistic sha: {checksum}")
        
        update_check_file(checksum)
        
        zip_csv_files(username)
        
        print(Fore.GREEN + 'All tasks completed!')
    except Exception as error:
        print(Fore.RED + f"An error occurred: {error}")
