This notebook aims to understand how sentiment is aimed at named entities

```python
import spacy
from spacy import displacy

from typing import Literal

nlp = spacy.load('en_core_web_sm')

def analyze_text_structures(text, style: Literal["dep", "ent"]):
    doc = nlp(text)
    displacy.render(doc, style=style, page=False)
```

Let's first consider transitive verbs constructions.

This text will serve as an example:

"Adam criticized John's horrible decisions."

Adam will have a netural/positive sentiment because Adam acted negatively upon the "horrible decision", which would turn positive.
John will have a negative sentiment as John is associated with "horrible decisions".

Now, let's check out how the dependancies work.

```python
analyze_text_structures("Adam criticized John's horrible decisions.", "dep")
```

Alright, so we have the following results.

The easy thing is finding the association between John and the negative sentiment. The primary source of negative sentiment comes from the term "horrible decisions", and since John associated with this negativity, then John is negative. However, since Adam is the subject criticizing Adam, then Adam is seen in a more positive light.

We can map this interaction out like this:

Subject Entity or Associated Entity (in this case nsubj) -> Verb -> Object Entity or Associated Entity (in this case dobj + poss)

However, for future reference, we can simply refer to this as Actor Clause -> Action -> Victim Clause.

Given that, the pattern I observe is so far is that:

Subj -> Positive Verb -> Obj (Negative Sentiment) = Negative Sentiment towards Subj
Subj -> Negative Verb -> Obj (Negative Sentiment) = Positive Sentiment towards Subj
Subj -> Positive Verb -> Obj (Positive Sentiment) = Positive Sentiment towards Subj
Subj -> Negative Verb -> Obj (Positive Sentiment) = Negative Sentiment towards Subj

Given all this, let's check out how the numbers would play out. For this analysis, I will be using VADER sentiment analysis.


```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

print(sia.polarity_scores("Adam criticized John's horrible decisions."))
print(sia.polarity_scores("Adam criticized"))
print(sia.polarity_scores("John's horrible decisions."))
```

```
{'neg': 0.667, 'neu': 0.333, 'pos': 0.0, 'compound': -0.7184}
{'neg': 0.714, 'neu': 0.286, 'pos': 0.0, 'compound': -0.3612}
{'neg': 0.636, 'neu': 0.364, 'pos': 0.0, 'compound': -0.5423}
```

From this, we can see two key things. First, the sentiment associated with John would be about -0.5423. However, what would the sentiment associated with Adam be?

While this may seem arbritrary, I simply multiplied the two together (as the sentiment patterns fit surprisingly well into math) to get a sentiment of about 0.19587876, or mildly positive.

However, there are still are two main conditions I don't understand: sentence structure and descriptive cases (descriptive voice means that "the sad person"—sad brings a negtive connotation but a positive verb towards the sad person would reflect well on the subject instead of negatively).

Given that, let's first look at the more straight-forward and possibly more difficult: sentence stucture. There are many different sentence structures, and determining the characters and their interactions is very difficult. However, we can boil it down to the very essentials to make things simpler: all we need to know is the actor and all associated clauses.

```python
analyze_text_structures("John's horrible decisions were criticized by Adam.", "dep")
```

```python
analyze_text_structures("Adam ordered John to stop eating in a late-night hateful rant.", "dep")
```

```python
analyze_text_structures("While ranting hatefully, Adam ordered John to stop eating.", "dep")
```

```python
analyze_text_structures("Adam, a horrible person, ordered John to stop eating.", "dep")
```

```python
analyze_text_structures("John was ordered to stop eating by Adam in a late-night hateful rant.", "dep")
```

```python
analyze_text_structures("While ranting hatefully, John was ordered to stop eating by Adam.", "dep")
```

Alright, so what do we see here?

Surprisingly, the patterns are pretty simple! 

First, in a passive voice scenario ("John's horrible decisions were criticized by Adam."): 
1. The Actor clause is Adam (pobj)
2. The Action is "were criticized by"
3. The Victim clause is John's horrible decisions (nsubjpass)

Next, in an active voice complex sentence with a final prepositional phrase modifier ("Adam ordered John stop eating in a late-night hateful rant."):
This case is a little more special because we have the added on "in a late-night hateful rant". This can either belong to the actor clause or the victim clause, so let's take a look at another sentence to be sure.

This is the passive voice version of the sentence: "John was ordered to stop eating by Adam in a late-night hateful rant." In this case, it seems that "in a late-night hateful rant" is once again associated with Adam, implying that a final prepositional phrase modifier is more commonly associated with the active actor instead of the subject. 

Thus, for both, we can determine that:
1. The Actor clause is Adam (nsubj/pobj) and "in a late-night hateful rant" (prep)
2. The Action is "ordered"/"was ordered" and "to stop eating" (xcomp)
3. The Victim clause is "John" (dobj/nsubjpass)

Now, let's look at a similar case but with "While ranting hatefully, John was ordered to stop eating by Adam." and "While ranting hatefully, Adam ordered John to stop eating."
For this one, the dependent clause (advcl) seems to always be associated with the nsubj in some way. 

Thus, it can be determined that for the first sentence:
1. The Actor clause is Adam (pobj)
2. The Action is "was ordered to stop eating"
3. The Victim clause is "While ranting hatefully" (advcl) and "John" (nsubjpass)

Meanwhile, for the second sentence:
1. The Actor clause is "While ranting hatefully" (advcl) and "Adam" (nsubj)
2. The Action is "ordered" and "to stop eating" (xcomp)
3. The Victim clause is "John"

Finally, let's look at "Adam, a horrible person, ordered John to stop eating."
This one was actually way simpler than all the other ones as "a horrible person" was associated to Adam with appos. That means that we can easily determine that:
1. The Actor clause is "Adam, a horrible person,"
2. The Action is "ordered" and "to stop eating" (xcomp)
3. The Victim clause is "John"

Thus, we have the general rules:
1. The Actor clause is the clause of the actor/perpetrator who performs the action
    - Associated information includes anything attached with advcl, poss, or prep
    - There are possibly more rules involved, just ones I haven't discovered yet
2. The Action is the verb and associated information with xcomp.
3. The Victim clause is the clause of the victim/reviever who recieves the action
    - Associated information includes anything attached with advcl, or poss
4. Any named entities within each of the clauses will be associated with the sentiment of the clauses as a whole.

Now the curiosity comes in when we have to try to find sentiments. We established before that we have to multiply the sentiment of the Victim clause with the sentiment of the Actor + Action clauses. However, things became slightly more muddled since, with the advent of sentiment within the actor clause, we need to see how this affects the sentence as a whole.

Let's take a look at three cases.

```python
# John's horrible decisions were criticized by Adam.
print(sia.polarity_scores("Adam ordered John to stop eating in a late-night hateful rant."))
print(sia.polarity_scores("Adam in a late-night hateful rant")) # Actor clause
print(sia.polarity_scores("Adam ordered in a late-night hateful rant")) # Actor clause + Action
print(sia.polarity_scores("Adam ordered to stop eating")) # Actor clause subject + Action
print(sia.polarity_scores("John")) # Victim clause

print()

# While ranting hatefully, John was ordered to stop eating by Adam.
print(sia.polarity_scores("While ranting hatefully, John was ordered to stop eating by Adam."))
print(sia.polarity_scores("While ranting hatefully, John")) # Victim clause
print(sia.polarity_scores("Adam")) # Actor clause
print(sia.polarity_scores("was ordered to stop eating by Adam.")) # Actor clause + Action
print(sia.polarity_scores("was ordered to stop eating by Adam.")) # Actor clause subject + Action


print()

# Adam, a horrible person, ordered John to stop eating.
print(sia.polarity_scores("Adam, a horrible person, ordered John to stop eating."))
print(sia.polarity_scores("Adam, a horrible person,")) # Actor clause
print(sia.polarity_scores("Adam, a horrible person, ordered")) # Actor clause + Action
print(sia.polarity_scores("Adam ordered")) # Actor clause subject + Action
print(sia.polarity_scores("John to stop eating.")) # Victim clause
```

