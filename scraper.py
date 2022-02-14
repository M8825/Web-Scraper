import requests
from bs4 import BeautifulSoup


def main():
    usr_input = input("Input the URL: \n")
    r = requests.get(usr_input, headers={'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code != 200:
        print(f"The URL returned {r.status_code}!")
    else:
        file = open('source.html', 'wb')
        file.write(r.content)  # Write response content
        file.close()
        print("Content saved.")


if __name__ == "__main__":
    main()
