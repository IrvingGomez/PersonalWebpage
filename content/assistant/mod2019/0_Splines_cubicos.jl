using Plots; pyplot()
using Random

using Pkg
using Distributions

using GLM
using DataFrames

# The regression function
m(x) = 3*x.-3*x.^2+x.^3-0.1*x.^4

Random.seed!(79015)
nn = 30
xx = range(0, stop = 3, length = nn)
yy = m(xx)+rand(Normal(0, 0.15), nn)

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")

# We adjust a first order linear estimator
model1 = lm(hcat(repeat([1], outer = 30), xx), yy)

# applies a function to each value of an array and returns a new array
# containing the resulting values:
roundmap(vect, b) = map(x -> round(x, digits = b), vect)

roundmap(coef(model1), 3)

#0.582
#-0.019
#the distribution function is 3*x.-3*x.^2+x.^3-0.1*x.^4

coef(model1)

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x].*coef(model1)),
    label = "Linear fit",
    line = (:RebeccaPurple, 1, 2))

#A quadratic fit
model2 = lm(hcat(repeat([1], outer = nn), xx, map(x -> x^2, xx)), yy)

roundmap(coef(model2), 3)

#0.599
#-0.055
#0.012
#the distribution function is 3*x.-3*x.^2+x.^3-0.1*x.^4

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x, x^2].*coef(model2)),
    label = "Quadratic fit",
    line = (:RebeccaPurple, 1, 2))

#A cubic fit
model3 = lm(hcat(repeat([1], outer = nn), xx, map(x -> x^2, xx),
    map(x -> x^3, xx)), yy)

roundmap(coef(model3), 3)

#0.014
#2.507
#-2.16
#0.483
#the distribution function is 3*x.-3*x.^2+x.^3-0.1*x.^4

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x, x^2, x^3].*coef(model3)),
    label = "Cubic fit",
    line = (:RebeccaPurple, 1, 2))

model4 = lm(hcat(repeat([1], outer = nn), xx, map(x -> x^2, xx),
    map(x -> x^3, xx), map(x -> x^4, xx)), yy)

roundmap(coef(model4), 3)

#-0.069
#3.16
#-3.178
#1.016
#-0.089
#the distribution function is 3*x.-3*x.^2+x.^3-0.1*x.^4

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x, x^2, x^3, x^4].*coef(model4)),
    label = "4 degree fit",
    line = (:RebeccaPurple, 1, 2))

A = [repeat([1], outer = 10) xx[1:10]]
B = [repeat([1], outer = 10) xx[11:20]]
C = [repeat([1], outer = 10) xx[21:30]]
Z = [repeat([0], outer = 10) repeat([0], outer = 10)]

X = [A Z Z;
    Z B Z;
    Z Z C]

bets = X'X\X'yy

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x].*bets[1:2]),
    0, 1,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x].*bets[3:4]),
    1, 2,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x].*bets[5:6]),
    2, 3,
    label = "",
    line = (:RebeccaPurple, 1, 2))

k1 = 1
k2 = 2
Kt =[1 k1 -1 -k1 0 0;
    0 0 1 k2 -1 -k2]

aux1 = X'X\Kt'
aux2 = (Kt*((X'X)\Kt'))\(Kt*bets)
tilbets = bets-aux1*aux2

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x].*tilbets[1:2]),
    0, 1,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x].*tilbets[3:4]),
    1, 2,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x].*tilbets[5:6]),
    2, 3,
    label = "",
    line = (:RebeccaPurple, 1, 2))

A = hcat(repeat([1], outer = 10), xx[1:10],
        map(x -> x^2, xx[1:10]), map(x -> x^3, xx[1:10]))
B = hcat(repeat([1], outer = 10), xx[11:20],
        map(x -> x^2, xx[11:20]), map(x -> x^3, xx[11:20]))
C = hcat(repeat([1], outer = 10), xx[21:30],
        map(x -> x^2, xx[21:30]), map(x -> x^3, xx[21:30]))
Z = reshape(repeat(repeat([0], outer = 10), outer = 4), (10, 4))

X = [A Z Z;
    Z B Z;
    Z Z C]

bets = X'X\X'yy

Kt =[1 k1 k1^2 k1^3 -1 -k1 -k1^2 -k1^3  0   0     0     0;
     0  0    0    0  1  k2  k2^2  k2^3 -1 -k2 -k2^2 -k2^3]

aux1 = X'X\Kt'
aux2 = (Kt*((X'X)\Kt'))\(Kt*bets)
tilbets = bets-aux1*aux2

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x, x^2, x^3].*tilbets[1:4]),
    0, 1,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x, x^2, x^3].*tilbets[5:8]),
    1, 2,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x, x^2, x^3].*tilbets[9:12]),
    2, 3,
    label = "",
    line = (:RebeccaPurple, 1, 2))

Kt =[Kt;
     0  1  2k1  3k1^2  0  -1  -2k1 -3k1^2  0   0     0      0;
     0  0    0      0  0   1   2k2  3k2^2  0  -1  -2k2 -3k2^2]

aux1 = X'X\Kt'
aux2 = (Kt*((X'X)\Kt'))\(Kt*bets)
tilbets = bets-aux1*aux2

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x, x^2, x^3].*tilbets[1:4]),
    0, 1,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x, x^2, x^3].*tilbets[5:8]),
    1, 2,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x, x^2, x^3].*tilbets[9:12]),
    2, 3,
    label = "",
    line = (:RebeccaPurple, 1, 2))

Kt =[Kt;
    0 0 2 6k1 0 0 -2 -6k1 0 0  0    0;
    0 0 0   0 0 0  2  6k2 0 0 -2 -6k2]

aux1 = X'X\Kt'
aux2 = (Kt*((X'X)\Kt'))\(Kt*bets)
tilbets = bets-aux1*aux2

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(x -> sum([1, x, x^2, x^3].*tilbets[1:4]),
    0, 1,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x, x^2, x^3].*tilbets[5:8]),
    1, 2,
    label = "",
    line = (:RebeccaPurple, 1, 2))
plot!(x -> sum([1, x, x^2, x^3].*tilbets[9:12]),
    2, 3,
    label = "",
    line = (:RebeccaPurple, 1, 2),
    ylims = (-0.5, 1.5))


using Dierckx
eee = Spline1D(xx, yy, [k1, k2], k = 3, bc = "extrapolate")
asasas(x) = evaluate(eee,x)

plot(xx, yy,
    seriestype=:scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(m,
    line = (:tomato, 1, 2),
    label = "Regression function")
plot!(asasas,
    label = "",
    line = (:RebeccaPurple, 1, 2),
    background_color = :Lavender,
    ylims = (-0.5, 1.5)
    )
