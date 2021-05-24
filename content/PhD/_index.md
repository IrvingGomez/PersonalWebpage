---
title: PhD
layout: docs  # Do not modify.

# Optional header image (relative to `static/img/` folder).
header:
  caption: ""
  image: ""
---

My PhD dissertation can be divided in two parts, the first part deals with the estimation of the regression function with random forests when the observations have missing entries. The commonly used CART-criterion only can be applied to completed observations, usually to solve this problem an imputation technique is used before the evaluation of the CART-criterion. The proposal in my dissertation solves this problem from a different perspective, it changes the untractable parts of the CART-criterion for mathematical objects that allow its computation. That is, we do not impute the missing values previously to the construction of the random forest, but we used the observations as they are in the construction of the random forest. I prove in my dissertation that this approach to estimate the regression function generates consistent estimators. It is worthy to say that this is the first result showing the consistency of an estimator with missing entries.

The second part of my dissertation is focused on the reconstruction of the missing values through autoencoders. In a nutshell an autoencoder is composed of two parts. The first part, called the encoder projects the observations with missing values in a space of small dimension. The second part, called the decoder, recovers the original (with no missing values) data. This fragment of the dissertation forms part of the project related to variational autoencoders with missing data, and was developed during a brief stay at <a href="https://www.inria.fr/centre/lille" target="_blank"> Inria-Lille</a> in collaboration with <a href="https://jilljenn.github.io/" target="_blank"> Jill-Jênn Vie </a> (to know more click <a href="https://irvinggomez.netlify.app/project/vaes/" target="_blank"> here </a>).

The codes to construct random forests to estimate the regression function with missing data are found in <a href="https://github.com/IrvingGomez/Random_forests_with_missing_values">https://github.com/IrvingGomez/Random_forests_with_missing_values</a>. The codes for the autoencoders with missing data are not publicly availabe (yet). The manuscript of my dissertation can be found here <a href="https://irvinggomez.com/phd/Random_Forests_and_Autoencoders_with_Missing_Data.pdf">https://irvinggomez.com/phd/Random_Forests_and_Autoencoders_with_Missing_Data.pdf</a>.
