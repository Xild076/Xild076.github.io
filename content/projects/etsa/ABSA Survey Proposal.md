## 1. Investigation Targets
This survey aims to use collect data on aspect based sentiment in order to develop mathematical formulas to map how sentiment is associated to entities due to entity interactions.
### a. Compound Sentiments
Compound sentiments refer to the final intra-sentence sentiments directed at entities that undergo a shift due to entity relations. As a ground truth, we will assume the following:
1. Directly associated words (ie: adjectives, adverbs, etc) will serve as the foundational sentiment of an entity from which sentiment shifts due to entity interactions will occur.
2. VADER sentiment analysis will be used as the numerical sentiment calculator.
#### i. Action
##### Explanation:
Action type entity relationships are relationships that occur because an "actor" entity performed an action upon a "target" entity.
##### Logic:
This was chosen as one of the three core entity relationships because how actions are viewed are heavily influenced by context, especially upon who an action is taken. For instance, beating someone up is considered negative, but if the one being beat up is a very bad person, the entire perception shifts.
##### Example:
The **brave firefighter (actor)** *heroically saved (action)* the **innocent, little kitten (target)**.

**Actor:** firefighter (associated tokens: "brave") (sentiment: +0.5267 - VADER)
**Action:** saved (associated tokens: "heroically") (sentiment: +0.4215 - VADER)
**Target:** kitten (associated tokens: "innocent, little") (sentiment: +0.34 - VADER)

<<< Pass through an arbitrary formula (based off of my own gut feelings as of right now for the sake of an example) >>>

**Actor:** firefighter (sentiment: +0.7)
**Target:** kitten (sentiment: +0.3)

**Rationale:** The sentiment for firefighter increased because it saved a positive-associated entity (the kitten) while the kitten stayed generally the same since it was a more passive entity.
##### Sub-points of interest:
- Possible negativity biases.
#### ii. Association
##### Explanation:
Association type entity relationships are relationships that occur because two entities are connected or related to one another due to proximity or explicit denotation.
##### Logic:
This was chosen as a core relationship because proximity plays a great role in how people perceive entities. It runs off of the same principle as hasty generalization fallacies—because things are connected, even if something isn't directly implicated, there remains a sentiment shift.
##### Example:
The **good person (entity)** and the **bad individual (entity)** ate food together.

**Entity 1:** person (associated tokens: "good") (sentiment: +0.4404 - VADER)
**Entity 2:** individual (associated tokens: "bad") (sentiment: -0.5423 - VADER)

<<< Associated by tokens: "and" and "together" >>>
<<< Pass through an arbitrary formula (based off of my own gut feelings) >>>

**Entity 1:** person (sentiment: +0.3 - VADER)
**Entity 2:** individual (sentiment: -0.3 - VADER)

**Rationale:** The sentiment for the person decreased because they were associated with a negative-associated entity, while the reverse was true for the individual.
##### Sub-points of interest:
- Possible negativity biases
- Inter-sentence cases of association
#### iii. Belonging
##### Explanation:
Belonging type entity relationships are relationships that occur because an entity (child) is the derivative of another entity (parent).
##### Logic:
This was chosen as a core relationship because while somewhat similar to association relationships, the fact that a child entity is a derivative of a parent entity means that the child entity has a massive effect on the perception of a parent entity, especially since a parent entity is the wholistic make up of its derivative parts.
##### Example:
The **good phone (parent)**'s **battery (child)** was horrible.

**Entity 1:** phone (associated tokens: "good") (sentiment: +0.4404 - VADER)
**Entity 2:** battery (associated tokens: "horrible") (sentiment: -0.5423 - VADER)

<<< Belonging by tokens: "'s" >>>
<<< Pass through an arbitrary formula (based off of my own gut feelings) >>>

**Entity 1:** phone (sentiment: +0.1 - VADER)
**Entity 2:** battery (sentiment: -0.5 - VADER)

**Rationale:** The phone's sentiment decreased because its derivative part was negative-associated, reflecting badly on phone in general. Meanwhile, the battery faced nearly no changes because its just one of the parts that made up the phone, meaning the phone sentiment to it is almost irrelevant. 
##### Sub-points of interest:
- Possible negativity biases
- Inter-sentence cases of belonging
### b. Aggregate Sentiments
##### Explanation:
Aggregate sentiment looks at how shifts in sentiment over time ultimately define the final impression left after reading a full text.
##### Logic:
People often have primacy and recency biases in terms of impressions, which lends itself to different weighing of sentiment. For instance, the start and end of a sentence may be valued higher in terms of sentiment than the middle parts. Thus, if an entity is referenced multiple times, the final aggregate sentiment will be more than the sum of its parts, it will be a sum of its weighted parts.

