import requests
from bs4 import BeautifulSoup


def main():
    usr_input = input("Input the URL: \n")

    if "title" not in usr_input:
        print("Invalid movie page!")
    else:
        r = requests.get(usr_input, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(r.content, 'html.parser')

        h1 = soup.find('h1')
        description = soup.find('span', {'data-testid': 'plot-l'})
        result = {"title": h1.text, "description": description.text}
        print(result)


if __name__ == "__main__":
    main()
