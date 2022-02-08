import requests


def main():
    usr_input = input("Input the URL: \n")
    r = requests.get(usr_input)

    if r.status_code != 200 or not r.json().get('content'):
        print("Invalid quote resource!")
    else:
        quote = r.json()['content']
        print(quote)


if __name__ == "__main__":
    main()