```
{'neg': 0.494, 'neu': 0.506, 'pos': 0.0, 'compound': -0.7783}
{'neg': 0.583, 'neu': 0.417, 'pos': 0.0, 'compound': -0.6808}
{'neg': 0.528, 'neu': 0.472, 'pos': 0.0, 'compound': -0.6808}
{'neg': 0.355, 'neu': 0.645, 'pos': 0.0, 'compound': -0.296}
{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

{'neg': 0.379, 'neu': 0.621, 'pos': 0.0, 'compound': -0.6705}
{'neg': 0.524, 'neu': 0.476, 'pos': 0.0, 'compound': -0.5106}
{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
{'neg': 0.268, 'neu': 0.732, 'pos': 0.0, 'compound': -0.296}
{'neg': 0.268, 'neu': 0.732, 'pos': 0.0, 'compound': -0.296}

{'neg': 0.449, 'neu': 0.551, 'pos': 0.0, 'compound': -0.6908}
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}
{'neg': 0.467, 'neu': 0.533, 'pos': 0.0, 'compound': -0.5423}
{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
{'neg': 0.423, 'neu': 0.577, 'pos': 0.0, 'compound': -0.296}
```

Okay, we have some interesting numbers to play with.

Now, I split the the sentiments into 4 different types: Actor clause, Actor clause + Action, Actor clause subject + Action, and Victim clause. 

The only three important ones are Actor clause, Actor clause subject + Action, and Victim clause.

The new one here is Actor clause subject + Action. Previously, I used Actor clause + Action, however, I realized that this meant that I couldn't get what the verb is actually implying, I decided to purely use the Actor clause subject with the action to determine the sentiment of the action. 

So, we have the following information (using "Adam ordered John stop eating in a late-night hateful rant." as an example):
- The Actor clause ("Adam in a late-night hateful rant") -> -0.6808 (AC)
- The Actor clause subject + action ("Adam ordered to stop eating") -> -0.296 (ACS+A)
- The Victim clause ("John") -> 0.0 (VC)

So, how do we calculate sentiment? First, let's get a sense of what sentiment we should feel towards each character. Adam should face a very negative sentiment while John face a positive one. So, how do we achieve that?

Well, going off of the previous one, to get the Actor clause sentiment, we would multiple the ACS+A with the VC to get 0.0 and average it with AC, but that seems odd, as aiming a negative sentiment at a neutral target would normally be considered a negative thing to do. However, let's just go with it for now. The results would come out to be a compound -0.3404 sentiment for AC.

Meanwhile, doing the opposite for the VC, the we would multiply ASC+A with AC to get a compound 0.1007584 sentiment for the VC. That seems pretty accurate.

Thus, we can derive the equation to calculate entity sentiment:

Compound A/VC Sentiment = (V/AC * ASC+A + A/VC) / 2

Pretty neat, pretty simple, though it does decrease the sentiment intensity. For now, we have a pretty simple way to semi-reliably calculate the sentiment aimed at an entity!

Now, though, let's list out and tackle the big three issues all at once.
- Descriptive (ex: happy, sad, tall, short) vs Evaluative (ex: horrible, bad, good, helpful) descriptors
- Sentiment mitigation and neutral sentiment cases
- VADER's failures.

First, let's solve the easiest issue: Vader's failures. 

The thing about Vader is that Vader:
1. Fails to understand things like sarcasm
2. Has a massively limited wordbank and range (especially compared to newer tools)

We can ignore the first issue as we aren't too worried about sarcasm right now since our focus is determining sentiment target rather than textual nuances.

