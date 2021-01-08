
from bs4 import BeautifulSoup
import requests
import json
from os import path
import random
import time



def scrape_top_list(url):
    if path.exists('movies.txt'):
        print('file exists')
        print('opening and reading existing file')

        json_file = open('movies.txt', 'r')
        movies_file = json_file.read()
        movies_list = json.loads(movies_file)
        return movies_list

    else:
        top_movies_list=scrape_top_list_if_no_file(url)
        print('file does not exist')

        text_file = open('movies.txt', 'w')
        text_file.write(json.dumps(top_movies_list))
        text_file.close()
        print('file created')

        print('opening and reading created file')
        json_file = open('movies.txt', 'r')
        movies_file = json_file.read()
        movies_list = json.loads(movies_file)

        return movies_list


def scrape_top_list_if_no_file(url): #Task 1  #function to get all 250 movie details
    top_movies_list=[]                                                           #variable to list all movies
    base_url = 'https://www.imdb.com'                                            #base url to add to link obtained for individual movie url

    html_text = requests.get(url).text                                           #gets the html code of the url page
    soup = BeautifulSoup(html_text, 'html.parser')                                        

    movies_html = soup.find('tbody', class_='lister-list')                       #finds lister-list in soup which is a html table that contains all movies details
    movies = movies_html.find_all('tr')                                          #finds and lists all tr elements in lister-list, each tr element contains one movie details

    for movie in movies:
        movie_details = {}                                                       #dictionary to store each movie details
        movie_dtls = movie.find('td', class_='titleColumn').text.split()         #gives position,movie name,year present in td element of class=titlecolumn
        movie_name = movie.find('td', class_='titleColumn').a.text               # a tag contains movie name
        movie_rating = soup.find('td', class_='ratingColumn imdbRating').text    # td element of class =ratingColumn imbdRating contains movie rating
        link = movie.a['href']                                                   # a tag has an attribute href which contains movie link

        movie_details['position'] = int(movie_dtls[0][:-1])                      # converting str to int, '1.' --> 1
        movie_details['name'] = movie_name                                       #string
        movie_details['year'] = int(movie_dtls[-1][1:-1])                        #converting str to int, '(1999)' --> 1999
        movie_details['rating'] = float(movie_rating)                            #converting str to float, '8.9' -->8.9, since rating should be in decimals
        movie_details['URL'] = base_url+link                                     #combining basic imbd link to individual movie link to give full movie link
        top_movies_list.append(movie_details)                                    #appending each movie_details dict to top_movies_list 
    
    return top_movies_list


def group_by_year(top_movies_list): #Task 2   #function to group all movies by year
    movies_by_year = {}                                                             
    for movie in top_movies_list:
        if movie['year'] in movies_by_year:
            movies_by_year[movie['year']].append(movie)
        else:
            movies_by_year[movie['year']]=[movie]
    return movies_by_year


def group_by_decade(top_movies_list):  #Task 3 #function to group all movies by decade
    movies_by_decade={}
    movies_by_year = group_by_year(top_movies_list)                               #function to get a list of all movies by grouped year
    
    for decade in range(1950,2021,10):
        for movie_year in movies_by_year:
            if decade<=movie_year<(decade+10):
                if decade in movies_by_decade:
                    for i in movies_by_year[movie_year]:
                        movies_by_decade[decade].append(i)
                else:
                    movies_by_decade[decade] = movies_by_year[movie_year]



    return movies_by_decade


def scrape_movie_details(top_movies_list):
    if path.exists('movies_details.txt'):
        print('file exists')
        print('opening and reading existing file')

        json_file = open('movies_details.txt', 'r')
        movies_file = json_file.read()
        movies_list = json.loads(movies_file)
        return movies_list

    else:
        movie_more_details = get_url_link_if_nofile(top_movies_list)
        print('file does not exist')

        text_file = open('movies_details.txt', 'w')
        text_file.write(json.dumps(movie_more_details))
        text_file.close()
        print('file created')

        print('opening and reading created file')
        json_file = open('movies_details.txt', 'r')
        movies_file = json_file.read()
        movies_list = json.loads(movies_file)

        return movies_list


