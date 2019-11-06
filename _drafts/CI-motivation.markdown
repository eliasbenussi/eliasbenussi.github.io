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

Does smoking cause cancer? Does human activity cause global warming? Had I left the house 10 minutes earlier, would I have still missed the bus? These are different questions in nature, but they all have in common an inquiry into causes and effects. We always search for causes and effects in our explanation, whether it is in science or in our daily life.

However for most of its history, statistics was confined to the identification of covariances and correlation. This means that while I might not not be able to state that temperature causes a change in the number shown by the thermometer, I can observe that the two are in a direct relationship. However sadly this is true in the reverse order: we observe

There is no concept of order or precedence in a correlation, however even without a formal definition our intuition says that, whatever the meaning of the word, temperature CAUSES the change in thermometer reading, and not vice versa.

Why is it that P(Y|X) does not give us causal information? Introduce confounders through the smoking example

This lack of formal defintion was one of the reasons why causality was not given the proper academic attention for so long by statisticians and mathematicians. This however changed in the 90s, when the field of causal inference was born, and it all started with providing a definition for causation.

To give an intuition of the definition of causality it's useful to understand how random control trials (RCTs) work, as for a long time they were our only tool to extrapolate causal information out of data.

In an RCT there is a group that goes through the treatment, and a control group