However, the second issue is a pretty big problem. Just take a look at how it handles these sentences:
```

```python
print(sia.polarity_scores("Adam ordered."))
print(sia.polarity_scores("Adam had a freak-out."))
print(sia.polarity_scores("Adam did harmful things."))
```

```
{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
```

Well... the first one makes sense but the other two are just ridiculous. "Harmful" and "freak-out" are definately negative.

Now, let's try to solve this! Solving this is pretty simple—let's just look at other tools instead and agregate a solution together! Let's use the same three examples.

```python
from textblob import TextBlob
from afinn import Afinn

print("Textblob sentiment:", TextBlob("Adam ordered.").sentiment)
print("Textblob sentiment:", TextBlob("Adam had a freak-out.").sentiment)
print("Textblob sentiment:", TextBlob("Adam did harmful things.").sentiment)

print()

afn = Afinn()

print("AFINN sentiment:", afn.score_with_wordlist("Adam ordered."))
print("AFINN sentiment:", afn.score_with_wordlist("Adam had a freak-out."))
print("AFINN sentiment:", afn.score_with_wordlist("Adam did harmful things."))
```

```
Textblob sentiment: Sentiment(polarity=0.0, subjectivity=0.0)
Textblob sentiment: Sentiment(polarity=0.0, subjectivity=0.0)
Textblob sentiment: Sentiment(polarity=0.0, subjectivity=0.0)

AFINN sentiment: 0.0
AFINN sentiment: -2.0
AFINN sentiment: -2.0
```

Well... these results don't look good for textblob, though they look better for AFINN, which makes sense, since AFINN operates purely on the words in the sentences.

So, how do we aggregate these results? Once again, while this may be crude, I decided to normalize AFINN with the total number of words tested, dividing them over 5, and average them with the Vader scores.

```python
import nltk
afn = Afinn()
sia = SentimentIntensityAnalyzer()

def normalized_afinn_score(text):
    tokens = nltk.word_tokenize(text)
    word_scores = [afn.score(word) for word in tokens]
    relevant_scores = [s for s in word_scores if s != 0]
    if relevant_scores:
        return sum(relevant_scores) / len(relevant_scores) / 5
    return 0

def get_sentiment(text):
    afn_score = normalized_afinn_score(text)
    polarity_score = sia.polarity_scores(text)['compound']
    return (afn_score + polarity_score) / 2

test_text = "Adam had a freak-out and did harmful things."

print("Aggregate sentiment:", get_sentiment(test_text))
print("AFINN sentiment:", normalized_afinn_score(test_text))
print("Polarity sentiment:", sia.polarity_scores(test_text))
```

```
Aggregate sentiment: -0.2
AFINN sentiment: -0.4
Polarity sentiment: {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
```

I'll be the first to admit that this is more than just "cobbled together", this is downright falling apart. But it's good enough for now, so let's move on to tacklign issue #2: sentiment mitigation and neutral sentiment cases.

Let's go back to the Adam example.
- The Actor clause ("Adam in a late-night hateful rant") -> -0.6808 (AC)
- The Actor clause subject + action ("Adam ordered to stop eating") -> -0.296 (ACS+A)
- The Victim clause ("John") -> 0.0 (VC)

Given:
Compound A/VC Sentiment = (V/AC * ASC+A + A/VC) / 2,
as mentioned before, the sentiment multiplied together would be 0.0 * -0.6808 = 0, which makes no sense. After all, taking action against a neutral individual is still negative. Thus, I decided to modify the equation slightly to reflect this by giving an addative to the compount sentiments and by adding a 1/3 weighing ratio:

Compound A/VC Sentiment = ((V/AC + 1) * ASC+A + A/VC * 3) / 4, V/AC >= 0
Compound A/VC Sentiment = ((V/AC - 1) * ASC+A + A/VC * 3) / 4, V/AC < 0

I did this because: 
- Adding/subtracting 1 would ensure that biases don't get unnecessarily mitigated
- Putting them on a ratio ensures that independent sentiment, which usually leaves a higher impression, is put to greater effect.

Now that is a bit better. Furthermore, this actually also solves the issue of sentiment mitigation as when before, the average would always decrease due to |V/AC| always being less than 1, now the average can increase as |V/AC| can be greater than 1. Let's put this into code.

```python
def calculate_compound_sentiment(base_sentiment, other_sentiment, action_sentiment):
    if other_sentiment >= 0:
        compound_sentiment = ((other_sentiment + 1) * action_sentiment + base_sentiment * 3) / 4
    else:
        compound_sentiment = ((other_sentiment - 1) * action_sentiment + base_sentiment * 3) / 4
    return compound_sentiment

print("Actor sentiment (Adam example):", calculate_compound_sentiment(-0.6808, 0.0, -0.296))
print("Victim sentiment (Adam example):", calculate_compound_sentiment(0.0, -0.6808, -0.296))

print()

# Positive -> positive -> positive case
print("Positive -> positive -> positive")
text = "The kind man positively helped the nice children."
ac = "The kind man"
asca = "positively helped"
vc = "the nice children"

ac_s = get_sentiment(ac)
asca_s = get_sentiment(asca)
vc_s = get_sentiment(vc)

print("AC sentiment:", ac_s)
print("ASCA sentiment:", asca_s)
print("VC sentiment:", vc_s)
print("Compound Actor sentiment (Random test):", calculate_compound_sentiment(ac_s, asca_s, vc_s))
print("Compound Victim sentiment (Random test):", calculate_compound_sentiment(vc_s, asca_s, ac_s))

print()

# Positive -> positive -> negative case
print("Positive -> positive -> negative")
text = "The kind man positively helped the evil villians."
ac = "The kind man"
asca = "positively helped"
vc = "the evil villians"

ac_s = get_sentiment(ac)
asca_s = get_sentiment(asca)
vc_s = get_sentiment(vc)

print("AC sentiment:", ac_s)
print("ASCA sentiment:", asca_s)
print("VC sentiment:", vc_s)
print("Compound Actor sentiment (Random test):", calculate_compound_sentiment(ac_s, asca_s, vc_s))
print("Compound Victim sentiment (Random test):", calculate_compound_sentiment(vc_s, asca_s, ac_s))

print()

# Positive -> positive -> negative case
print("Positive -> negative -> positive")
text = "The kind man sucker punched the nice children."
ac = "The kind man"
asca = "sucker punched"
vc = "the nice children"

ac_s = get_sentiment(ac)
asca_s = get_sentiment(asca)
vc_s = get_sentiment(vc)

print("AC sentiment:", ac_s)
print("ASCA sentiment:", asca_s)
print("VC sentiment:", vc_s)
print("Compound Actor sentiment (Random test):", calculate_compound_sentiment(ac_s, asca_s, vc_s))
print("Compound Victim sentiment (Random test):", calculate_compound_sentiment(vc_s, asca_s, ac_s))

print()

# Positive -> negative -> negative case
print("Positive -> negative -> negative")
text = "The kind man sucker punched the evil villians."
ac = "The kind man"
asca = "sucker punched"
vc = "the evil villians"

ac_s = get_sentiment(ac)
asca_s = get_sentiment(asca)
vc_s = get_sentiment(vc)

print("AC sentiment:", ac_s)
print("ASCA sentiment:", asca_s)
print("VC sentiment:", vc_s)
print("Compound Actor sentiment (Random test):", calculate_compound_sentiment(ac_s, asca_s, vc_s))
print("Compound Victim sentiment (Random test):", calculate_compound_sentiment(vc_s, asca_s, ac_s))

print()

# Negative -> negative -> negative case
print("Negative -> negative -> negative")
text = "The evil warlord brutally murdered the cruel dictator."
ac = "The evil warlord"
asca = "brutally murdered"
vc = "the cruel dictator"

ac_s = get_sentiment(ac)
asca_s = get_sentiment(asca)
vc_s = get_sentiment(vc)

print("AC sentiment:", ac_s)
print("ASCA sentiment:", asca_s)
print("VC sentiment:", vc_s)
print("Compound Actor sentiment (Random test):", calculate_compound_sentiment(ac_s, asca_s, vc_s))
print("Compound Victim sentiment (Random test):", calculate_compound_sentiment(vc_s, asca_s, ac_s))
```

```
Actor sentiment (Adam example): -0.5845999999999999
Victim sentiment (Adam example): 0.1243792

Positive -> positive -> positive
AC sentiment: 0.46335
ASCA sentiment: 0.46335
VC sentiment: 0.51075
Compound Actor sentiment (Random test): 0.534364003125
Compound Victim sentiment (Random test): 0.552573305625

Positive -> positive -> negative
AC sentiment: 0.46335
ASCA sentiment: 0.46335
VC sentiment: -0.62985
Compound Actor sentiment (Random test): 0.11708975062500002
Compound Victim sentiment (Random test): -0.30287669437500003

Positive -> negative -> positive
AC sentiment: 0.46335
ASCA sentiment: -0.26335
VC sentiment: 0.51075
Compound Actor sentiment (Random test): 0.18619849687499998
Compound Victim sentiment (Random test): 0.23671919437500002

Positive -> negative -> negative
AC sentiment: 0.46335
ASCA sentiment: -0.26335
VC sentiment: -0.62985
Compound Actor sentiment (Random test): 0.546442749375
Compound Victim sentiment (Random test): -0.618730805625

Negative -> negative -> negative
AC sentiment: -0.62985
ASCA sentiment: -0.72775
VC sentiment: -0.59295
Compound Actor sentiment (Random test): -0.21627015937500005
Compound Victim sentiment (Random test): -0.17265666562499998
```

And the results are pretty satisfactory, each example relatively accurately illustrate how the sentiment should play out.

Now, let's get to the final and (possibly) most difficult part: determining the difference between descriptive and evaluative words.

First, let's define the difference between descriptive and evaluative words. Descriptive words are primarily words that observe versus evaluative words being words that judge. This chart below contains a few examples:

| Descriptive | Evaluative |
| ----- | ----- |
| Tall, short, loud, quiet | nice, bad, corrupt, amazing |

Now let's look at what the sentiment analyzers say about them!

```python
print("Descriptive:")

print("\nTall:")
print("Afinn score:", afn.score("tall"))
print("Vader score:", sia.polarity_scores("tall"))

print("\nShort:")
print("Afinn score:", afn.score("short"))
print("Vader score:", sia.polarity_scores("short"))

print("\nLoud:")
print("Afinn score:", afn.score("loud"))
print("Vader score:", sia.polarity_scores("loud"))

print("\nQuiet:")
print("Afinn score:", afn.score("quiet"))
print("Vader score:", sia.polarity_scores("quiet"))

print("\n\nEvaluative")

print("\nNice:")
print("Afinn score:", afn.score("nice"))
print("Vader score:", sia.polarity_scores("nice"))

print("\nBad:")
print("Afinn score:", afn.score("bad"))
print("Vader score:", sia.polarity_scores("bad"))

print("\nCorrupt:")
print("Afinn score:", afn.score("corrupt"))
print("Vader score:", sia.polarity_scores("corrupt"))

print("\nAmazing:")
print("Afinn score:", afn.score("amazing"))
print("Vader score:", sia.polarity_scores("amazing"))
```

```
Descriptive:

Tall:
Afinn score: 0.0
Vader score: {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

Short:
Afinn score: 0.0
Vader score: {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

Loud:
Afinn score: 0.0
Vader score: {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

Quiet:
Afinn score: 0.0
Vader score: {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}


Evaluative

Nice:
Afinn score: 3.0
Vader score: {'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4215}

Bad:
Afinn score: -3.0
Vader score: {'neg': 1.0, 'neu': 0.0, 'pos': 0.0, 'compound': -0.5423}

Corrupt:
Afinn score: -3.0
Vader score: {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

Amazing:
Afinn score: 4.0
Vader score: {'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.5859}
```

Well... how surprising! It turns out: the perceived issue wasn't an issue at all! AFINN and Vader had it covered! That means that all three major issues in calculating sentiment have been completed.

However, we am not done yet! There are still two things we need to do:

First, remember how we split everything into: Actor Clause -> Action -> Victim Clause? Well, we need to figure out how to do that.

Secondly, we need to consider everything that doesn't fall under the category of transitive verbs constructions, which is basically just any sentence without a direct object. Getting sentiment for these types of sentences are pretty easy, but we need to be able to be able to locate independant clauses and the such to actually properly calculate sentiment.

That being said, let's get started with the first issue.

First, I had a quick look through all the sentences to extract the patterns and they ended up below.

Active Voice:
- Actor: nsubj and all subtrees
- Action: Verb + xcomp (excluding prep subtrees)
- Victim: dobj and all subtrees

Passive Voice:
- Actor: pobj and all subtrees
- Action: Verb + auxpass + agent
- Victim: nsubjpass and all subtrees

Active Voice + Final Prepositional Phrase Modifier:
- Actor: nsubj and all subtrees + prep
- Action: Verb + xcomp (excluding prep subtrees)
- Victim: dobj and all subtrees

Active Voice (Complex Sentence):
- Actor: nsubj and all subtrees + advcl and all subtrees
- Action: Verb + xcomp (excluding prep subtrees)
- Victim: dobj and all subtrees

Passive Voice + Final Prepositional Phrase Modifier:
- Actor: pobj and all subtrees + prep
- Action: Verb + xcomp (excluding prep subtrees)
- Victim: nsubjpass and all subtrees

Passive Voice (Complex Sentence):
- Actor: dobj and all subtrees
- Action: Verb + xcomp (excluding prep subtrees)
- Victim: advcl + nsubjpass

```python
def get_sentence_root(doc):
    return [sent.root for sent in doc.sents]

def get_tokens_by_dependencies(doc, target_deps):
    return [token for token in doc if token.dep_ in target_deps]

def get_full_subtree(token, exclude_branch_types=[]):
    subtree_tokens = []
    def traverse_subtree(token):
        if token.dep_ not in exclude_branch_types:
            subtree_tokens.append(token)
            for child in token.children:
                traverse_subtree(child)
    traverse_subtree(token)
    return sorted(subtree_tokens, key=lambda t: t.i)

def has_dependency(doc, target_dep):
    return any(token.dep_ == target_dep for token in doc)

def extract_named_entities_token(tokens):
    if not tokens:
        return []
    allowed_labels = {"PERSON", "ORG", "GPE", "NORP", "FAC", "PRODUCT", "EVENT", "LOC", "WORK_OF_ART", "LAW", "LANGUAGE"}
    token_idxs = {t.i for t in tokens}
    doc = tokens[0].doc
    return [ent.text for ent in doc.ents if ent.label_ in allowed_labels and any(t.i in token_idxs for t in ent)]

def extract_named_entities(doc):
    allowed_labels = {"PERSON", "ORG", "GPE", "NORP", "FAC", "PRODUCT", "EVENT", "LOC", "WORK_OF_ART", "LAW", "LANGUAGE"}
    return [ent.text for ent in doc.ents if ent.label_ in allowed_labels]

def split_into_independent_clauses(text):
    doc = nlp(text)
    clauses = []
    for sent in doc.sents:
        tokens = list(sent)
        split_indices = []
        for i, token in enumerate(tokens):
            if token.dep_ == "cc" and token.head == sent.root:
                split_indices.append(i)
        if not split_indices:
            clauses.append(sent.text.strip())
        else:
            start = 0
            for idx in split_indices:
                clause_tokens = tokens[start:idx]
                if clause_tokens and clause_tokens[0].text.lower() in {"and", "or", "but"}:
                    clause_tokens = clause_tokens[1:]
                clause_text = " ".join(t.text for t in clause_tokens).strip()
                if clause_text:
                    clauses.append(clause_text)
                start = idx + 1
            clause_tokens = tokens[start:]
            if clause_tokens and clause_tokens[0].text.lower() in {"and", "or", "but"}:
                clause_tokens = clause_tokens[1:]
            clause_text = " ".join(t.text for t in clause_tokens).strip()
            if clause_text:
                clauses.append(clause_text)
    return clauses

def extract_ac_asca_vc(text):
    doc = nlp(text)
    if has_dependency(doc, 'nsubj') and has_dependency(doc, 'dobj'):
        ac_base = get_tokens_by_dependencies(doc, ['nsubj'])
        ac_base_subtree = get_full_subtree(ac_base[0])
        ac_prep_base = get_tokens_by_dependencies(doc, ['prep'])[0] if get_tokens_by_dependencies(doc, ['prep']) else None
        ac_prep_base_subtree = get_full_subtree(ac_prep_base) if ac_prep_base else []
        ac_advcl_base = get_tokens_by_dependencies(doc, ['advcl'])[0] if get_tokens_by_dependencies(doc, ['advcl']) else None
        ac_advcl_base_subtree = get_full_subtree(ac_advcl_base) if ac_advcl_base else []
        ac_full = ac_base_subtree + ac_prep_base_subtree + ac_advcl_base_subtree
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])
        
        a_base = get_sentence_root(doc)
        a_base_subtree = get_full_subtree(a_base[0], ["nsubj", "dobj", "prep", "advcl", "dative"])
        a_full = sorted(a_base_subtree, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])
        
        asca_full = ac_base + a_full
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])

        vc_base = get_tokens_by_dependencies(doc, ['dobj'])
        vc_base_subtree = get_full_subtree(vc_base[0])
        vc_dative_base = get_tokens_by_dependencies(doc, ['dative'])
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = vc_base_subtree + vc_dative_base_subtree
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])

        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)

        return ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim
    elif has_dependency(doc, 'nsubjpass') and has_dependency(doc, 'pobj'):
        ac_base = get_tokens_by_dependencies(doc, ['pobj'])
        ac_base_subtree = get_full_subtree(ac_base[0])
        full_prep_tokens = get_tokens_by_dependencies(doc, ['prep'])
        ac_prep_base = full_prep_tokens[-1] if len(full_prep_tokens) > 1 else full_prep_tokens[0]
        ac_prep_base_subtree = get_full_subtree(ac_prep_base) if ac_prep_base else []
        ac_full = ac_base_subtree + ac_prep_base_subtree if len(full_prep_tokens) > 1 else ac_prep_base_subtree
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])

        a_base = get_sentence_root(doc)
        a_base_subtree = get_full_subtree(a_base[0], ["nsubjpass", "pobj", "prep", "advcl", "dative"])
        a_full = sorted(a_base_subtree, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])

        asca_full = [ac_base[0], get_tokens_by_dependencies(doc, ['prep'])[0]] + a_full
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])

        vc_base = get_tokens_by_dependencies(doc, ['nsubjpass'])
        vc_base_subtree = get_full_subtree(vc_base[0])
        vc_dative_base = get_tokens_by_dependencies(doc, ['dative'])
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = vc_base_subtree + vc_dative_base_subtree
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])

        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)
        return ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim
    else:
        return "", "", "", "", [], []
