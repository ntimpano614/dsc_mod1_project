import pandas as pd
import requests
import time

# original dataset

def id_to_info(id):
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


# r = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=e9de04fcc8a31bc7b76e80846b9bc597&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&primary_release_year=2020')
# print(r.status_code)
# data = r.json()

errors = []
ids = []

total_pages = 501
all_rows = []
columns = ['genre_ids', 'id', 'original_language', 'original_title', 'popularity',
       'release_date', 'title', 'vote_average', 'vote_count']
other_cols = ['revenue','budget', 'runtime', 'imdb_id']
all_columns = columns + other_cols

for page in range(1,total_pages):
    r = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=e9de04fcc8a31bc7b76e80846b9bc597&language=en-US&sort_by=popularity.desc&\
    include_adult=false&include_video=false&page={page_number}&primary_release_year=2019'.format(page_number = page))
    print(r.status_code)
    data = r.json()
    for result in data['results']:
        more_info = id_to_info(result['id'])
        temp_lst = []
        for col in columns:
            temp_lst.append(result[col])
        for col in other_cols:
            temp_lst.append(more_info[col])
        all_rows.append(temp_lst)

df = pd.DataFrame(all_rows,columns = all_columns)
df.to_csv('zippedData/tmdb/tmdb_movies_updated_final.csv')
# errors_df.to_csv('zippedData/tmdb/tmdb_unknown_ids.csv')
#('zippedData/tmdb/tmdb_movies_revenue.csv')
