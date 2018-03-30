import argparse
import re
import requests
import json


API_KEY = "FIXME"


def convert(year_file_name):
	with open(year_file_name) as f:
		return [parse_line(line) for line in f.readlines()]


def parse_line(line):
	matches = re.search(r"\|\ (.+)\ \|\ \|\ (.+)\ \|", line)
	if matches:
		name = matches.group(1)
		info = requests.get(url = "http://www.omdbapi.com/?t={}&apikey={}".format(name, API_KEY)).json()
		date = matches.group(2)
		if "imdbID" in info:
			return "| [{}](http://www.imdb.com/title/{}/) | | {} |".format(info["Title"], info["imdbID"], date)
		else:
			return "'{}' not found!".format(name)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("year_file")
	args = parser.parse_args()

	for line in convert(args.year_file):
		print(line)


if __name__ == "__main__":
	main()