```

Given all of that, we have a basic rule-based method for transitive verbs constructions! Yay! Just as a disclaimer though: This is completely cobbled together and in no way accurate/proper. That being said, let's start testing.

```python
# Test cases
print(extract_ac_asca_vc("Adam and Alice ordered John to stop eating in a late-night hateful rant."))
print(extract_ac_asca_vc("While ranting hatefully, Adam ordered John to stop eating."))
print(extract_ac_asca_vc("Adam, a horrible person, ordered John to stop eating."))
print(extract_ac_asca_vc("John was ordered to stop eating by Adam in a late-night hateful rant."))
print(extract_ac_asca_vc("While ranting hatefully, John was ordered to stop eating by Adam."))

print()

# Actual example texts from 
print(extract_ac_asca_vc("The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history."))
print(extract_ac_asca_vc("The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects."))
```

```
('Adam and Alice in a late - night hateful rant', 'ordered to stop eating .', 'Adam ordered to stop eating .', 'John', ['Adam', 'Alice'], ['John'])
('While ranting hatefully Adam', ', ordered to stop eating .', ', Adam ordered to stop eating .', 'John', ['Adam'], ['John'])
('Adam , a horrible person ,', 'ordered to stop eating .', 'Adam ordered to stop eating .', 'John', ['Adam'], ['John'])
('Adam in a late - night hateful rant', 'was ordered to stop eating .', 'was ordered to stop eating by Adam .', 'John', ['Adam'], ['John'])
('by Adam', ', was ordered to stop eating .', ', was ordered to stop eating by Adam .', 'John', ['Adam'], ['John'])

