---
layout: post
title:  "Causal inference (1/6): motivation"
date:   2019-11-06 18:30:00 +0000
categories: jekyll update
---


<!--
First define
- task
- thread
- core
-->

<!--
Define an order:
- sequential
- concurrent
    - parallel
    - asynchronous
-->

Cause-effect relationships between events are our main interest in our lives. From more hard hitting questions such as _does smoking cause cancer?_ or _does human activity cause global warming?_ to the more menial _Had I left the house 10 minutes earlier, would I have still missed the bus?_ these are the kind of questions we spend most of our time contemplating.

In science the tool of choice to answer such questions in a principled manner is statistics. However for most of its history, statistics was confined to the identification of covariances and correlation, rather than causality. However it's not hard to picture scenarios where this can be quite dissatisfying. When statistics tells us that there is a correlation between temperature and the number shown by the thermometer, our intuitive brain suggests us that this relationship isn't symmetrical: temperature causes changes in the thermometer, not vice versa.

However our ability to formally describe and extrapolate causality was limited for a very long time.
Enter causal inference, a field born roughly in the 90s, with the intention to make a formal study of causality, which would allow us to (1) speak about causal relationships in a more principled manner (2) make quantifiable assesments and predictions of causal relationships from observable data. Before I delve into my understanding of the topic, a quick mention of the resources that have been helping me in my research. Usurprisingly most of the resources I used are either by Judea Pearl or by his students and collaborators.

- A good first introduction was provided by Judea Pearl's most recent book _The book of why_ (https://www.basicbooks.com/titles/judea-pearl/the-book-of-why/9780465097609/)
- A more academic overview is available in his book _Causality - models, reasoning, and inference_ (https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B)
- For some of the the nitty gritty details I found useful to skim through these papers




======================================

This means that while I might not not be able to state that temperature causes a change in the number shown by the thermometer, I can observe that the two are in a direct relationship. However sadly this is true in the reverse order: we observe

There is no concept of order or precedence in a correlation, however even without a formal definition our intuition says that, whatever the meaning of the word, temperature CAUSES the change in thermometer reading, and not vice versa.

Why is it that
P(Y|X)
does not give us causal information? Introduce confounders through the smoking example

This lack of formal defintion was one of the reasons why causality was not given the proper academic attention for so long by statisticians and mathematicians. This however changed in the 90s, when the field of causal inference was born, and it all started with providing a definition for causation.

To give an intuition of the definition of causality it's useful to understand how random control trials (RCTs) work, as for a long time they were our only tool to extrapolate causal information out of data.

In an RCT there is a group that goes through the treatment, and a control group