##### Example:
The phone is good. The phone has a bad battery life. The phone also has a bad screen. However, the phone has good functionality and effectiveness.

**By Sentence:**
- "The phone is good." (sentiment: +0.4404 - VADER)
- "The phone has a bad battery life." (sentiment: -0.5423 - VADER)
- "The phone also has a bad screen." (sentiment: -0.5423 - VADER)
- "However, the phone has good functionality and effectiveness." (sentiment: +0.4404 - VADER)

<<< Pass through an arbitrary formula (based off of my own gut feelings) >>>

**Final "phone" sentiment:** +0.3

**Rationale:** Due to primacy and recency bias, more weight is given to the start and end, resulting in a positive compound sentiment.
## 2. Survey design
The survey will contain 30 questions. 4 questions will have the purpose of gathering data on compound action, 4 will gather data on association, 4 will gather data on possession, and 15 will gather data on aggregation. One question will be an attention check.

To prevent biases, the survey will take the following measures:
- Gender neutral and repetitive names for the association and action relationship questions.
- Commonly-used objects with no branding for the possession relationship and aggregation questions.

In addition, to add variety, within each question, for both negative and positive terms, a phrase will be chosen from a list of phrases composed of four different possible valences: very (sentiment score on VADER from 1 to 0.7), medium (0.7 to 0.5), somewhat (0.5 to 0.3), and slightly (0.3 to 0.1).

Users will score the sentiment on a 9-point Likert scale where each possible choice will align with the four different valence choices as put above in addition to a neutral choice of 0.1 to -0.1.

For the sake of reproducibility, the random seed will be recorded per user. 

In addition, the structured examples with positive and negative are only there to show one of the two possible combinations. To cover more ground and combinations, the sentiments may be reversed, for instance, if a text structure says: {+} {+} {-}, on random, it may be flipped to {-} {-} {+} instead.

Independent/non-linking questions will be randomized in its given order. The attention check will be added in the middle.
### a. Compound Sentiments
#### i. Action
*4 questions*
<sup>Note: x and y can refer to any positive (+)/negative (-) sentiments. Given this, the given questions should cover all possible permutations.</sup>
##### Question 1:
**Purpose:** To check x-x-y relationships.
**Text or Structure:**
"{+ actor} {+ action} {- target}"
##### Question 2:
**Purpose:** To check y-x-x relationships
**Text or Structure:**
"{+ actor} {- action} {- target}"
##### Question 3:
**Purpose:** To check x-x-x relationships
**Text or Structure:**
"{- actor} {- action} {- target}"
##### Question 4:
**Purpose:** To check x-y-x relationships.
**Text or Structure:**
"{+ actor} { action} {+ target}"
#### ii. Association
*4 questions*
##### Question 1:
**Purpose:** To check association opposite polarity.
**Text or Structure:**
"{+ entity} and {- entity} often {neutral action} together."
##### Question 2:
**Purpose:** To check inter-sentence association.
**Text or Structure:**
"{- entity} often hung out with {- entity}."
##### Question 3:
**Purpose:** To check inter-sentence association and negativity bias.
**Text or Structure:**
"{+ entity} did {+ action} {neutral action} together every weekend."
##### Question 4:
**Purpose:** To check association opposite polarity.
**Text or Structure:**
"{- entity} partnered with {+ entity} all the time."
#### iii. Belonging
*4 questions*
##### Question 1:
**Purpose:** To check association opposite polarity
**Text or Structure:**
"The {- parent}'s {+ child} was {+ description}, though the {- parent} itself was {- description}."
##### Question 2:
**Purpose:** To check association same polarity
**Text or Structure:**
"The {- parent} is {- description}, and its {- child} is {- description}."
##### Question 3:
**Purpose:** To check association opposite polarity
**Text or Structure:**
"The {- child} was {- description}, but the {+ parent} was {+ description}."
##### Question 4:
**Purpose:** To check association same polarity
**Text or Structure:**
"The {+ parent} is {+ description}, and its {+ child} is {+ description}."
### b. Aggregate Sentiments
*2 packets, 8 questions total*
##### Packet 1:
*3 questions*
**Purpose:** To check shorter aggregate sentiment shifts.
**Text or Structure:**
1. "xxx was good."
2. "xxx was good."
3. "xxx was bad."
##### Packet 2:
*5 questions*
**Purpose:** To check medium-length aggregate sentiment shifts and shift back cases.
**Text or Structure:**
1. "xxx was bad."
2. "xxx was good."
3. "xxx was good."
4. "xxx was bad."
5. "xxx was bad."
##### Packet 3:
*9 questions*
**Purpose:** To check long-length aggregate sentiment shifts.
### Template
#### Independent Questions
<sub>These will include the Action, Association, and Possession questions.</sub>

