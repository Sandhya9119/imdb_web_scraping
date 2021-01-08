import req

url = 'https://www.imdb.com/india/top-rated-indian-movies/'


# gives list top of top 250 movies with position,name,year,rating and url
top_movies_list = req.scrape_top_list(url)
print('top_movies_list:',len(top_movies_list))
for movie in top_movies_list:
    for detail in movie:
        print(detail,':',movie[detail],sep=' ')
    print('\n')


#    <-------------Task 2----------------->
movies_by_year=req.group_by_year(top_movies_list)           # groups the movies in top_movies_list by year
for year in movies_by_year:
    print(year,':',end='\n')
    for movie in movies_by_year[year]:
        for detail in movie:
            print('\t',detail, ':', movie[detail], sep=' ')
        print('\n')


# #    <-------------Task 3----------------->
movies_by_decade=req.group_by_decade(top_movies_list)        #groups the movies in top_movies_list by decade
for decade in movies_by_decade:
    print(decade, ':', end='\n')
    for movie in movies_by_decade[decade]:
        for detail in movie:
            print('\t', detail, ':', movie[detail], sep=' ')
        print('\n')