('The best road trip in in Boston Boston history history', 'has given .', 'trip has given .', 'the Celtics a chance at grabbing a piece of NBA history', ['Boston'], ['Celtics', 'NBA'])
('The wasp ’s of the carnivorous Venus flytrap plant , which snaps shut to to digest digest unsuspecting unsuspecting insects insects', 'resemble .', 'wasp hairs resemble which snaps .', 'the structure of the carnivorous Venus flytrap plant , which snaps shut to digest unsuspecting insects', ['Venus'], ['Venus'])
```

Well, we have some successes and some failures, which is natural as the rule-based structure needs to be continuously updated, something of which I will continue to do later on. However, for now, it is generally satisfactory, though it fails real-world tests. That being said, let's get to the second issue: anything that doesn't fall under the category of transitive verbs constructions. The solution to this is very easy—as there aren't two different verbs, sentiment can only be aimed at a single thing! So let's update some things real quick.

```python
def extract_ac_asca_vc(text):
    doc = nlp(text)
    if has_dependency(doc, 'nsubj') and has_dependency(doc, 'dobj'):
        ac_base = get_tokens_by_dependencies(doc, ['nsubj'])
        ac_base_subtree = get_full_subtree(ac_base[0])
        ac_prep_base = get_tokens_by_dependencies(doc, ['prep'])[0] if get_tokens_by_dependencies(doc, ['prep']) else None
        ac_prep_base_subtree = get_full_subtree(ac_prep_base) if ac_prep_base else []
        ac_advcl_base = get_tokens_by_dependencies(doc, ['advcl'])[0] if get_tokens_by_dependencies(doc, ['advcl']) else None
        ac_advcl_base_subtree = get_full_subtree(ac_advcl_base) if ac_advcl_base else []
        ac_full = ac_base_subtree + ac_prep_base_subtree + ac_advcl_base_subtree
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])
        
        a_base = get_sentence_root(doc)
        a_base_subtree = get_full_subtree(a_base[0], ["nsubj", "dobj", "prep", "advcl", "dative"])
        a_full = sorted(a_base_subtree, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])
        
        asca_full = ac_base + a_full
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])

        vc_base = get_tokens_by_dependencies(doc, ['dobj'])
        vc_base_subtree = get_full_subtree(vc_base[0])
        vc_dative_base = get_tokens_by_dependencies(doc, ['dative'])
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = vc_base_subtree + vc_dative_base_subtree
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])

        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)

        return {'type': 'tvc', 'output': (ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim)}
    elif has_dependency(doc, 'nsubjpass') and has_dependency(doc, 'pobj'):
        ac_base = get_tokens_by_dependencies(doc, ['pobj'])
        ac_base_subtree = get_full_subtree(ac_base[0])
        full_prep_tokens = get_tokens_by_dependencies(doc, ['prep'])
        ac_prep_base = full_prep_tokens[-1] if len(full_prep_tokens) > 1 else full_prep_tokens[0]
        ac_prep_base_subtree = get_full_subtree(ac_prep_base) if ac_prep_base else []
        ac_full = ac_base_subtree + ac_prep_base_subtree if len(full_prep_tokens) > 1 else ac_prep_base_subtree
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])

        a_base = get_sentence_root(doc)
        a_base_subtree = get_full_subtree(a_base[0], ["nsubjpass", "pobj", "prep", "advcl", "dative"])
        a_full = sorted(a_base_subtree, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])

        asca_full = [ac_base[0], get_tokens_by_dependencies(doc, ['prep'])[0]] + a_full
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])

        vc_base = get_tokens_by_dependencies(doc, ['nsubjpass'])
        vc_base_subtree = get_full_subtree(vc_base[0])
        vc_dative_base = get_tokens_by_dependencies(doc, ['dative'])
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = vc_base_subtree + vc_dative_base_subtree
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])

        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)
        return {'type': 'tvc', 'output': (ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim)}
    else:
        return {'type': 'ntvc', 'output': (doc.text, "", "", "", extract_named_entities(doc), "")}
```

Let's try this out.

```python
print(extract_ac_asca_vc("Jerry was very upset and sad."))
```

```
{'type': 'ntvc', 'output': ('Jerry was very upset and sad.', '', '', '', ['Jerry'], '')}
```

Yup, works as expected.

Thus, the barebones of the project is complete. We have a basic, heuristic, rule-based method to calculate enitty-targeted sentiment! Yay!

However, as always, this isn't perfect. The main thing we need to improve is the rule-based actor-action-victim extraction and everything will be set. But for now, let's get to refining.

```python
analyze_text_structures("The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history.", "dep")
```

```python
analyze_text_structures("The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects.", "dep")
```

For the first text, these should be the clauses:
- AC: "The best road trip in Boston history"
- A: "has given"
- VC: "the Celtics a chance at grabbing a piece of NBA history."

For the second text, these should be the clauses:
- AC: "The wasp’s flaps and teeth-like hairs"
- A: "resemble"
- VC: "the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects."

It seems, thus, the big issue within our code is that we don't go off of the root of the text. So let's try that out.

```python
def get_conjuncts(token):
    result = []
    for child in token.children:
        if child.dep_ == "conj":
            result.append(child)
            result.extend(get_conjuncts(child))
    return result

def get_subtree_dependents_by_dep(token, allowed_deps):
    result = []
    for child in token.children:
        if child.dep_ in allowed_deps:
            result.append(child)
            result.extend(get_conjuncts(child))
            result.extend(get_subtree_dependents_by_dep(child, allowed_deps))
    return result

def get_full_subtree(token, exclude_branch_types=[], excluded_tokens=[]):
    subtree_tokens = []
    def traverse_subtree(token):
        if token in excluded_tokens:
            return
        if token.dep_ not in exclude_branch_types:
            subtree_tokens.append(token)
            for child in token.children:
                traverse_subtree(child)
    traverse_subtree(token)
    return sorted(subtree_tokens, key=lambda t: t.i)

def get_tokens_by_dependencies(doc, target_deps, excluded_tokens=[]): 
    if isinstance(target_deps, str):
        target_deps = [target_deps]
    return [token for token in doc if token.dep_ in target_deps and token not in excluded_tokens]

def get_tokens_dep_excluding_subtrees(doc, dep_labels, exclusion_list):
    if isinstance(dep_labels, str):
        dep_labels = [dep_labels]
    excluded_tokens = set()
    for token in exclusion_list:
        excluded_tokens.update(token.subtree)
    return [token for token in doc if token.dep_ in dep_labels and token not in excluded_tokens]

def extract_ac_asca_vc(text):
    doc = nlp(text)
    if has_dependency(doc, 'nsubj') and has_dependency(doc, 'dobj'):
        root = get_sentence_root(doc)[0]
        
        ac_base = get_subtree_dependents_by_dep(root, ["nsubj"])
        vc_base = get_subtree_dependents_by_dep(root, ["dobj"])

        ac_base_subtree = []
        for token in ac_base:
            ac_base_subtree.extend(get_full_subtree(token))
        ac_base_subtree = sorted(list(set(ac_base_subtree)), key=lambda t: t.i)

        ac_prep_base = get_tokens_dep_excluding_subtrees(doc, ["prep"], ac_base + vc_base)
        ac_prep_base_subtree = get_full_subtree(ac_prep_base[0]) if ac_prep_base else []
        ac_advcl_base = get_tokens_dep_excluding_subtrees(doc, ["advcl"], ac_base + vc_base)
        ac_advcl_base_subtree = get_full_subtree(ac_advcl_base[0]) if ac_advcl_base else []
        ac_full = list(set(ac_base_subtree + ac_prep_base_subtree + ac_advcl_base_subtree))
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])

        a_base_subtree = get_full_subtree(root, ["nsubj", "dobj", "prep", "advcl", "dative"])
        a_full = list(set(a_base_subtree))
        a_full = sorted(a_full, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])

        asca_full = list(set(ac_base + a_full))
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])

        vc_base_subtree = []
        for token in vc_base:
            vc_base_subtree.extend(get_full_subtree(token))
        vc_dative_base = get_tokens_dep_excluding_subtrees(doc, ["dative"], vc_base)
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = list(set(vc_base_subtree + vc_dative_base_subtree))
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])

        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)

        return {'type': 'tvc', 'output': (ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim)}

    elif has_dependency(doc, 'nsubjpass') and has_dependency(doc, 'pobj'):
        root = get_sentence_root(doc)[0]

        ac_base = get_subtree_dependents_by_dep(root, ["pobj"])
        vc_base = get_subtree_dependents_by_dep(root, ["nsubjpass"])

        ac_base_subtree = []
        for token in ac_base:
            ac_base_subtree.extend(get_full_subtree(token))
        ac_prep_base = get_tokens_dep_excluding_subtrees(doc, ["prep"], ac_base + vc_base)
        ac_prep_base_subtree = get_full_subtree(ac_prep_base[0]) if ac_prep_base else []
        ac_advcl_base = get_tokens_dep_excluding_subtrees(doc, ["advcl"], ac_base + vc_base)
        ac_advcl_base_subtree = get_full_subtree(ac_advcl_base[0]) if ac_advcl_base else []
        ac_full = list(set(ac_base_subtree + ac_prep_base_subtree + ac_advcl_base_subtree))
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])

        a_base_subtree = get_full_subtree(root, ["nsubjpass", "pobj", "prep", "advcl", "dative"])
        a_full = list(set(a_base_subtree))
        a_full = sorted(a_full, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])

        asca_full = list(set(ac_base + a_full))
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])

        vc_base_subtree = get_full_subtree(vc_base[0])
        vc_dative_base = get_tokens_dep_excluding_subtrees(doc, ["dative"], vc_base)
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = list(set(vc_base_subtree + vc_dative_base_subtree))
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])

        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)

        return {'type': 'tvc', 'output': (ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim)}

    else:
        return {'type': 'ntvc', 'output': (doc.text, "", "", "", extract_named_entities(doc), "")}