**Please read the following text:**

>The brave firefighter heroically saved the innocent, little kitten.

**After reading sentence, how do you feel about (the) firefighter?**

- Very Negative (-4)
- Negative (-3)
- Somewhat Negative (-2)
- Slightly Negative (-1)
- Neutral (0)
- Slightly Positive (1)
- Somewhat Positive (2)
- Positive (3)
- Very Positive (4)

**After reading sentence, how do you feel about (the) kitten?**

- Very Negative (-4)
- Negative (-3)
- Somewhat Negative (-2)
- Slightly Negative (-1)
- Neutral (0)
- Slightly Positive (1)
- Somewhat Positive (2)
- Positive (3)
- Very Positive (4)
#### Packets
<sub>These will include Aggregate questions. Note that the questions will be shown one by one.</sub>

**The following questions are continuations of each other.**

**Please read the following text:**

>The phone is good.

**After reading sentence, how do you feel about (the) phone?**

- Very Negative (-4)
- Negative (-3)
- Somewhat Negative (-2)
- Slightly Negative (-1)
- Neutral (0)
- Slightly Positive (1)
- Somewhat Positive (2)
- Positive (3)
- Very Positive (4)

--- Page Break ---

**Please read the following text:**

>The phone is good.  The phone has a bad battery life.

**After reading sentence, how do you feel about (the) phone?**

- Very Negative (-4)
- Negative (-3)
- Somewhat Negative (-2)
- Slightly Negative (-1)
- Neutral (0)
- Slightly Positive (1)
- Somewhat Positive (2)
- Positive (3)
- Very Positive (4)

--- Page Break ---

**Please read the following text:**

>The phone is good.  The phone has a bad battery life. However, the phone has good functionality and effectiveness.

**After reading sentence, how do you feel about (the) phone?**

- Very Negative (-4)
- Negative (-3)
- Somewhat Negative (-2)
- Slightly Negative (-1)
- Neutral (0)
- Slightly Positive (1)
- Somewhat Positive (2)
- Positive (3)
- Very Positive (4)

--- Page Break ---
<< 9 question packet here >>
## 3. Mathematical Formulae
<sub>Note that these formulae will be based off of preconceived assumptions about how sentiment works and may be up to change depending on the survey results. Initial sentiments will be based off of directly associated tokens and VADER sentiment calculations. The survey data will be normalized to fit the VADER scores. Also please note that the λ is independent for each equation, even those of the same category.</sub>
### a. Compound Sentiments
#### i. Building blocks
##### 1. Weighted averages
$$s_{new}=λ*s_{old}+(1-λ)*s_{update}$$
Measures importance of directly associated sentiment and entity-interaction derived sentiment
##### 2. Signed weights and biases
$$w(δ)=\begin{cases} 
      w^+ & s_{driver}> 0 \\
      w^- & s_{driver}\leq0
   \end{cases}
$$
$$b(δ)=\begin{cases} 
      b^+ & s_{driver}> 0 \\
      b^- & s_{driver}\leq0
   \end{cases}
