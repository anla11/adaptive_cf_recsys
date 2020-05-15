# Adaptive Collaborative Filtering for Recommender System

Implementation of my publish [Adaptive Collaborative Filtering](https://doi.org/10.1007/978-3-030-23182-8_9)

## 1. AWC and matrix computing

Although this is graph-based model, AWC can be represented as matrix multiplication. Checkout the folder [awc_matrix_computing](/awc_matrix_computing).

Prequitesite: numpy, pandas

## 2. Large-scale recommending

The rest of the projects are belong to large-scale recommending. History of users are represented as graph. The item-item matrix is calculated on graph, then recommending occurs in containers, each of them includes a pre-determined number of users.  

+ Prequitesite: numpy, pandas and C++ for graph.
+ To start running the code, check out [bash](/bash), where demo and recommending for MovieLen with multiple parameters are provided. These example includes automatically evaluating the result of recommending by 5 metrics: precicion, popularity, diversity, coverage and congestion.
+ Visualization of relationship between metric is implemented in [visualize](/visualize)

![visualize/metric_relationship.png](visualize/metric_relationship.png)
