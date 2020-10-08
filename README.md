# Adaptive Collaborative Filtering for Recommender Systems (ACF)

## 1. Overview

This is implementation of my paper [Adaptive Collaborative Filtering for Recommender Systems](https://doi.org/10.1007/978-3-030-23182-8_9), a graph-based model for large scale recommendation systems with the ability to automatically balance multiple evaluation metrics.

    La A., Vo P., Vu T. (2019) Adaptive Collaborative Filtering for Recommender System. In: Endres D., Alam M., Şotropa D. (eds) Graph-Based Representation and Reasoning. ICCS 2019. Lecture Notes in Computer Science, vol 11530. Springer, Cham. https://doi.org/10.1007/978-3-030-23182-8_9

### Functions

1. Recommending similar items: recommending items given 1 or list of items
2. Personalization: recommending items given ID of a user
3. Other
    - Trending recommendation: training models with lambda (a parameter, detail below) close to 1.0 first, then use 1. or 2.
    - After training, reporting 4 characteristics of dataset via 4 evaluation metrics: popularity, diversity, coverage, congestion. Note that the model automatically balances all metrics.
    - Getting user-item or item-item matrix for futher analysis on graph of data.

![demo.png](/images/demo.png) Examples of recommending items given an item or list of historical items of a user on [the ecommerce dataset](https://www.kaggle.com/carrie1/ecommerce-data)

### How to use

  - Read data and save into a pandas dataframe
  - Create a log parser object with passing column names of user key and item key
  
     ```python
      log_parser = LOG_PARSER(log_df, user_key='CustomerID', item_key='StockCode')
     ```
  
  - Create an AWC_REC object by passing log parser and setting of parameters
  
     ```python
     awc = AWC_REC(log_parser, parameters={'gamma':0.5, 'lambda':0.7})
     ```
      
  - Using log_parser to get ids of users and items 
   
     ```python
     item_his = log_parser.get_itemids(0) #get ids of item with StockCode = 0
     ```
        
  - Recommend for an item or a user
  
     ```python
     rec_df = awc.recommend(item_his)
     ```
     
   Beside that, there are functions: ```awc.recommend_byusers```, ```awc.get_itemitem_matrix```, ```awc.get_useritem_matrix```. Checkout [awc_matrix_computing/main.py](/awc_matrix_computing/main.py). 
   
      
### Parameters

  Gamma and lambda is two tunable parameters of the model. In negative side, the model exploits more on the differences between users, while positive values allow the model focuses more on common interests between users. Lambda is in range [0.0, 1.0], higher value gives more trending results.
 
 Keep tracks on evaluation metrics (popularity, diversity, coverage, congestion) of results while tuning parameters, the model reveals the relationship between metrics on dataset. The point which has highest precision on training set also has balancing values on other metrics.

## 2. Details

### 2.1 Matrix computing for AWC formula

Requirement: numpy, pandas

The recommending formula of ACF is AWC (Adaptive Weighted Conduction). It balances multiple evaluation metrics at the same time. AWC can be represented as matrix multiplication. Checkout the folder [awc_matrix_computing](/awc_matrix_computing), [lib/utils](/lib/utils).

### 2.2. Visualize relationship between metrics

Visualization of relationship between metrics is implemented in [visualize](/visualize).

Tuning parameters of AWC reveals and adapts to characteristics of each dataset. 
+ Users focus more on trending items (common preferences) or unpopular items (specific preferences). The type of preferences is indicated by popularity.
+ Selecting the appropriate strategy (recommending trending or speicific items) leads to high precision and balacing diversity, coverge, congestion.

![visualize/metric_relationship.png](visualize/metric_relationship.png)

Visualize relationship between evaluation metrics while running AWC on [MovieLen 100k](https://grouplens.org/datasets/movielens/100k/)


### 2.3. Large-scale recommending

The rest of the projects are large-scale recommending. History of users are represented as graph. The item-item matrix is calculated on graph, then recommending occurs in containers, each of them includes a pre-determined number of users.  

+ Requirement: numpy, pandas and C++ for graph.
+ To start running the code, check out [bash](/bash), where demo and recommending for MovieLen with multiple parameters are provided. These example includes automatically evaluating the result of recommending by 5 metrics: precicion, popularity, diversity, coverage and congestion.