```

Alright, now that it is updated, let's give it a test run.

```python
print(extract_ac_asca_vc("The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history."))
print(extract_ac_asca_vc("The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects."))
```

```
{'type': 'tvc', 'output': ('The best road trip in Boston history', 'has given .', 'trip has given .', 'the Celtics a chance at grabbing a piece of NBA history', ['Boston'], ['Celtics', 'NBA'])}
{'type': 'tvc', 'output': ('The wasp ’s flaps and teeth - like hairs', 'resemble .', 'hairs resemble .', 'the structure of the carnivorous Venus flytrap plant , which snaps shut to digest unsuspecting insects', [], ['Venus'])}
```

Wow! The code actually works now! Good stuff. With that settled, let's put everything together into one, final, solid function to calculate sentiment.

```python
def calculate_entity_directed_sentiment(text):
    sentences = split_into_independent_clauses(text)
    entities = {}
    for sentence in sentences:
        out = extract_ac_asca_vc(sentence)
        if out['type'] == 'tvc':
            ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim = out['output']

            ac_sentiment = get_sentiment(ac_full_text)
            asca_sentiment = get_sentiment(asca_full_text)
            vc_sentiment = get_sentiment(vc_full_text)
            
            for entity in named_entities_actor:
                e = entity.lower().capitalize()
                if e not in entities:
                    entities[e] = {'sentiment': 0, 'count': 0}
                entities[e]['sentiment'] += calculate_compound_sentiment(ac_sentiment, vc_sentiment, asca_sentiment)
                entities[e]['count'] += 1
            for entity in named_entities_victim:
                e = entity.lower().capitalize()
                if e not in entities:
                    entities[e] = {'sentiment': 0, 'count': 0}
                entities[e]['sentiment'] += calculate_compound_sentiment(vc_sentiment, ac_sentiment, asca_sentiment)
                entities[e]['count'] += 1
        elif out['type'] == 'ntvc':
            for entity in out['output'][4]:
                e = entity.lower().capitalize()
                if e not in entities:
                    entities[e] = {'sentiment': 0, 'count': 0}
                entities[e]['sentiment'] += get_sentiment(sentence)
                entities[e]['count'] += 1
        else:
            print("No valid output found.")
    return entities, out
```

Now let's give this a try with a variety of sentences:

```python
texts = [
    "Adam and Alice ordered John to stop eating in a late-night hateful rant.",
    "While ranting hatefully, Adam ordered John to stop eating.",
    "Adam, a horrible person, ordered John to stop eating.",
    "John was ordered to stop eating by Adam in a late-night hateful rant.",
    "While ranting hatefully, John was ordered to stop eating by Adam.",
    "The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history.",
    "The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects.",
]

texts_new = [
    "Dr. Velnor's theory was dismissed as absurd by the entire academic panel.",
    "Zantra Corp’s latest device revolutionized clean energy storage overnight.",
    "Mayor Ellith of Norbridge failed to respond during the town’s worst flood in decades.",
    "The Lysara Institute continues to produce groundbreaking neuroscience research.",
    "Critics slammed Darven Tech's flagship phone for its unreliable battery life.",
    "Professor Kezil’s lectures are dry, but his insights are unmatched in the field.",
    "Juno Aeronautics impressed investors with its sleek new drone prototypes.",
    "Velara’s book on dream logic captivated readers with its haunting prose.",
    "The Norell Foundation’s involvement in the scandal tarnished its spotless reputation.",
    "Cylix Entertainment delivered a visually stunning game plagued by technical flaws."
]

print("--- Previous texts ---")
for text in texts:
    print(text)
    s, o = calculate_entity_directed_sentiment(text)
    print(o)
    print(s)
    print()

print()
print("--- New texts ---")
for text in texts_new:
    print(text)
    s, o = calculate_entity_directed_sentiment(text)
    print(o)
    print(s)
    print()
```

```
--- Previous texts ---
Adam and Alice ordered John to stop eating in a late-night hateful rant.
{'type': 'tvc', 'output': ('Adam and Alice in a late - night hateful rant', 'ordered to stop eating .', 'Adam Alice ordered to stop eating .', 'John', ['Adam', 'Alice'], ['John'])}
{'Adam': {'sentiment': -0.5423, 'count': 1}, 'Alice': {'sentiment': -0.5423, 'count': 1}, 'John': {'sentiment': 0.1017048, 'count': 1}}

