from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests

BASEURL = 'https://www.boxofficemojo.com/year/'
APIURL = 'https://www.omdbapi.com/'
KEY = 'OMEGALUL YOURE NOT MY REAL KEY'


def get_movies_for_year(year: int) -> [str]:
    out = []
    url = BASEURL + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find("div", {"id": "table"})
    t = div.find("table")
    rows = t.find_all('tr')
    for row in rows:
        try:
            title = row.findAll('td')[1].a.contents[0]
            out.append(title)
            # out.append(row.findAll('td')[1].a.contents)
        except Exception as e:
            print(e)

    return out


def get_all_movies_by_year() -> {int: [str]}:
    yr = int(datetime.today().strftime("%Y"))
    return {year: get_movies_for_year(year) for year in range(1977, yr+1)}


def get_movie_runtime_by_title(title: str, year=None) -> int:
    info = get_movie_info_by_title(title, year)
    try:
        return int(info["Runtime"].split(" ")[0])
    except Exception as e:
        print(e)
        return -1


def get_movie_info_by_title(title: str, year=None) -> {str: str}:
    url = APIURL + '?t=' + title + '&apikey=' + KEY
    if year:
        url += '&y=' + str(year)
    print("Trying to get: " + title)
    try:
        ret = requests.get(url, timeout=0.3)
        info = json.loads(ret.content)
        return dict(info)
    except Exception as e:
        return {}


def get_runtimes_for_year(year: int):
    movies = get_movies_for_year(year)
    out = []
    for movie in movies:
        runtime = get_movie_runtime_by_title(movie, year)
        if runtime != -1:
            out.append(runtime)
    print(out)
    return out


if __name__ == "__main__":
    # movies = get_movies_for_year("2020")
    # print(movies)
    # print(get_all_movies_by_year())
    get_runtimes_for_year(2020)


