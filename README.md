#### Synopsis:

The repository employs the Apriori algorithm to mine frequent itemsets within the MovieLens database,  and generate association rules based on these frequent itemsets.<br>
The generation of association rules plays a big role in contemporary Retail and Market Basket Analysis.

At every level in the apriori algorithm, the generated itemsets are further pruned.<br>
This ensures that unnecesary itemsets are not worked upon, generating non-frequent itemsets in forthcoming levels  (derived from the apriori property).

The ratings.csv dataset contains 1,00,836 ratings submitted by MovieLens users across 9,742 movies (present in movies.csv). 

Of the association rules so mined, the top 100 with the highest support and confidence are present in X.txt and Y.txt respectively.

Sample recall and precision values are determined as well (using a 20% test set).


#### Execution:

The files Ruleminer.py and recommender.py mine the association rules and make recommendations for a specific user respectively.

GUI Backend required to display plots.
Files may take a few minutes to run given the size of the dataset.
