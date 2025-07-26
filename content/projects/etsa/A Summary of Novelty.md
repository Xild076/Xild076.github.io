## Existing Literature

### Limitations of Current ABSA Benchmarks
Most ABSA models are trained and evaluated on benchmark datasets such as SemEval (Pontiki et al., [2014](https://aclanthology.org/S14-2004/), [2015](https://aclanthology.org/S15-2082/), [2016](https://aclanthology.org/S16-1002/)), MAMS ([Jiang et al., 2019](https://aclanthology.org/D19-1654/)), and Twitter ([Vo et al., 2015](https://www.ijcai.org/Proceedings/15/Papers/194.pdf)). However, these benchmarks predominantly focus on sentence-level examples, lacking comprehensive document-level annotations. Given a random example pulled from the MAMS dataset—

```txt
The O -999
decor B-ASP Negative
Was O -999
not O -999
good O -999
at O -999
all O -999
but O -999
their O -999
food O -999
and O -999
amazing O -999
prices O -999
make O -999
up O -999
made O -999
it O -999
. O -999
````

(−999 means the token is not an aspect) —it is evident that the datasets used to train and benchmark most modern ABSA models fail to consider multiple entities and broader contextual understanding.

### Limitations of Transformer-Based ABSA Models

There are multiple transformer-based models adapted for ABSA, from BERT ([Devlin et al., 2019](https://arxiv.org/pdf/1810.04805)) to RoBERTa ([Liu et al., 2019](https://arxiv.org/pdf/1907.11692)), culminating in what can be considered the current SOTA model: PyABSA ([Yang et al., 2022](https://arxiv.org/pdf/2208.01368)), which provides plug-and-play implementations for a variety of neural ABSA architectures and basic ABSA functionality. While they are powerful, these systems are very limited. They suffer from three core limitations:

1. **Inability to operate on full-text input with sentiment shifts**  
Due to being a transformer model, the models are still somewhat able to retain context. For instance, with two sentences, it is still able to retain sentiment:

> **Example:**  
> Input: `"The individual was pure evil. [ASP]They[ASP] ate a candy"`  
> Output: `'sentiment': ['Negative'], 'confidence': [0.9839126467704773]`

However, this ability falls apart for longer inputs:

> **Example:**  
> Input: `"The initial setup for [ASP]the new software[ASP] was a bit confusing, and the manual wasn't very clear. I even encountered a few error messages. However, once I got past that initial hurdle, its performance was blazingly fast. It has streamlined my workflow considerably, and the advanced features are a game-changer. I'm now much more productive thanks to it."`  
> Output: `'sentiment': ['Negative'], 'confidence': [0.8788386583328247]`

With the addition of more context and a slight temporal shift in sentiment, the model is unable to properly grasp the sentiment progression. In a [micro-dataset](https://drive.google.com/file/d/14TwtppLsao0d2hbtBgNFwn2GgVljbJmS/view?usp=sharing) (see `long_text_limitation_showcase` and `entity_interaction_limitation_showcase`), the evaluated accuracy for each dataset of 10 sentences was 60% and 40% respectively and 50% collectively.

A highly likely reason for this trend is primacy bias within transformer models—the tendency to overweight earlier inputs and underweight later context which is seen very predominantly in BERT models ([Goel et al., 2025](https://arxiv.org/pdf/2412.15241)). This is an issue, however, as it fails to reflect human psychology, which tends to follow a serial position curve ([Murdock, 1962](https://psycnet.apa.org/doiLanding?doi=10.1037%2Fh0045106)), or a U shape with both first and last impressions being important.

2. **Failure to model sentiment interaction between entities** 
Many of the models fail to capture the nuances of the relationship between actions and entities. For instance, if entity A performed action B against entity C, the relationship between A, B, and C often goes unnoticed.

> **Example:**  
> Input: `"The [ASP]rescue team[ASP] battled treacherous weather conditions and unstable terrain for hours to reach the stranded hikers. Their perseverance in the face of such overwhelming natural obstacles was heroic and ultimately successful."`  
> Output: `'sentiment': ['Negative'], 'confidence': [0.49039655923843384]`

The given example illustrates the case well. The aspect, rescue team (a positive entity), performed the action, battled (a relatively negative verb), against the other aspect, treacherous weather conditions and unstable terrain (a negative entity). However, the transformer predicted a negative sentiment where, theoretically, performing a negative action against a negative entity should give a positive sentiment. In a [micro-dataset](https://drive.google.com/file/d/14TwtppLsao0d2hbtBgNFwn2GgVljbJmS/view?usp=sharing) (see `entity_interaction_limitation`), the evaluated accuracy for the dataset of 10 sentences was 70%.

This is extremely important because, more often than not, the texts upon which these tools operate involve complex inter-entity dynamics.

3. **Lack of valence scoring and sentiment granularity**  
The sentiment models, including PyABSA, only focus on sentiment polarity with three options: Positive, Negative, and Neutral instead of a more nuanced explanation of sentiment intensity.

### Graph-Based Sentiment Propagation
GNNs have emerged as a tool for capturing structural relationships in text, for instance, DyGIE++ ([Wadden et al., 2019](https://www.semanticscholar.org/paper/Entity%2C-Relation%2C-and-Event-Extraction-with-Span-Wadden-Wennberg/fac2368c2ec81ef82fd168d49a0def2f8d1ec7d8)) which utilized a dynamic span graph to extract relations and SenticGCN ([Liang et al., 2021](https://www.sentic.net/sentic-gcn.pdf)) or ASGCN ([Zhang et al., 2019](https://arxiv.org/pdf/1909.03477)) which builds graphs from dependencies to model the relationship between aspect terms and opinion words for ABSA. However, these models still fall short in several key areas:

1. **Limited long-text and temporal context evaluation**  
The models are mostly built on an individual sentence level (SentiGNC and ASGCN) and fail to capture shifts in sentiment over long texts. DyGIE++, which performs cross-sentence entity evaluations, does not provide sentiment analysis.

2. **Inadequate modeling**  
By focusing only on dependency paths, the models fail to look at deeper semantic relationships. As a result, they generally do not differentiate between the nature of various sentiment relations, for instance, how the verb/action 'attacked' impacts sentiment versus 'helped' when performed on different entities.

### Missing Granularity in Sentiment Analysis
Most sentiment classification systems output discrete polarity labels (positive, neutral, negative) or coarse-grained intensity scores. While tools like VADER ([Hutto & Gilbert, 2014](https://ojs.aaai.org/index.php/ICWSM/article/view/14550)) and CoreNLP's ([Manning et al., 2014](https://aclanthology.org/P14-5010.pdf)) sentiment module offer real-valued sentiment estimates, they do so in isolation from structured context. They cannot, for instance, distinguish between a positive sentiment toward a villain and a positive sentiment toward a hero. (e.g., “X helped Y” vs. “X helped the criminal”). Furthermore, in the specific area of ABSA, there are no relevant or SOTA models that perform sentiment classification with granularity.

### Summary
Thus, to summarize, the five main problems we found in existing ABSA models/tools and aim to solve with our pipeline are:
1. Lack of detailed, full-text level analysis
2. Failure to analyze temporal shifts in sentiment
3. Inadequacy in nuanced, inter-entity and semantic analysis
4. Lack of granularity and valence in ABSA analysis
5. Lack of explainability in ABSA models
## Our Proposed Pipeline
![image](ETSA%20Pipeline.png)  
Full Image: [[ETSA Pipeline.png]]

Our proposed methodology for entity-centric narrative analysis unfolds through a multi-stage pipeline designed to systematically extract and interpret complex textual information.

The initial stage, **Entity Identification and Coreference Resolution**, processes raw textual input to identify all mentions of entities (e.g., persons, organizations). Crucially, it resolves coreferences, linking various textual references to their canonical entity representations, thereby consolidating all mentions pertaining to a unique, underlying entity and noting their precise textual locations.

Following this, the **Entity-Associated Phrase (EAP) Extraction** stage builds upon the identified entities. It focuses on extracting descriptive words, phrases, or tokens directly pertinent to each entity. These EAPs serve to characterize the entity or describe its state or attributes, effectively enriching the entity representation with contextual details.

Subsequently, **Entity-Based Graph Mapping (EBGM)** transforms the processed text and entity information into a structured graph. In this representation, typically constructed on a sentence-by-sentence basis, entities are modeled as nodes, and their corresponding EAPs become node attributes. Furthermore, interactions, actions, or relationships between entities, as discerned from the text, are formalized as edges connecting the respective entity nodes, creating a relational understanding of the narrative.

The pipeline then proceeds to **Sentiment Analysis and Assignment**. This stage quantifies the sentiment associated with entities and their interactions within the graph. Sentiment scores are computed by considering contextual factors such as the positioning of sentiment-bearing terms, the directionality of sentiment, and the overall polarity of described events. The graph is thus augmented with these affective annotations, providing insight into the emotional tone surrounding entities and their relationships.

> **Example:** "Team Alpha, known for their brave actions and strategic planning, attacks Villain Corp while also protecting Civilians."
> **Output:** ![[Sentiment Graph.png]]

Finally, the **Sentiment Recursion and Evolution** stage models the dynamic changes in entity sentiment as the narrative progresses. Sentiment scores are not treated as static but are updated recursively. As new information, actions, or descriptions pertaining to an entity emerge in subsequent textual segments, its sentiment score is recalculated, allowing the system to capture temporal shifts and reflect the cumulative impact of unfolding events on the perceived sentiment.

This integrated pipeline provides a comprehensive framework for transforming unstructured text into a rich, structured representation, enabling a deeper understanding of the entities, their characteristics, their interactions, and the dynamic evolution of their associated sentiments throughout a narrative.
### Full Text Analysis
This pipeline solves for the first issue of full-text analysis by analyzing all of the sentences in a given document and combining the data. In doing so, it can capture the nuances of longer contexts, something of which current ASBA models can not.
### Temporal Shifts
Building off of the full-text analysis, by analysis all sentences independently and looking at how the sentiment interacts, the pipeline can properly analyze sentiment progression without primacy bias.
### Inter-entity Analysis
By focusing on specifically how entities interact with each other as the basis of the sentiment calculations, the pipeline can accurately determine how entity sentiment plays off each other, building a more accurate sentiment model.
### Granularity and Valence
Since the model are computed from tools that include inherent granularity and valence, the model inherits the traits and provides calculated sentiments. Due to the nature of sentiment interactions between entities and subtle shifts in sentiment direction, granularity and valence is necessary in the calculations the model uses.
### Explainability
By using rule-based methods where possible, creating heuristic sentiment calculations, by exporting every part of the sentiment calculation sequence in human-interpretable JSON files, the pipeline offers the explainability of sentiment calculations other transformer models fail to do.