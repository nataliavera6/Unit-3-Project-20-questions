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
