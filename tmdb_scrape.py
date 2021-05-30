import pandas as pd
import requests
import time

# original dataset
tmdb_movies = pd.read_csv('zippedData/tmdb/tmdb_movies.csv', index_col=0)
# get genres for tmdb
# r = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=e9de04fcc8a31bc7b76e80846b9bc597&language=en-U')
# print(r.status_code)
# tmdb_genres = r.content
# tmdb_g = r.json()

errors = []
ids = []

def id_to_revenue_budget(id):
    r = requests.get('https://api.themoviedb.org/3/movie/{movie_id}?api_key=e9de04fcc8a31bc7b76e80846b9bc597&language=en-U&sort_by=revenue.desc&include_all_movies=true'.format(movie_id=id))
    if r.status_code == 200:
        data = r.json()
        # the runtime and imdb_id may return null, which will not work when creating the df
        if data['runtime'] == None:
            print('runtime is none')
            data['runtime'] = 0
        elif data['imdb_id'] == None:
            print('imdb_id is none')
            data['imdb_id'] = 'nan'
        return {'revenue':data['revenue'], 'budget':data['budget'], 'runtime':data['runtime'], 'imdb_id':data['imdb_id']}
    else:
        print('There was an error with the request: ')
        print(r.status_code)
        print('Error with movie: ')
        print(id)
        errors.append(r.status_code)
        ids.append(id)
        return {'revenue': 0, 'budget':0, 'runtime':0, 'imdb_id': 'nan'}

df = tmdb_movies
df['revenue'] = 0
df['budget'] = 0
df['runtime'] = 0
df['imdb_id'] = '0'
for index, row in df.iterrows():
    result = id_to_revenue_budget(row['id'])
    df['revenue'].values[index] = result['revenue']
    df['budget'].values[index] = result['budget']
    df['runtime'].values[index] = result['runtime']
    df['imdb_id'].values[index] = result['imdb_id']

# create dictionary of errors
error_dict = {'error_code':errors,'id':ids}
errors_df = pd.DataFrame(error_dict)

df.to_csv('zippedData/tmdb/tmdb_movies_updated_02.csv')
errors_df.to_csv('zippedData/tmdb/tmdb_unknown_ids.csv')

#('zippedData/tmdb/tmdb_movies_revenue.csv')