While ranting hatefully, Adam ordered John to stop eating.
{'type': 'tvc', 'output': ('While ranting hatefully Adam', ', ordered to stop eating .', ', Adam ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.253475, 'count': 1}, 'John': {'sentiment': 0.0778286, 'count': 1}}

Adam, a horrible person, ordered John to stop eating.
{'type': 'tvc', 'output': ('Adam , a horrible person ,', 'ordered to stop eating .', 'Adam ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.49036250000000003, 'count': 1}, 'John': {'sentiment': 0.0974113, 'count': 1}}

John was ordered to stop eating by Adam in a late-night hateful rant.
{'type': 'tvc', 'output': ('by Adam', 'was ordered to stop eating .', 'was ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.062, 'count': 1}, 'John': {'sentiment': -0.062, 'count': 1}}

While ranting hatefully, John was ordered to stop eating by Adam.
{'type': 'tvc', 'output': ('While ranting hatefully by Adam', ', was ordered to stop eating .', ', was ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.253475, 'count': 1}, 'John': {'sentiment': 0.0778286, 'count': 1}}

The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history.
{'type': 'tvc', 'output': ('The best road trip in Boston history', 'has given .', 'trip has given .', 'the Celtics a chance at grabbing a piece of NBA history', ['Boston'], ['Celtics', 'NBA'])}
{'Boston': {'sentiment': 0.46383749999999996, 'count': 1}, 'Celtics': {'sentiment': 0.24375000000000002, 'count': 1}, 'Nba': {'sentiment': 0.24375000000000002, 'count': 1}}

The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects.
{'type': 'tvc', 'output': ('The wasp ’s flaps and teeth - like hairs', 'resemble .', 'hairs resemble .', 'the structure of the carnivorous Venus flytrap plant , which snaps shut to digest unsuspecting insects', [], ['Venus'])}
{'Venus': {'sentiment': 0.0, 'count': 1}}


--- New texts ---
Dr. Velnor's theory was dismissed as absurd by the entire academic panel.
{'type': 'tvc', 'output': ('as absurd', 'was dismissed by .', 'was dismissed by .', "Dr. Velnor 's theory", [], ['Velnor'])}
{'Velnor': {'sentiment': -0.05, 'count': 1}}

Zantra Corp’s latest device revolutionized clean energy storage overnight.
{'type': 'tvc', 'output': ('Zantra Corp ’s latest device', 'revolutionized overnight .', 'device revolutionized overnight .', 'clean energy storage', ['Zantra Corp’s'], [])}
{'Zantra corp’s': {'sentiment': 0.0, 'count': 1}}

Mayor Ellith of Norbridge failed to respond during the town’s worst flood in decades.
{'type': 'ntvc', 'output': ('Mayor Ellith of Norbridge failed to respond during the town’s worst flood in decades.', '', '', '', ['Ellith', 'Norbridge'], '')}
{'Ellith': {'sentiment': -0.6563, 'count': 1}, 'Norbridge': {'sentiment': -0.6563, 'count': 1}}

The Lysara Institute continues to produce groundbreaking neuroscience research.
{'type': 'tvc', 'output': ('The Lysara Institute', 'continues to produce groundbreaking .', 'Institute continues to produce groundbreaking .', '', ['The Lysara Institute'], [])}
{'The lysara institute': {'sentiment': 0.0, 'count': 1}}

Critics slammed Darven Tech's flagship phone for its unreliable battery life.
{'type': 'tvc', 'output': ('Critics for its unreliable battery life', 'slammed .', 'Critics slammed .', "Darven Tech 's flagship phone", [], ["Darven Tech's"])}
{"Darven tech's": {'sentiment': 0.3057885, 'count': 1}}

Professor Kezil’s lectures are dry, but his insights are unmatched in the field.
{'type': 'ntvc', 'output': ('his insights are unmatched in the field .', '', '', '', [], '')}
{'Kezil': {'sentiment': 0.0, 'count': 1}}

Juno Aeronautics impressed investors with its sleek new drone prototypes.
{'type': 'tvc', 'output': ('Juno Aeronautics with its sleek new drone prototypes', 'impressed .', 'Aeronautics impressed .', 'investors', ['Juno Aeronautics'], [])}
{'Juno aeronautics': {'sentiment': 0.1345875, 'count': 1}}

Velara’s book on dream logic captivated readers with its haunting prose.
{'type': 'tvc', 'output': ('Velara ’s book on dream logic with its haunting prose', 'captivated .', 'book captivated .', 'readers', [], [])}
{}

The Norell Foundation’s involvement in the scandal tarnished its spotless reputation.
{'type': 'tvc', 'output': ('The Norell Foundation ’s involvement in the scandal', 'tarnished .', 'involvement tarnished .', 'its spotless reputation', ['The Norell Foundation’s'], [])}
{'The norell foundation’s': {'sentiment': -0.45015, 'count': 1}}

Cylix Entertainment delivered a visually stunning game plagued by technical flaws.
{'type': 'tvc', 'output': ('Cylix Entertainment', 'delivered .', 'Entertainment delivered .', 'a visually stunning game plagued by technical flaws', ['Cylix Entertainment'], [])}
{'Cylix entertainment': {'sentiment': 0.21905179375, 'count': 1}}

```

Interesting. So it seems that right now, the rule-based analysis for prepositions doesn't consider the difference unique to the word "for" as "for" associates an issue with the victim instead of the actor, as is common for most other preps ("Critics slammed Darven Tech's flagship phone for its unreliable battery life." case). Also, for some reason, the entity "Velara" isn't extracted/considered an entity ("Velara’s book on dream logic captivated readers with its haunting prose." case). Let's try fix this.

```python
def extract_ac_asca_vc(text):
    doc = nlp(text)
    if has_dependency(doc, 'nsubj') and has_dependency(doc, 'dobj'):
        root = get_sentence_root(doc)[0]
        ac_base = get_subtree_dependents_by_dep(root, ["nsubj"])
        vc_base = get_subtree_dependents_by_dep(root, ["dobj"])
        ac_base_subtree = []
        for token in ac_base:
            ac_base_subtree.extend(get_full_subtree(token))
        ac_base_subtree = sorted(list(set(ac_base_subtree)), key=lambda t: t.i)
        ac_prep_base = get_tokens_dep_excluding_subtrees(doc, ["prep"], ac_base + vc_base)
        ac_prep_tokens_actor = []
        vc_prep_tokens_victim = []
        for token in ac_prep_base:
            if token.text.lower() in ["for", "to", "with"]:
                vc_prep_tokens_victim.append(token)
            else:
                ac_prep_tokens_actor.append(token)
        ac_prep_base_subtree = []
        for token in ac_prep_tokens_actor:
            ac_prep_base_subtree.extend(get_full_subtree(token))
        vc_prep_base_subtree = []
        for token in vc_prep_tokens_victim:
            vc_prep_base_subtree.extend(get_full_subtree(token))
        ac_advcl_base = get_tokens_dep_excluding_subtrees(doc, ["advcl"], ac_base + vc_base)
        ac_advcl_base_subtree = get_full_subtree(ac_advcl_base[0]) if ac_advcl_base else []
        ac_full = list(set(ac_base_subtree + ac_prep_base_subtree + ac_advcl_base_subtree))
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])
        a_base_subtree = get_full_subtree(root, ["nsubj", "dobj", "prep", "advcl", "dative"])
        a_full = list(set(a_base_subtree))
        a_full = sorted(a_full, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])
        asca_full = list(set(ac_base + a_full))
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])
        vc_base_subtree = []
        for token in vc_base:
            vc_base_subtree.extend(get_full_subtree(token))
        vc_dative_base = get_tokens_dep_excluding_subtrees(doc, ["dative"], vc_base)
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = list(set(vc_base_subtree + vc_dative_base_subtree + vc_prep_base_subtree))
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])
        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)
        return {'type': 'tvc', 'output': (ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim)}
    elif has_dependency(doc, 'nsubjpass') and has_dependency(doc, 'pobj'):
        root = get_sentence_root(doc)[0]
        ac_base = get_subtree_dependents_by_dep(root, ["pobj"])
        vc_base = get_subtree_dependents_by_dep(root, ["nsubjpass"])
        ac_base_subtree = []
        for token in ac_base:
            ac_base_subtree.extend(get_full_subtree(token))
        ac_base_subtree = sorted(list(set(ac_base_subtree)), key=lambda t: t.i)
        ac_prep_base = get_tokens_dep_excluding_subtrees(doc, ["prep"], ac_base + vc_base)
        ac_prep_tokens_actor = []
        vc_prep_tokens_victim = []
        for token in ac_prep_base:
            if token.text.lower() == ["for", "to", "with"]:
                vc_prep_tokens_victim.append(token)
            else:
                ac_prep_tokens_actor.append(token)
        ac_prep_base_subtree = []
        for token in ac_prep_tokens_actor:
            ac_prep_base_subtree.extend(get_full_subtree(token))
        vc_prep_base_subtree = []
        for token in vc_prep_tokens_victim:
            vc_prep_base_subtree.extend(get_full_subtree(token))
        ac_advcl_base = get_tokens_dep_excluding_subtrees(doc, ["advcl"], ac_base + vc_base)
        ac_advcl_base_subtree = get_full_subtree(ac_advcl_base[0]) if ac_advcl_base else []
        ac_full = list(set(ac_base_subtree + ac_prep_base_subtree + ac_advcl_base_subtree))
        ac_full = sorted(ac_full, key=lambda t: t.i)
        ac_full_text = " ".join([token.text for token in ac_full])
        a_base_subtree = get_full_subtree(root, ["nsubjpass", "pobj", "prep", "advcl", "dative"])
        a_full = list(set(a_base_subtree))
        a_full = sorted(a_full, key=lambda t: t.i)
        a_full_text = " ".join([token.text for token in a_full])
        asca_full = list(set(ac_base + a_full))
        asca_full = sorted(asca_full, key=lambda t: t.i)
        asca_full_text = " ".join([token.text for token in asca_full])
        vc_base_subtree = get_full_subtree(vc_base[0])
        vc_dative_base = get_tokens_dep_excluding_subtrees(doc, ["dative"], vc_base)
        vc_dative_base_subtree = get_full_subtree(vc_dative_base[0]) if vc_dative_base else []
        vc_full = list(set(vc_base_subtree + vc_dative_base_subtree + vc_prep_base_subtree))
        vc_full = sorted(vc_full, key=lambda t: t.i)
        vc_full_text = " ".join([token.text for token in vc_full])
        named_entities_actor = extract_named_entities_token(ac_full)
        named_entities_victim = extract_named_entities_token(vc_full)
        return {'type': 'tvc', 'output': (ac_full_text, a_full_text, asca_full_text, vc_full_text, named_entities_actor, named_entities_victim)}
    else:
        return {'type': 'ntvc', 'output': (doc.text, "", "", "", extract_named_entities(doc), "")}
