PersonalizedWebSearch
=====================

This project aims at personalizing web search rankings of a user by analyzing user search history from Yandex's search engine logs. We have built a total of 73 features on the log data, different combinations of which are run on Learning to Rank algorithms. We analyze the importance of different features through the NDCG score obtained for different combinations. The algorithms used are - Random Forest, LambdaMART, RankNet and AdaRank for each set of features. Performance is measured using NDCG score.

Reference: 
P.Masurel,K.Lefevre-Hasegawa, C.Bourguignat, M.Scordia 2013. Dataiku's Solution to Yandex's Personalized Web Search WSCD
