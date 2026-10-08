---
layout: post
title: "Why the determinant formula is true"
math: true
description: "Why the Mai–Speicher formula for the Fuglede–Kadison determinant of a matrix semicircle survives adding a constant matrix: how I think about it."
---

In [his post](https://rolandspeicher.com/2026/09/09/a-story-of-the-determinant-of-operator-valued-semicircular-elements/) Roland Speicher asked whether the [Mai–Speicher formula](https://arxiv.org/abs/2406.15922) for the Fuglede–Kadison determinant of a matrix semicircle survives when a constant matrix is added. With $$S_a=a\otimes1+\sum_jA_j\otimes s_j$$ and $$\eta(X)=\sum_jA_jXA_j$$, the proposed formula is

$$
\begin{aligned}
\log\Delta(S_a-z)&=-\frac12+\inf_{b}\Bigl\{\operatorname{tr}_m\log b+\frac12\langle a-z,(\mathcal C_b+\eta)^{-1}(a-z)\rangle\Bigr\},\\
\mathcal C_b(X)&=bXb,
\end{aligned}
$$

where the infimum is over positive matrices $$b$$ with $$\mathcal C_b-\eta\succeq0$$. It is true, for every real $$z$$. The proof is in the manuscript. Here I only want to say how I think about it, because the formula looked strange to me at first and now it looks a bit less strange.

<!--more-->

## There had to be some formula

The logarithmic potential is an integral of the Stieltjes transform. The Stieltjes transform comes from the Dyson equation $$G^{-1}+\eta(G)=z-a$$. And the Dyson equation is the Euler–Lagrange equation of a functional, the Dyson action

$$
\mathcal A_z(M)=-\operatorname{tr}_m\log M-\frac12\operatorname{tr}_m\bigl(M\eta(M)\bigr)+\operatorname{tr}_m\bigl((z-a)M\bigr)-1 .
$$

If you differentiate the action at its critical point with respect to $$z$$, only the explicit $$z$$ contributes, and you get $$\operatorname{tr}_mG$$. So the action at the Dyson solution is also an integral of the Stieltjes transform, and it is not a surprise that $$\log\Delta(S_a-z)=\operatorname{Re}\mathcal A_z(G(z))$$. The shift $$a$$ plays no role here. It rides along with $$z$$.

So the determinant is a critical value. The trouble is that it is the wrong kind of critical value. The action is holomorphic in $$M$$, so the Dyson solution is a saddle of its real part, with as many directions going down as going up. A formula with an “$$\inf$$” in it cannot come from the action directly.

## The idea: free the scale

In the centered case the answer is $$\det b$$ for the matrix $$b$$ that scales $$\eta$$ to a doubly stochastic map. This suggested that $$G$$ should come with a positive “scale” also in general. It does: there is a unique $$b\succ0$$ with

$$
G=b^{-1/2}\,U\,b^{-1/2},\qquad U\ \text{unitary}.
$$

For scalars this is just $$b=1/\lvert G\rvert$$ and $$U$$ is the phase.

The step that was unexpected for me is to forget that $$b$$ is determined by $$G$$ and treat it as a new independent variable. Write $$G=-u-i\gamma$$ and consider

$$
\begin{aligned}
\mathcal K(b,u,\gamma)=\operatorname{tr}_m\log b&+\langle a-z,u\rangle-\frac12\langle u,(\mathcal C_b+\eta)u\rangle\\
&-\frac12\langle\gamma,(\mathcal C_b-\eta)\gamma\rangle.
\end{aligned}
$$

When $$b$$ is the true scale of $$-u-i\gamma$$ this is the real part of the Dyson action (plus $$\frac12$$), by a direct computation. And the Dyson solution, together with its scale, is still a critical point of $$\mathcal K$$ in the three variables. So nothing is lost. What is gained is that the saddle has been taken apart: $$\mathcal K$$ is concave in $$u$$ and in $$\gamma$$, so all the descending directions sit in these two variables, and one can remove them by maximizing.

## Two things that come for free

The first is the constraint. I had thought of $$\mathcal C_b-\eta\succeq0$$ as a condition somebody cleverly imposed. But look at the last term of $$\mathcal K$$. Its supremum over $$\gamma\succeq0$$ is $$0$$ if $$\mathcal C_b-\eta\succeq0$$ and $$+\infty$$ otherwise. The feasible set is simply the set of $$b$$ for which the problem makes sense. It is the trace that the imaginary part of $$G$$ leaves behind.

Maximizing over $$u$$ then gives exactly the function in Roland's formula.

The second is convexity, and this is the heart of the matter. The function of $$b$$ that remains is not convex in the usual sense. It is convex along the geodesics $$b^{1/2}e^{tX}b^{1/2}$$ of the positive cone, and it is so *precisely on the feasible set*. The scalar semicircle shows what this means. There the function is

$$
F_x(b)=\log b+\frac{x^2}{2(b^2+1)},\qquad b\ge1 .
$$

For positive numbers the geodesics are simply $$t\mapsto be^{t}$$, so geodesic convexity is ordinary convexity in the variable $$s=\log b$$. In this variable

$$
F_x=s+\frac{x^2}{4}\,\bigl(1-\tanh s\bigr).
$$

The first term is linear. The second is a reflected $$\tanh$$: it is convex for $$s>0$$ and concave for $$s<0$$, and its inflection point is at $$s=0$$, that is, at $$b=1$$, exactly the boundary of the feasible set. So the constraint that came out of the imaginary part is the same as the condition that makes the problem convex. I do not think this is an accident, but I cannot say in one sentence why it must be so.

Once we have convexity, a critical point is a global minimum, and the critical point is the scale of the Dyson solution. This is the whole proof in the upper half-plane. To get to the real axis one adds $$\varepsilon\operatorname{tr}_m\gamma$$ to $$\mathcal K$$, which adds a positive term of order $$\varepsilon^2$$ to the function of $$b$$, and lets $$\varepsilon\to0$$. Everything is monotone, and one never needs to know what the minimizers do.

## What the picture looks like

In the scalar example the equation $$F_x'(b)=0$$ is $$b+1/b=\lvert x\rvert$$, which is the Dyson equation for $$b=1/\lvert G\rvert$$. For $$\lvert x\rvert>2$$ it has a solution with $$b>1$$. For $$\lvert x\rvert<2$$ it has none, the minimum sits at the wall $$b=1$$, and its value is $$x^2/4$$, as it should be.

The same holds for matrices, at least at points where the density is nondegenerate. Outside the spectrum the minimizer is in the interior of the feasible set. Inside the spectrum it is on the boundary, and the kernel of $$\mathcal C_b-\eta$$ at the minimizer contains $$\gamma=-\operatorname{Im}G$$. In other words, the spectrum is where the constraint is active, and the density of states is its Lagrange multiplier. This is the form in which I remember the result.

## What I do not understand

Is the infimum attained at spectral edges, and at points where the matrix density is nonzero but singular? I do not know. The scales $$b_\varepsilon$$ might run away, and at points where the density blows up they do. It would be nice to read the type of the singularity from how fast they run.

The question I find most interesting is about the Brown measure. By hermitization the formula applies to any $$S=a_0\otimes1+\sum a_i\otimes s_i$$ with arbitrary matrices $$a_i$$ and any complex $$z$$. For each fixed $$b$$ the function under the infimum is a quadratic polynomial in $$\operatorname{Re}z$$ and $$\operatorname{Im}z$$. So the logarithmic potential of the Brown measure is an infimum of quadratic polynomials over a fixed convex set.

Now we can ask whether the minimizer $$b_z$$ sits in the interior or on the boundary of the feasible set. By the picture above this should detect the spectrum of $$S$$: if $$S-z$$ is invertible, the minimizer is in the interior. Is this enough to detect the support of the Brown measure? That is, *is the Brown measure of $$S$$ supported exactly where the constraint is active?* For general operators the spectrum can be strictly larger than the support of the Brown measure. [Haagerup and Larsen](https://www.sciencedirect.com/science/article/pii/S0022123600936103) found this for $$R$$-diagonal elements, where it happens when the element has an inverse which is in $$L^2$$ but is not bounded. [Miyagawa](https://arxiv.org/abs/2603.19528) has recently shown that a rational function in free semicirculars which is in $$L^2$$ is bounded, so this mechanism is not available here, and he asks whether there is any gap at all in that setting. [Hall and Ho](https://arxiv.org/abs/2510.03382) proved that there is none for a self-adjoint element plus a free elliptic one. For matrix semicirculars I do not know the answer. If there is no gap, the variational problem should show it: one would have to prove that the potential cannot be harmonic at a point where the constraint binds.

* * *

*I should add that I worked on this in long conversations with language models. It felt like working with a co-author, and I cannot separate who contributed what. The responsibility for the correctness is mine.*
