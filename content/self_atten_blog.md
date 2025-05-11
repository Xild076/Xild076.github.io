A while back, while working on Alitheia AI, I had the idea to apply self-attention to textual clustering after learning about what self-attention was. Unfortunately, I didn't know how to train the self-attention model then, so I left it untrained.

Surprisingly, however, the self-attention often somewhat improved the textual clarity of the clustering while also massively improving the cluster's scoring on a series of metrics. 

Thus, in this blog, I wanted to explore some possibilities as to why this may have occurred.

First and foremost, it turned out that my idea was not as novel as I thought it was as. There is an excellent paper about this topic that I will be using as reference for the rest of the blog: Lovedeep Singh's [Clustering Text Using Attention](https://arxiv.org/pdf/2201.02816).

Taking a look at Singh's results the average improvement of about 174.65% from baseline clustering to clustering after applying AP2 (attention clustering w/pre-trained embeddings and using 20% of data for training), which is certainly impressive. Furthermore, applying AP9 saw even more improvement, although variable.

However, the issue lies with the fact that when doing my own tests with an untrained self-attention model, I saw a consistent improvement of about 161.22%, which isn't too far off from Singh's result with trained models. 

That was surprising since theoretically, the untrained model should have seen, on average, no improvement in clustering, yet it showed consistent improvements. This got me thinking that maybe given how silhouette scores were calculated, any sort of self-attention, if consistent, could improve clustering.

The idea behind this depends on the fact that silhouette scores are calculated purely on a numerical basis and determined through relative similarity between clusters. Self-attention, meanwhile applies both amplifying and dampening weights, meaning that if applied consistently, certain similar sets of values will be decreased or increased. My belief is that given such effects, a sort of artificial dimensional reduction is applied. Due to some values being dampened into irrelevance, an effect similar to that of UMAP of PCA reduction might have occurred, resulting in greater cluster separability due to the algorithm having less nuance to worry about.

The issue with this is that such clustering doesn't actually guarantee better clustering since random words or phrases will be amplified. Thus, I can only chalk up the improved perceived clustering to luck, but I still need to do more tests on the perceived clustering improvements to be sure. Furthermore, I think it is necessary to find a better and more universal scoring metric for textual clustering in particular, as, otherwise, there won't be a consistent method to determine the validity of textual clusters.

All in all, the conclusion I came to was that self-attention is indeed a useful tool for improving textual clustering and that using silhouette scores as a scoring metric is not such a good idea. Overall, this was a very interesting topic to look into, and I think it is an area that needs a lot more research. 

Cheers!