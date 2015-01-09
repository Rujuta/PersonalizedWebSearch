PersonalizedWebSearch
=====================

This project aims at personalizing web search rankings of a user by analyzing user search history from Yandex's search engine logs. We have built a total of 73 features on the log data, different combinations of which are run on Learning to Rank algorithms. We analyze the importance of different features through the NDCG score obtained for different combinations. The algorithms used are - Random Forest, LambdaMART, RankNet and AdaRank for each set of features. Performance is measured using NDCG score.

References: 
1. P.Masurel,K.Lefevre-Hasegawa, C.Bourguignat, M.Scordia 2013. Dataikus Solution to Yandex's Personalized Web Search WSCD
2. http://people.cs.umass.edu/~vdang/ranklib.html
3. http://en. wikipedia.org/wiki/Learning_to _rank
4. Fox, S., Karnawat, K., Mydland, M., Dumais, S., & White, T. 2005. Evaluating implicit measures to improve web search. ACM Transactions on Informa-tion Systems . ACM TOIS.
5. Teevan, J., Dumais, S. T., & Liebling, D. J. 2008, July. To personalize or not to personalize: modeling queries with variation in user intent. ACM SIGIR.
6. Sontag, D., Collins-Thompson, K., Ben-nett, P. N., White, R. W., Dumais, S., & Billerbeck, B. 2012, February. Probabilistic models for personal-izing web search. ACM.
7. Craswell, N., Zoeter, O., Taylor, M., & Ramsey, B. 2008, February. An experimental compar-ison of click position-bias models. In Proceedings of the 2008 International Conference on Web Search and Data Mining. ACM.
