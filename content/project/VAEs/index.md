---
title: Variational Autoencoders with Missing Data
summary: The summary
tags:
- Deep Learning
date: "2016-04-27T00:00:00Z"

# Optional external URL for project (replaces project detail page).
external_link: ""

image:
  focal_point: Smart
---

This is a project in collaboration with Jill-Jênn Vie from Inria-Lille, France.

# Autoencoders

## Dimensionality Reduction

In some applications like data visulisation, data storage or when the dimmensionality of our data is to large, we'd like to reduce its dimmensionality of the data,
keeping as much information as possible. So we'd like to construct an encoder that takes the original data and transform it into a latent variable of lower
dimmensionality. Some times we'd like to recover the original points (with the minimal error) from their encoded versions.
So we need an encoder that takes points from the latent space and
transform them into points in the original space.

## Original/Greedy Autoencoder

Let's denote by $x$ an observation in the original space and $z$ its encoded value. If we denote by $g$ the encoded function, then $z = g(x)$.
We can decode $z$ through a decoded function $f$,
and try to recover the original point from this decoded value. That is, $f(z)$ is not necessarily equal to $\hat x$, this is becasue $f(z)$ does not necessarily belogs to
the original space, then we need one more step to transform $f(z)$ into value that belongs to the original space.
This final transformation might be done in two different ways, the first
and original one is to use a deterministic function that takes decoded value $f(z)$ and transform them into the original space, the second one is to take $f(z)$ as the
parameter of a random variable, and make $\hat x$ an observation of this final distribution.

When we model $f$ and $g$ as neural networks (usually deep neural networks), we get the so-called autoencoder. Where $f$ and $g$ are learned with some trainig data set
and according to some loss functions $L(x, f(z))$.

{{< figure src="AE_draw.jpg" title="Original Autoencoder">}}

## Example

For example, if $x$ is an observation of a Bernoulli distribution we could choose $L(x,f(z))$ as the loglikelihood, where $f(z)$ is the parameter of such distribution,
that is

$$L(x,f(z)) = f(z)\log(x)+(1-f(z))\log(1-x)$$

where $z = g(z)$ and $f$ and $g$ are learned with (stochastic) gradient ascent.

Note that while $x\in\{0,1\}$, $f(z)\in (0,1)$. Thus, we can take $\hat x = 1\\{f(z)>=0.5\\}$ (which would be a deterministic approach) or
$\hat x\sim \text{Bernoulli}(f(z))$ (which with a random approach), the standard is to take a deterministic approach to go from $f(z)$ to $\hat x$

A good introduction to VAEs can be found <a href="https://towardsdatascience.com/understanding-variational-autoencoders-vaes-f70510919f73" target="_blank"> here </a>

{{< figure src="original_denoise_vae_latent.gif" title="Evolution of the latent space" width="300">}}




