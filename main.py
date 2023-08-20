from bs4 import BeautifulSoup as b4
import api
import sys

def main(args):
    if len(args) < 2:
        print("Wrong arguments. \nUsage:exec <anime url> <folder to save episodes>")
        exit()

    anime_url = args[1]
    to = "./"

    if len(args) >= 3:
        to = args[2]

    print("Starting downloading")
    api.utils.animew_download_episodes(anime_url,to)
    print("Finished downloading")

if __name__ == "__main__":
    main(sys.argv)
