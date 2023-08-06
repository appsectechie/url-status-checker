import requests
from colorama import Fore, Style
from tqdm import tqdm
import sys
import re

def load_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

def check_url_status(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return None

def save_urls_by_status(urls, status_codes, output_files):
    for status_code, output_file in zip(status_codes, output_files):
        matching_urls = [url for url in urls if check_url_status(url) == status_code]
        with open(output_file, 'w') as file:
            file.write('\n'.join(matching_urls))

def print_colored_status(url, status_code):
    if status_code == 200:
        print(f'{Fore.GREEN}{url} - {status_code}{Style.RESET_ALL}')
    elif status_code == 302:
        print(f'{Fore.YELLOW}{url} - {status_code}{Style.RESET_ALL}')
    elif status_code == 403:
        print(f'{Fore.RED}{url} - {status_code}{Style.RESET_ALL}')
    else:
        print(f'{url} - {status_code}')

def get_user_input():
    status_codes = []
    while True:
        code = input("Enter HTTP status code to check (or 'done' to finish): ")
        if code.lower() == 'done':
            break
        try:
            status_code = int(code)
            status_codes.append(status_code)
        except ValueError:
            print("Invalid input. Please enter a valid HTTP status code.")
    return status_codes

def process_urls(urls):
    processed_urls = []
    for url in urls:
        if not re.match(r'^https?://', url):
            url_with_http = f'http://{url}'
            url_with_https = f'https://{url}'
            processed_urls.extend([url_with_http, url_with_https])
        else:
            processed_urls.append(url)
    return processed_urls

def main():
    file_path = 'urls.txt'  # Replace with your file path

    urls = load_urls_from_file(file_path)
    processed_urls = process_urls(urls)

    if len(sys.argv) > 1:
        status_codes = [int(code) for code in sys.argv[1:]]
        output_files = [f'urls_{code}.txt' for code in status_codes]
    else:
        status_codes = get_user_input()
        output_files = [f'urls_{code}.txt' for code in status_codes]

    for url in tqdm(processed_urls, desc="Checking URLs"):
        status_code = check_url_status(url)
        print_colored_status(url, status_code)

    # Check status codes and save URLs
    save_urls_by_status(processed_urls, status_codes, output_files)

if __name__ == '__main__':
    main()
