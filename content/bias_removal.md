While working on Alitheia AI (once again lol), I came across an issue: how do you remove bias and subjectivity from a text without altering its fundemental meaning? In order to present information in the most objective way possible, this was a necessary step that I needed to take, but unfortunately, there was basically no research done on it.

When it came to objectifying sentences, I had two main ideas: 1. creating a rule-based algorithm to alter the text to improve objectivity and 2. fine-tuning summarization models to add the function of objectifying text.

Due to my inexperience in fine-tuning summarization models and the computational power necessary to do so (I do all my programming and processing on a MacBook Air with the occasional use of Collab), I ended up going with the first option.

Looking into things a bit more, I found some research that attempted to do similar things—[*Dbias: Detecting biases and ensuring Fairness in news articles* by Raza et al](https://arxiv.org/pdf/2208.05777) and [*Automatically Neutralizing Subjective Bias in Text* by Pryzant et al](https://nlp.stanford.edu/pubs/pryzant2020bias.pdf), though a few things about their methodology and results confused me.

The main issue I had with these projects was their complexity. While a comprehensive pipeline is definitely good for accuracy, the four-tiered BERT-based model in Dbias seemed a bit too computationally intensive to be run casually, and while Pryzant et al's methods were a more computationally friendly with just two larger BERT-based models used, overall, it was still relatively intensive. While using distilled versions may improve its efficiency, I still feel that there are better ways to go about this.

Another issue I had with the systems was the usage of a masking method to find word replacements. While masking methods are great at finding contextual fits, they often miss the point of the entire text. For instance, a text saying "They were elated." that masks "elated" ("They were [MASK].") could have a lot of things fit into that mask—"happy", "sad", "angry", and evidently some of those words don't fit due to context mismatches.

This issue is seen more prominently in Dbias, where the sentence "Billy Eilish issues apology for mouthing an anti-Asian derogatory term in resurface video." masked "mouthing" and "anti-Asian" ("Billy Eilish issues apology for [MASK] an [MASK] derogatory term in resurface video."), and while the masking makes sense, the results don't. While results varied for the word "mouthing", with the better ones being "using" and the worse ones being "wearing", the "anti-Asian" result made even less sense; the replacement was "intentional" all the way through. While the issues were more obvious in Dbias, the issues also showed themselves in Pryzant's work as they used the same masking methods. While I admit that larger models and more context do somewhat account for the issue, I do feel that given the computational cost-to-result ratio, using a BERT masking method is just not a good idea.

Thus, I decided to look into my own methods of improvement, one geared towards improved efficiency and accuracy in de-biasing.

The first issue comes with determining what actually causes subjectivity and bias within the text. Doing some research led me to [The University of Adelaide's *Objective Language Writing Centre Learning Guide*](https://www.adelaide.edu.au/writingcentre/ua/media/21/learningguide-objectivelanguage.pdf), which outlined the common points of subjectivity within writing:

- Personal language

- Judgmental language

- Emotive language

Personal language isn't as large of an issue in bias removal—in fact, I believe that personal language is pretty important for distinguishing opinion from perceived "fact", thus I will ignore it for now.

Judgemental and emotive language, on the other hand, are problematic issues. From what I can tell, these are found most predominantly in adjectives, adverbs, titular nouns, and verbs (not accounting for more structural system bias that may be more hidden). To debias, these words need to be altered. 

However, there needs to be a criterion to determine how to alter these words, as each word in a sentence has a property that may make it uniquely difficult to alter.

1. Structural value: Does the removal of the word impact the structure of the sentence?
2. Is the word subjective: Does the removal/alteration of the word improve bias, or is it an important descriptive word
3. Does the removal of this one word improve the subjectivity of the entire text: Sometimes, words can be subjective but prove to improve the overall objectivity of the text in rare cases. This also must be accounted for.

Thus, given this, it is decently straightforward to develop a rule-based objectivity based on NLP pipelines like NLTK and Stanza where words can be marked for change and removal.

Furthermore, for a word replacement, I thought to turn to the more unique method of synonym finding using a dictionary API. While this may not produce the same nuance, creating a list of words and checking for which word provides the most objective alternative, should hold up much better than a BERT-based model when it comes to retaining meaning.

All in all, while I kept the explanation of my methodology rather short, I do believe that it can serve as a different, more algorithmic approach to debiasing within the ML community, though I am no expert so I'd love to hear from anyone with more experience in this field about their perspective on my methodology.

More research definitely needs to be done in this area, though, with growing polarization often fueled by such bias-riddled rhetoric. But, that is a worry for tomorrow's me.

Cheers!