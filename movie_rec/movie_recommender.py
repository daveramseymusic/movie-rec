# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_movie_recommender.ipynb.

# %% auto 0
__all__ = ['path', 'data_folder', 'learn', 'df_titles', 'get_movie_recs', 'search_movie_titles', 'search_movies_n_recommend']

# %% ../nbs/00_movie_recommender.ipynb 11
# For modeling
from fastai.tabular.all import *
from fastai.collab import *
#for publishing the model
import gradio as gr

# %% ../nbs/00_movie_recommender.ipynb 16
#load the model and movie titles with indexes (from the previous data loaders)
path = Path('.')
data_folder = '../models_and_dls'

#check if modedels folder is up one level if not 'for readme' then check in current directory
if not os.path.isdir(data_folder):
    data_folder = './models_and_dls'
#load learner and titles csv    
learn = load_learner(path/data_folder/'movie_18mil_xu_mdl_669.pkl')
df_titles = pd.read_csv(path/data_folder/'movie_18mil_xu.csv')

# %% ../nbs/00_movie_recommender.ipynb 18
def get_movie_recs(full_title:str, # String saved to `favorite_movie` variable
                   learn,# Trained Model
                   df_titles: pd.DataFrame #DataFrame with all movie titles from dls
                        ):
    "This function will use the `nn.CosineSimilarity` on the 50 latent factors for each movie to find the 30 movies most similar to your favorite movie."
    movie_factors = learn.model.i_weight.weight
    idx = int(df_titles[df_titles.title == full_title].midx)
    distances =  nn.CosineSimilarity(dim=1)(movie_factors,movie_factors[idx][None])
    idx = distances.argsort(descending=True)
    return [o for o in df_titles.title[idx.tolist()][:30]]

# %% ../nbs/00_movie_recommender.ipynb 19
def search_movie_titles(favorite_movie:str, # String saved to `favorite_movie` variable
                        df_titles:pd.DataFrame): #DataFrame with all movie titles located in the column `title` from dls
    "This Function searches through df_titles['title'] column for titles that contian words saved in the `favorite_movie` variable after making all words lowercase and removing THE from the start of a title"
    movies_found = ''
    s = favorite_movie.lower()
    #remove THE from the title
    if s[:4] == 'the ':
        s = s[4:]

    lst = df_titles['title'].tolist() # turn it to a list
    index = []
    i=0
    length = len(lst)
    while i<length:
        if s in lst[i].lower():
            full_title = lst[i]
            movies_found+= str(full_title) +'\n'
#             print(f'Your Favorite Movies:  {full_title}')
        i+=1
    return full_title, movies_found

# %% ../nbs/00_movie_recommender.ipynb 20
def search_movies_n_recommend(favorite_movie:str, # The movie title typed into the `gr.Textbox()` that the user will see on the `gradio` app
                             learn, # Trained model
                              df_titles: pd.DataFrame, # Movie titles df
                             ):
    "This function returns 30 recommendations using `search_movie_titles` and `get_movie_recs`."
    full_title, movies_found = search_movie_titles(favorite_movie, df_titles=df_titles)    
    # write explaination in case multiple movies
    explainer = f'If there are multiple movies above: Please paste your favorite movie into the "favorite_movie" box.\n The box below is currently showing recommendations for the movie:  {full_title}'
    #print movies found and explainer
    output_str =  movies_found+'\n\n'+explainer
    
    #get recommendations from model
    recommendations = get_movie_recs(full_title=full_title, learn=learn, df_titles=df_titles) 
    
    #create list of all the recommendations to print
    print_lst = ''
    for o in recommendations:    print_lst =print_lst+str(o) + '\n'
    
    return output_str, f'Recommendations for {full_title}: \n\n {print_lst}'
