class TreeNode:
    """
    Represents a node in a decision tree for the 20 Questions game.
    """

    def __init__(self, feature=None, value=None, results=None, yes_child=None, no_child=None):
        """
        Initializes a TreeNode.

        Args:
            feature (str): The feature (question) associated with the node.
            value (int): The value of the feature (e.g., 1 or 0 for binary features).
            results (dict): A dictionary of possible results (movie titles) and their counts at this node.
            yes_child (TreeNode): The child node for the "yes" branch.
            no_child (TreeNode): The child node for the "no" branch.
        """
        self.feature = feature
        self.value = value
        self.results = results
        self.yes_child = yes_child
        self.no_child = no_child

    def __repr__(self):
        """
        String representation of the TreeNode.
        """
        if self.results:
            return f"TreeNode(results={self.results})"
        else:
            return f"TreeNode(feature={self.feature}, value={self.value})"



"""


FUNCTION CONTRACTS:

load_movie_data(filepath):
    Input: filepath (string) - The path to the CSV file containing movie data.
    Output: movies (List of Dictionaries) - A list of dictionaries, where each dictionary represents a movie and its features.
    Purpose: Reads the movie data from the CSV file and returns it in a usable format.

build_tree(movies, features):
    Input: movies (List of Dictionaries), features (List of Strings) - The movie data and the list of feature names.
    Output: root (TreeNode) - The root node of the decision tree.
    Purpose: Constructs the decision tree, prioritizing even splits.

    find_best_split(movies, features):
        Input: movies (List of Dictionaries), features (List of Strings) - The movie data and the list of available features.
        Output: best_feature (string) - The name of the feature that most evenly splits the data (count amount of 1 and 0 and return feature with minimum difference between counts)
        Purpose: Finds the feature that most evenly splits the data.

    split_data(movies, feature, value):
        Input: movies (List of Dictionaries), feature (string), value (integer) - The movie data, the feature to split on, and the value to split by (0 or 1).
        Output: (true_set, false_set) (Tuple of List of Dictionaries) - Two lists of movies, split based on the feature value.
        Purpose: Splits the movie data into two subsets based on a feature and its value.

    get_results(movies):
        Input: movies (List of Dictionaries)
        Output: results (Dictionary) - A dictionary of movie titles and their counts.
        Purpose: Returns the counts of movies remaining.

play_game(root, movies):
    Input: root (TreeNode), movies (List of Dictionaries) - The root node of the decision tree and the original movie data.
    Output: None (prints game output).
    Purpose: Manages the gameplay loop, traversing the decision tree based on user input.

    ask_question(feature):
        Input: feature (string) - The feature to ask the user about.
        Output: answer (string) - The user's answer ("yes" or "no").
        Purpose: Asks the user a question and gets their response.

    get_remaining_movies(node):
        Input: node (TreeNode) - The current node in the decision tree.
        Output: remaining_movies (List of Strings) - A list of the remaining possible movie titles.
        Purpose: Gets the list of movies remaining at the current node.

    display_results(remaining_movies):
        Input: remaining_movies (List of Strings) - The list of remaining possible movie titles.
        Output: None (prints results).
        Purpose: Displays the final results to the user.


Relationships:
    load_movie_data provides the initial movie data to build_tree and play_game.

    build_tree uses calculate_entropy, find_best_split, split_data, and get_results to construct the decision tree.

    play_game uses ask_question, get_remaining_movies, and display_results to manage the gameplay.

    build_tree creates the tree that play_game traverses.

"""

import csv
import random
movie_name=''
def load_movie_data(filepath):
    """
    Reads the movie data from the CSV file and returns it as a list of dictionaries
    and the list of feature categories (excluding the identifier column).
    
    Parameters:
        filepath (str): Path to the CSV file.
    
    Returns:
         List of movie dictionaries and list of feature names.
    """
    movies = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        all_columns = reader.fieldnames
        identifier_column = all_columns[0]   # assume first column is identifier (e.g., movie name)
        movie_name=identifier_column
        categories = all_columns[1:]         # treat remaining columns as features
        
        for row in reader:

            movies.append(dict(row))

    return movies, categories,movie_name


def build_tree(movies,categories,movie_name):
  
    if len(categories)==0 or len(movies)<=1:
        return TreeNode(feature=[movie[movie_name]for movie in movies])

    def find_best_split(movies, categories):
        min_diff = float('inf')
        best_feature = None
        for category in categories:
            ones=0
            for movie in movies:
                if movie[category] == '1':
                    ones+=1
            
            zeros = len(movies) - ones
            diff = abs(ones - zeros)
            if diff < min_diff:
                
                min_diff = diff
                best_feature = category

        return best_feature
    
    def split_data(movies, category, value):
        true=[]
        false=[]
        for movie in movies:
            if movie[category]==value:
                true.append(movie)
            else:
                false.append(movie)
        return true,false



    cat=find_best_split(movies, categories)
    remaining_features = [f for f in categories if f != cat]
    yes_movies,no_movies=split_data(movies, cat, '1')
    if not yes_movies or not no_movies:
        return TreeNode(feature=[movie[movie_name]for movie in movies])
    true_branch=build_tree(yes_movies, remaining_features,movie_name)
    false_branch=build_tree(no_movies, remaining_features,movie_name)

    return TreeNode(feature=cat, yes_child=true_branch, no_child=false_branch)



def play_game(root):     
    def ask_question(category):
        answer=input(f"is your movie {category} ")
        if answer.lower()=='yes':
            return True
        elif answer.lower()=='no':
            return False
        else:
            print("invalid answer, type yes or no")
            ask_question(category)

    def winner_messages(again):
        if again.lower()=="yes":
            play_game(root)
        elif again.lower()=="no":
            print("alright, bye!")
        else:
            again=input("invalid answer, type yes or no: ")
            winner_messages(again)
        
    def display_results(results,guesses):
        answer=False
        if len(results)>0:
            rand=random.randint(0,len(results))
            answer=ask_question(results[rand])
        if answer:
            again=input(f"good game!I won in only {guesses} guesses...want to play again? ")
            winner_messages(again)
        else:
            again=input(f"movie not found, congratulations!...want to play again? ")
            winner_messages(again)

    def get_next_question(root,guesses):
        if type(root.feature)==list:
            return display_results(root.feature,guesses+1)
        elif ask_question(root.feature):
            get_next_question(root.yes_child,guesses+1)
        else:
            get_next_question(root.no_child,guesses+1)

    get_next_question(root,0)

movies,categories,movie_name=load_movie_data('Corrected_Movie_Dataset.csv')

root=build_tree(movies, categories,movie_name)

def transverse(root,child,number):
    print(" " * (child * 4) + f"{number}{root.feature}")
    if root.yes_child:
        transverse(root.yes_child, child+1,str(f"{number}.1"))
    if root.no_child:
        transverse(root.no_child, child+1,str(f"{number}.2"))
transverse(root, 0,'0')



play_game(root)