def scrape_movie_details_if_nofile(movie_url):  #Task 4

    movie_details_dict={}

    html_text = requests.get(movie_url).text                                   # gets the html code of the url page
    soup = BeautifulSoup(html_text, 'html.parser')

    movie_name = soup.find('div', class_='title_wrapper').h1.text[:-7]
    image_source = soup.find('div', class_='poster').img['src']
    bio = soup.find('div', class_='summary_text').text.strip()

    find_director = soup.find_all('div', class_='credit_summary_item')
    directors_names = []
    for head_tag in find_director:
        if head_tag.h4.text == 'Director:' or head_tag.h4.text == 'Directors:':
            directors = head_tag.find_all('a')
            for director in directors:
                directors_names.append(director.text)
            
            

    find_genres = soup.find_all('div', class_='see-more inline canwrap')
    for head_tag in find_genres:
        genres = []
        if head_tag.h4.text == 'Genres:':
            genres_list = head_tag.find_all('a')
            for genre in genres_list:
                genres.append(genre.text)

    other_details = soup.find_all('div', class_='txt-block')
    runtime=''
    for head_tag in other_details:
        # print(head_tag,end='\n\n')
        if head_tag.h4 != None:
            # print(head_tag.h4)
            if head_tag.h4.text == 'Country:':
                country = head_tag.a.text
            elif head_tag.h4.text == 'Runtime:':
                runtime = head_tag.time.text
            elif head_tag.h4.text == 'Language:':
                languages = []
                find_languages = head_tag.find_all('a')
                for language in find_languages:
                    languages.append(language.text)
    movie_details_dict['Movie Name']=movie_name
    movie_details_dict['Directors']=directors_names
    movie_details_dict['Country']=country
    movie_details_dict['Language']=languages
    movie_details_dict['poster_image_url']=image_source
    movie_details_dict['bio']=bio
    movie_details_dict['RunTime']=runtime
    movie_details_dict['Genre']=genres

    return movie_details_dict
    

def get_url_link_if_nofile(top_movies_list):
    movies_more_details = []

    for movie in top_movies_list:
        movie_url = movie['URL']
        # scrape_movie_details(movie_url)
        movie_details_dict = scrape_movie_details_if_nofile(movie_url)
        movies_more_details.append(movie_details_dict)
        # print(movies_more_details,end='\n\n\n')
    # print(movies_more_details)
    return movies_more_details


def scrape_top10_movie_details(top_movies_list): #Task 5
    movie_more_details=scrape_movie_details(top_movies_list)
    return movie_more_details[:10]


def analyse_movies_by_language(top10_movie_details): #Task 6
    top10_movies_by_language={}
    for movie in top10_movie_details:
        language_list=movie['Language']
        for language in language_list:
            top10_movies_by_language[language]=top10_movies_by_language.get(language,0)+1
    return top10_movies_by_language


def analyse_movies_by_director(top10_movie_details): #Task 7
    top10_movies_by_director = {}
    for movie in top10_movie_details:
        director_list = movie['Directors']
        for director in director_list:
            top10_movies_by_director[director] = top10_movies_by_director.get(director, 0)+1
    return top10_movies_by_director



url = 'https://www.imdb.com/india/top-rated-indian-movies/'

#    <-------------Task 1----------------->
top_movies_list = scrape_top_list(url)                    #gives list top of top 250 movies with position,name,year,rating and url
# print('top_movies_list:',len(top_movies_list))
# for movie in top_movies_list:
#     for detail in movie:
#         print(detail,':',movie[detail],sep=' ')
#     print('\n')



#    <-------------Task 2----------------->
# movies_by_year=group_by_year(top_movies_list)           # groups the movies in top_movies_list by year
# for year in movies_by_year:
#     print(year,':',end='\n')                                   
#     for movie in movies_by_year[year]:
#         for detail in movie:
#             print('\t',detail, ':', movie[detail], sep=' ')
#         print('\n')



#    <-------------Task 3----------------->
# movies_by_decade=group_by_decade(top_movies_list)        #groups the movies in top_movies_list by decade
# for decade in movies_by_decade:
#     print(decade, ':', end='\n')                       
#     for movie in movies_by_decade[decade]:
#         for detail in movie:
#             print('\t', detail, ':', movie[detail], sep=' ')
#         print('\n')


#    <-------------Task 4----------------->
# movie_more_details=scrape_movie_details(top_movies_list)
# for movie in movie_more_details:
#     for detail in movie:
#         print(detail,':',movie[detail],sep=' ')
#     print('\n')
# print('movie_more_details:', len(movie_more_details))



#    <-------------Task 5----------------->
top10_movie_details= scrape_top10_movie_details(top_movies_list)
# for movie in top10_movie_details:
#     for detail in movie:
#         print(detail,':',movie[detail],sep=' ')
#     print('\n')


#    <-------------Task 6----------------->
# top10_movies_by_language =analyse_movies_by_language(top10_movie_details)
# for language in top10_movies_by_language:
#     print(language,':',top10_movies_by_language[language],sep=' ')


#    <-------------Task 7----------------->
# top10_movies_by_director = analyse_movies_by_director(top10_movie_details)
# for director in top10_movies_by_director:
#     print(director, ':', top10_movies_by_director[director], sep=' ')
                                        