$$
Considers greater weight put on negative information due to negativity bias with signed weights and uneven mitigation of bias with signed biases. $δ$ is the sign of the driver's sentiment
##### 3. Normalization
$$s_{final}=\tanh(s_{new})$$
Compresses the sum between $(-1,1)$ to prevent sentiment from exceeding VADER structure.
### a. Compound Sentiments
#### i. Action
##### Actor:
**Formula:**
$$s_{final-actor}=\tanh[λ_{actor}*s_{init-actor} + (1-λ_{actor}) * w_{actor}(δ) * s_{action} * s_{init-target} + b_{actor}(δ)]$$
**Inputs:**
- $s_{init-actor}$: the actor's sentiment before the action
- $s_{action}$: the sentiment of the action
- $s_{init-target}$: the actor's target's before the action
**Weights:**
- $λ_{actor}$: memory weight factor
- $w_{actor}$: actor signed weight
- $b_{actor}$: actor signed biases
**Rationale:** The actor's sentiment is a combination of past sentiment and actions taken. The impact is based off of the sentiment of the target—if its a bad action on a bad person, the ultimate outcome is positive, it multiplies actions to determine the "true" evaluators. The  bias included reflects possible negativity biases.
##### Target:
**Formula:**
$$s_{final-target}=\tanh[λ_{target}*s_{init-target} + (1-λ_{target}) * w_{target}(δ) * s_{action}+b_{target}(δ)]$$
**Inputs:**
- $s_{init-target}$: the actor's sentiment before the action
- $s_{action}$: the sentiment of the action
**Weights:**
- $λ_{target}$: memory weight factor
- $w_{action}$: action signed weight
- $b_{target}$: actor signed biases
**Rationale:** Since the role of the actor plays a smaller role on the receiving end, the sentiment of the target is removed, but it may be added back depending on survey results.
#### ii. Association
**Formula:**
$$s_{final-entity}=\tanh[λ_{entity}*s_{init-entity} + (1-λ_{entity}) * w_{entity}(δ) * s_{other} + b_{entity}(δ)]$$
**Inputs:**
- $s_{init-entity}$: the actor's sentiment before the action
- $s_{other}$: the sentiment of the other entity
**Weights:**
- $λ_{entity}$: memory weight factor
- $w_{entity}$: entity signed weight
- $b_{entity}$: entity signed biases
**Rationale:** Much simpler, just an average with higher weight. May become more complex depending on the situation.
#### iii. Belonging
##### Parent
**Formula:**
$$s_{final-parent}=\tanh[λ_{parent}*s_{init-parent} + (1-λ_{parent}) * (s_{child})]$$
**Inputs:**
- $s_{init-parent}$: the parent's sentiment before the action
- $s_{child}$: the sentiment of the child
**Weights:**
- $λ_{parent}$: memory weight factor
**Rationale:** Much simpler, just an average with higher weight. May become more complex depending on the situation.
##### Child
**Formula:**
$$s_{final-child}=\tanh[λ_{child}*s_{init-child} + (1-λ_{child}) * (s_{parent})]$$
**Inputs:**
- $s_{init-child}$: the child's sentiment before the action
- $s_{parent}$: the sentiment of the other parent
**Weights:**
- $λ_{child}$: memory weight factor
**Rationale:** Much simpler, just an average with higher weight. May become more complex depending on the situation. Despite the child being influenced much less than the parent, it is still possible there are some minor influences, thus the formula.
### b. Aggregate Sentiments
**Formula:**
$$s_{final}=Σ_{i=1}^{N}[w_i*s_i]$$
where
$$w_i=\frac{i^{α-1}(n-i+1)^{β-1}}{\sum_{k=1}^nk^{α-1}(n-k+1)^{β-1}}$$
where
$α=M_α*N+b_α$
$β=M_β*N+b_β$
(modified probability mass function, a type of beta curve that provides weighed probabilities in parabolic form)
**Inputs:**
- $s$: list of all sentiments
**Weights:**
- $α$: Primacy weight, and the smaller $α$ gets, the more weight is put on primacy.
- $β$: Recency weight, and the smaller $β$ gets, the more weight is put on recency.

**Rationale:** Primacy and recency bias means that aggregate sentiments would most likely be based off of weights looking like a pseudo-parabola. Furthermore, primacy and recency may change depending on the length of the text, hence the linear function for alpha and beta.
**How to apply survey:** Unlike the other ones, the survey will be harder to apply here because we can only see the $Δs$, not the weight applied to each. Thus, just throwing everything at a graph will not work. The only thing we know for sure at the end of the day is the final ground truth, that the entire rating will be $x$. I suppose how we would be going forward is to run the test through each step of the human investigation with the simple algorithm and an optimization program to check for the closest solution, round it, and call it a day for the heuristic approach.