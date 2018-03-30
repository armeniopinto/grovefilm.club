import argparse
import re
import requests
import json


API_KEY = "FIXME"


def get_imdb_ids(year_file_name):
	ids = []
	with open(year_file_name) as f:
		for line in f.readlines():
			matches = re.search(r'\[.+\]\(.+\/(.+)\/\)', line)
			if matches:
				ids.append(matches.group(1))
	return ids


def get_stats(ids):
	stats = {
		"number_of_films": len(ids),
		"runtimes": [],
		"total_runtime": 0,
		"genres_count": {
		},
		"actors_count": {
		}
	}
	for id in ids:
		response = requests.get(url = "http://www.omdbapi.com/?i={}&apikey={}".format(id, API_KEY)).json()
		#with open("sample.json") as file:
		#	response = json.load(file)

		try:
			runtime = int(response["Runtime"].rsplit(" ")[0])
			stats["runtimes"].append(runtime)
			stats["total_runtime"] += runtime
		except ValueError:
			print("Runtime not found for '{}'.".format(response["Title"]))

		for genre in response["Genre"].rsplit(", "):
			genres_count = stats["genres_count"]
			if (genre not in genres_count):
				genres_count[genre] = 0
			genres_count[genre] += 1

		for actor in response["Actors"].rsplit(", "):
			actors_count = stats["actors_count"]
			if (actor not in actors_count):
				actors_count[actor] = 0
			actors_count[actor] += 1

	sort_by_count(stats, "genres_count")
	sort_by_count(stats, "actors_count")
	return stats


def sort_by_count(stats, key):
	d = stats[key]
	new = {}
	for k in sorted(d, key = d.get, reverse = True):
		new[k] = d[k]
	stats[key] = new


def print_stats(stats):
	print(stats)
	print("We watched a total of {} films.".format(stats["number_of_films"]))
	
	print("The combined total runtime was {}.".format(duration_to_string(stats["total_runtime"] * 60)))
	average = int(sum(stats["runtimes"]) / len(stats["runtimes"]))
	print("The average runtime per film was {} minutes.".format(average))

	genres_count = stats["genres_count"]
	mc_genre = list(genres_count.keys())[0]
	print("The most common genre was {} ({} times).".format(mc_genre, genres_count[mc_genre]))
	lc_genre = list(genres_count.keys())[len(genres_count) - 1]
	print("The least common genre was {} ({} times).".format(lc_genre, genres_count[lc_genre]))

	actors_count = stats["actors_count"]
	ac_genre = list(actors_count.keys())[0]
	print("The most common actor was {} ({} times).".format(ac_genre, actors_count[ac_genre]))


def duration_to_string(seconds):
	seconds = int(seconds)
	days, seconds = divmod(seconds, 86400)
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)
	return "{} days, {} hours and {} minutes".format(days, hours, minutes)



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("year_file")
	args = parser.parse_args()

	ids = get_imdb_ids(args.year_file)
	stats = get_stats(ids)
	print_stats(stats)


if __name__ == "__main__":
	main()