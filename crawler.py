import os
import argparse
import urllib

BASE_URL = 'http://hsin.hr/honi/arhiva'
YEARS = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
ROUNDS = [6, 6, 6, 7, 7, 6, 6, 6, 7]

def make_season(year):
    return "{0}_{1}".format(year, year+1)

def make_task_name(round_index):
    return "kolo{0}_zadaci.pdf".format(round_index)

def make_test_name(round_index):
    return "kolo{0}_testpodaci.zip".format(round_index)

def make_solution_name(round_index):
    return "kolo{0}_rjesenja.zip".format(round_index)

def make_url(season, name):
    return "{0}/{1}/{2}".format(BASE_URL, season, name)

def crawl(dest_dir):
    for year, rounds in zip(YEARS, ROUNDS):
        season = make_season(year)

        for round_index in range(1, rounds+1):
            output_dir = os.path.join(dest_dir, season, str(round_index))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            task_name = make_task_name(round_index)
            task_url = make_url(season, task_name)
            task_destination = os.path.join(output_dir, task_name)
            urllib.urlretrieve(task_url, task_destination)
            print "{0} ===> {1}".format(task_url, task_destination)

            test_name = make_test_name(round_index)
            test_url = make_url(season, test_name)
            test_destination = os.path.join(output_dir, test_name)
            urllib.urlretrieve(test_url, test_destination)
            print "{0} ===> {1}".format(test_url, test_destination)

            solution_name = make_solution_name(round_index)
            solution_url = make_url(season, solution_name)
            solution_destination = os.path.join(output_dir, solution_name)
            urllib.urlretrieve(solution_url, solution_destination)
            print "{0} ===> {1}".format(solution_url, solution_destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dest", metavar="DEST DIR", dest="dest", help="directory in which to inflate the task structure")

    options = parser.parse_args()

    crawl(options.dest)

