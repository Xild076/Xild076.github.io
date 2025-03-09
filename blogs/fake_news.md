While looking into stuff I could add to Alitheia AI to improve it, I came across the idea of using ML to detect fake news, so I did some research into it. 

It turns out, there are much more ways to detect fake news using ML than I thought. In this blog post, I thought I'd look at a couple of these methods and give my own input on possible directions that this can be taken.

A paper, [*Detection of fake news from social media using support vector machine learning algorithms* by Sudhakar and Kaliyamurthie](https://www.sciencedirect.com/science/article/pii/S2665917424000047), included a comprehensive list of the most mainstream methods, of which included:

- Naive Bayes

- Logistic Regression

- Support Vector Machine

- Decision Tree

- Random Forest and K-Nearest Neighbor

- Convolutional Neural Networks

- Long Short-Term Memory

The results of the paper indicated that the best method was SVM, which sat at an accuracy of about 98%, while the worst was LSTM, which sat at an accuracy of about 54%. Logistic Regression also provided surprising accuracy at a rate of around 95%. SVM and Logistic Regression's success is consistent with the findings in other papers—[*Fake News Detection using Support Vector Machine* by Patel et al](https://www.scitepress.org/PublishedPapers/2021/105620/105620.pdf) found that out of NB, Decision Tree, Random Forest, Multinomial NB, Logistic Regression, and SVM, Logistic Regression and SVM were the most accurate at 94.92% and 94.93% accuracy respectively.

In fact, the highest accuracy I found for SVM was in [*Strengthening Fake News Detection: Leveraging SVM and Sophisticated Text Vectorization Techniques. Defying BERT?* by Karim et al](https://arxiv.org/html/2411.12703v1), where an optimized SVM method produced a 99.81% accuracy, which is remarkably high, especially since it was being compared to BERT, a transformer model.

However, I also came across another very interesting technique—a CNN-LSTM hybrid model approach discussed in [*LSTMCNN: A hybrid machine learning model to unmask fake news by* Dev et al](https://www.sciencedirect.com/science/article/pii/S2405844024012751). While the accuracy presented was only 98% compared to an optimized and intensively-trained SVM's 99.81%, the interesting thing was that within the paper, the CNN-LSTM hybrid model is compared to a Logistic Regression model with an accuracy of 95%. That would make it closer to the accuracy found in Patel et al's paper, meaning that relatively, SVM should be much less accurate compared to a CNN-LSTM hybrid model.

However, since there is no direct comparison with both models trained to the max, we can't be sure which one is the better one, although transformer models will likely still remain king.

From reading all those papers, the key takeaway I got was:

1. For the greatest cost-performance ratio, SVM is the best fake news detection method.
2. For a more intensive but more widely applicable and flexible method, CNN-LSTM hybrid models are the best.
3. For the most intensive but most accurate model, BERT is the best.

However, I do have a few thoughts and gripes about the current methodologies.

First, I believe that it is worth looking into more hybrid model options. I have a few random ideas for those: CNN-BiLSTM, CNN-SVM, and (Bi)LSTM-SVM. Since I'm only familiar with LSTM, I'm not sure I can explain the merit of the hybrid models, but I do think given patterns and trends I've seen within the models, these models could be worth a try. 

The second issue I have with current methodologies is the binary approach. Personally, I think that a binary approach is not accurate to what is necessary in the modern age. I believe that fake news and misinformation are more commonly half-lies or half-truths instead of full lies. For instance, while a piece of news may provide correct information on one part of the issue, it may provide incorrect information or just not provide information on another important part of the information. This presents a bit of an issue because, with a binary system for classifying news, a lot of nuance is lost within the sauce. 

I did find some good solutions—[*Toward Automatic Fake News Classification* by Souvick Ghosh and Chirag Shah](https://scholarspace.manoa.hawaii.edu/server/api/core/bitstreams/2eb9a917-e4dc-4371-bb5a-dd894001bf57/content) presented a ternary classification method which I believe accounts for a lot of the nuance needed by creating a "suspicious" section and [*"Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection* by William Wang](https://www.kaggle.com/datasets/doanquanvietnamca/liar-dataset) presented a good dataset with nuanced distinguishing of what news was almost true or almost false. 

All in all, I do believe that more research needs to be done and better methodologies need to be created, as misinformation is a growing and massively pressing issue.

Cheers!