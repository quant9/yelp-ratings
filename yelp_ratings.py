import rauth
import time, string
from pprint import pprint
import yelp_ratings_guru as guru

consumer_key = 'get your own!'
consumer_secret = 'get your own!'
access_token = 'get your own!'
access_token_secret = 'get your own!'


class RatingsTotals(object):

    def __init__(self):
        self.ratings_dict = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 }

    def add_ratings_to_totals(self, ratings):
        for rating in ratings.keys():
            self.ratings_dict[rating] += ratings[rating]

def main():

    ratings_totals = RatingsTotals()
    params = {}
    raw_term = raw_input('Enter business name: ')
    params['term'] = raw_term.lower().replace(' ', '+')
    raw_location = raw_input('Enter your city or zip code: ')
    params['location'] = raw_location.replace(' ', '+')
    max_len = min(5, len(raw_term))
    matches = []

    # sweeps through the first 20*20 = 400 businesses for matches
    for offset in range(20):
        params['offset'] = offset * 20
        results = get_results(params)['businesses']
        for result in results:
            if result['name'].lower().startswith(params['term'][0:max_len]):
                ratings, stats = scrape_result(result['url'])
                matches.append(result)
                print result['name'].ljust(40), ', '.join(result['location']['display_address']).ljust(100), \
                    round(stats['mu'], 2)
                ratings_totals.add_ratings_to_totals(ratings)

    total_stats = guru.get_avg_and_stddev(ratings_totals.ratings_dict)

    print "{} matches found for {} near {}".format(len(matches), raw_term, raw_location)
    for i in range(1,6):
        print "{}-star ratings: {}".format(i, ratings_totals.ratings_dict[i])
    print "Average rating: ".ljust(20), round(total_stats['mu'], 2)
    print "Variance: ".ljust(20), round(total_stats['sigma2'], 3)
    print "Standard deviation: ".ljust(20), round(total_stats['sigma'], 3)

def get_results(params):
 
    session = rauth.OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token,
        access_token_secret = access_token_secret)
        
    request = session.get("http://api.yelp.com/v2/search",params=params)
    
    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()
    return data

def scrape_result(result_url):

    root = guru.get_root_from_url(result_url)
    ratings = guru.get_ratings_from_root(root)
    return ratings, guru.get_avg_and_stddev(ratings)

if __name__=="__main__":
    main()
