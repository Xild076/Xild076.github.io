Several days ago, I watched a chess video by Levy on AlphaZero, the legendary chess AI from 2017 that beat stockfish, the past and prevailing champion. It was a pretty exciting video, however, it got me thinking—what was the key difference between the two chess bots? In essence, the two are the same thing—mathematical constructs to determine the best chess move to make. However, the two operate in very different ways and with very different principles, and that is what I want to explore.

First of all, I am no chess savant, in fact, the only thing I know about chess (other than the very basics) is en passant, but I do know about AIs and algorithms, thus I will be evaluating two models based as a programmer instead of a chess player.

When considering general differences between the two, the first that comes to mind is computational power. Stockfish is a very accessible chess bot as it runs purely on CPU while AlphaZero is a notoriously computationally intensive AI that requires TPUs to run. That can't be considered accessible by any means. 

However, the general difference is natural—Stockfish uses common search algorithms and very basic neural networks to make 30+ move predictions while AlphaZero is a self-learning AI model with millions if not billions of parameters that looks at deep patterns. 

Given this fact, though, I think that the key, core difference becomes clear. Stockfish is meant to be the perfect machine while AlphaZero is meant to be the perfect human, and I feel that AlphaZero fails to capitalize on this fact. 

What I mean by this is that Stockfish, given the way it's built, seems to be aiming towards predicting as many future possibilities in the game as possible. This is a very mechanical way of approaching things, while AlphaZero, on the other hand, seems to attempt emulating human behavior by zoning in on patterns within play.

Then given that, my question is, why was AlphaZero trained only off of self-play? When you look at most grandmasters, they each have a distinct style of play, driven by their own psychology. If trained off of these grandmaster's games, in theory, AlphaZero could develop an insight into chess player's mindset to best find ways to counter them efficiently. This is something that Stockfish, being purely rule-based, can't do, yet AlphaZero fails to capitalize on this by focusing soley on self-play.

While I understand that Deepmind intended AlphaZero to only do self-play so AlphaZero could create some more unique playstyles, I feel that it is a massive missed opportunity and can be explored. Creating a hybrid training method of both using grandmaster games as reference and then self-playing to develop unique playstyles while still retaining knowledge on the human psyche.

However, I am no expert and I definitely don't have the ability to make such impressive AI. Even though I have my small ideas, AlphaZero is still beyond impressive and pretty ahead of its time. This was just a small blog off of some small thoughts, but yeah!

Cheers!