```

Alright, with that fixed: let's test one more time:

```python
texts = [
    "Adam and Alice ordered John to stop eating in a late-night hateful rant.",
    "While ranting hatefully, Adam ordered John to stop eating.",
    "Adam, a horrible person, ordered John to stop eating.",
    "John was ordered to stop eating by Adam in a late-night hateful rant.",
    "While ranting hatefully, John was ordered to stop eating by Adam.",
    "The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history.",
    "The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects.",
]

texts_new = [
    "Dr. Velnor's theory was dismissed as absurd by the entire academic panel.",
    "Zantra Corp’s latest device revolutionized clean energy storage overnight.",
    "Mayor Ellith of Norbridge failed to respond during the town’s worst flood in decades.",
    "The Lysara Institute continues to produce groundbreaking neuroscience research.",
    "Critics slammed Darven Tech's flagship phone for its unreliable battery life.",
    "Professor Kezil’s lectures are dry, but his insights are unmatched in the field.",
    "Juno Aeronautics impressed investors with its sleek new drone prototypes.",
    "Velara’s book on dream logic captivated readers with its haunting prose.",
    "The Norell Foundation’s involvement in the scandal tarnished its spotless reputation.",
    "Cylix Entertainment delivered a visually stunning game plagued by technical flaws."
]

print("--- Previous texts ---")
for text in texts:
    print(text)
    s, o = calculate_entity_directed_sentiment(text)
    print(o)
    print(s)
    print()

print()
print("--- New texts ---")
for text in texts_new:
    print(text)
    s, o = calculate_entity_directed_sentiment(text)
    print(o)
    print(s)
    print()
```

```
--- Previous texts ---
Adam and Alice ordered John to stop eating in a late-night hateful rant.
{'type': 'tvc', 'output': ('Adam and Alice in a late - night hateful rant', 'ordered to stop eating .', 'Adam Alice ordered to stop eating .', 'John', ['Adam', 'Alice'], ['John'])}
{'Adam': {'sentiment': -0.5423, 'count': 1}, 'Alice': {'sentiment': -0.5423, 'count': 1}, 'John': {'sentiment': 0.1017048, 'count': 1}}

While ranting hatefully, Adam ordered John to stop eating.
{'type': 'tvc', 'output': ('While ranting hatefully Adam', ', ordered to stop eating .', ', Adam ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.253475, 'count': 1}, 'John': {'sentiment': 0.0778286, 'count': 1}}

Adam, a horrible person, ordered John to stop eating.
{'type': 'tvc', 'output': ('Adam , a horrible person ,', 'ordered to stop eating .', 'Adam ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.49036250000000003, 'count': 1}, 'John': {'sentiment': 0.0974113, 'count': 1}}

John was ordered to stop eating by Adam in a late-night hateful rant.
{'type': 'tvc', 'output': ('by Adam in a late - night hateful rant', 'was ordered to stop eating .', 'was ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.5423, 'count': 1}, 'John': {'sentiment': 0.1017048, 'count': 1}}

While ranting hatefully, John was ordered to stop eating by Adam.
{'type': 'tvc', 'output': ('While ranting hatefully by Adam', ', was ordered to stop eating .', ', was ordered to stop eating .', 'John', ['Adam'], ['John'])}
{'Adam': {'sentiment': -0.253475, 'count': 1}, 'John': {'sentiment': 0.0778286, 'count': 1}}

The best road trip in Boston history has given the Celtics a chance at grabbing a piece of NBA history.
{'type': 'tvc', 'output': ('The best road trip in Boston history', 'has given .', 'trip has given .', 'the Celtics a chance at grabbing a piece of NBA history', ['Boston'], ['Celtics', 'NBA'])}
{'Boston': {'sentiment': 0.46383749999999996, 'count': 1}, 'Celtics': {'sentiment': 0.24375000000000002, 'count': 1}, 'Nba': {'sentiment': 0.24375000000000002, 'count': 1}}

The wasp’s flaps and teeth-like hairs resemble the structure of the carnivorous Venus flytrap plant, which snaps shut to digest unsuspecting insects.
{'type': 'tvc', 'output': ('The wasp ’s flaps and teeth - like hairs', 'resemble .', 'hairs resemble .', 'the structure of the carnivorous Venus flytrap plant , which snaps shut to digest unsuspecting insects', [], ['Venus'])}
{'Venus': {'sentiment': 0.0, 'count': 1}}


--- New texts ---
Dr. Velnor's theory was dismissed as absurd by the entire academic panel.
{'type': 'tvc', 'output': ('as absurd', 'was dismissed by .', 'was dismissed by .', "Dr. Velnor 's theory", [], ['Velnor'])}
{'Velnor': {'sentiment': -0.05, 'count': 1}}

Zantra Corp’s latest device revolutionized clean energy storage overnight.
{'type': 'tvc', 'output': ('Zantra Corp ’s latest device', 'revolutionized overnight .', 'device revolutionized overnight .', 'clean energy storage', ['Zantra Corp’s'], [])}
{'Zantra corp’s': {'sentiment': 0.0, 'count': 1}}

Mayor Ellith of Norbridge failed to respond during the town’s worst flood in decades.
{'type': 'ntvc', 'output': ('Mayor Ellith of Norbridge failed to respond during the town’s worst flood in decades.', '', '', '', ['Ellith', 'Norbridge'], '')}
{'Ellith': {'sentiment': -0.6563, 'count': 1}, 'Norbridge': {'sentiment': -0.6563, 'count': 1}}

The Lysara Institute continues to produce groundbreaking neuroscience research.
{'type': 'tvc', 'output': ('The Lysara Institute', 'continues to produce groundbreaking .', 'Institute continues to produce groundbreaking .', '', ['The Lysara Institute'], [])}
{'The lysara institute': {'sentiment': 0.0, 'count': 1}}

Critics slammed Darven Tech's flagship phone for its unreliable battery life.
{'type': 'tvc', 'output': ('Critics', 'slammed .', 'Critics slammed .', "Darven Tech 's flagship phone for its unreliable battery life", [], ["Darven Tech's"])}
{"Darven tech's": {'sentiment': 0.3057885, 'count': 1}}

Professor Kezil’s lectures are dry, but his insights are unmatched in the field.
{'type': 'ntvc', 'output': ('his insights are unmatched in the field .', '', '', '', [], '')}
{'Kezil': {'sentiment': 0.0, 'count': 1}}

Juno Aeronautics impressed investors with its sleek new drone prototypes.
{'type': 'tvc', 'output': ('Juno Aeronautics', 'impressed .', 'Aeronautics impressed .', 'investors with its sleek new drone prototypes', ['Juno Aeronautics'], [])}
{'Juno aeronautics': {'sentiment': 0.1345875, 'count': 1}}

Velara’s book on dream logic captivated readers with its haunting prose.
{'type': 'tvc', 'output': ('Velara ’s book on dream logic', 'captivated .', 'book captivated .', 'readers with its haunting prose', [], [])}
{}

The Norell Foundation’s involvement in the scandal tarnished its spotless reputation.
{'type': 'tvc', 'output': ('The Norell Foundation ’s involvement in the scandal', 'tarnished .', 'involvement tarnished .', 'its spotless reputation', ['The Norell Foundation’s'], [])}
{'The norell foundation’s': {'sentiment': -0.45015, 'count': 1}}

Cylix Entertainment delivered a visually stunning game plagued by technical flaws.
{'type': 'tvc', 'output': ('Cylix Entertainment', 'delivered .', 'Entertainment delivered .', 'a visually stunning game plagued by technical flaws', ['Cylix Entertainment'], [])}
{'Cylix entertainment': {'sentiment': 0.21905179375, 'count': 1}}

```

Well, that is much better, though it seems Velara is just not considered a named enitity and "flagship" is considered positive while "unreliable" is not. Other than that though, I'm really satisfied with how this project turned out! It seems to handle texts very well for it being rule based. While further things need to be tested, for now, I'd say it's good enough. 

Just to list a few of my future goals:
- Build a structure that makes adding new conditions very easy
- Refine and consider how most sentences are structured
    - For instance: Negative statements ("Adam did not fight John")
    - Discourse-level sentiment ambiguity (Short phrases in conversation like: "Adam? He was bad.")
    - No distinction for quoted entities
- Refine the sentiment calculations and tools

All in all though, I'm pretty satisfied with this first start.

Cheers!
