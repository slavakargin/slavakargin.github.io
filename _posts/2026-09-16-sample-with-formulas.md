---
layout: post
title: "Sample post with formulas"
math: true
---

A sample post, safe to delete. It carries `math: true` in its header, which is what loads MathJax; posts without formulas skip the script. The semicircle law has density $\frac{1}{2\pi}\sqrt{4-x^2}$ on $[-2,2]$, and it plays the role in free probability that the Gaussian plays in the classical theory.

<!--more-->

Inline formulas go between single dollar signs, displayed ones between double dollar signs on their own lines. Free convolution is linearized by the $R$-transform:

$$
R_{\mu \boxplus \nu}(z) = R_\mu(z) + R_\nu(z),
$$

and for the semicircle law of variance $t$ one has $R(z) = tz$, so semicircle laws form a semigroup under $\boxplus$, just as Gaussians do under ordinary convolution.

One thing to know. Markdown reads the text before MathJax does, and it occasionally takes a pair of `*` or `_` inside single dollars for emphasis: `$a^*b^*$` is the classic victim. If a formula comes out mangled, write it with double dollars inline, like this: $$a^*b^*$$. Markdown leaves everything between double dollars alone, and in the middle of a sentence it still comes out as an inline formula.
