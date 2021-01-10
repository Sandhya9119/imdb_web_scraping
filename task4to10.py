import req

url = 'https://www.imdb.com/india/top-rated-indian-movies/'
top_movies_list = req.scrape_top_list(url)

#    <-------------Task 4----------------->
movie_more_details=req.scrape_movie_details(top_movies_list)
for movie in movie_more_details:
    for detail in movie:
        print(detail,':',movie[detail],sep=' ')
    print('\n')
print('movie_more_details:', len(movie_more_details))


#    <-------------Task 5----------------->
top10_movie_details= req.scrape_top10_movie_details(top_movies_list)
for movie in top10_movie_details:
    for detail in movie:
        print(detail,':',movie[detail],sep=' ')
    print('\n')


#    <-------------Task 6----------------->
top10_movies_by_language =req.analyse_movies_by_language(top10_movie_details)
for language in top10_movies_by_language:
    print(language,':',top10_movies_by_language[language],sep=' ')


#    <-------------Task 7----------------->
top10_movies_by_director = req.analyse_movies_by_director(top10_movie_details)
for director in top10_movies_by_director:
    print(director, ':', top10_movies_by_director[director], sep=' ')

#    <-------------Task 10----------------->
movie_analysis_dict = req.analyse_by_language_and_director(top_movies_list)
for director in movie_analysis_dict:
    print(director, ':')
    for languages in movie_analysis_dict[director]:
        print('\t\t', languages, ':', movie_analysis_dict[director][languages])
    print('\n')
