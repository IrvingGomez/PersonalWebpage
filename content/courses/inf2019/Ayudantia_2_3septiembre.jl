### Irving Gomez Mendez
### September 3rd 2019

#Considérense una muestra de n = 47 observaciones independientes e idénticamente distribuidas que corresponden a
#los tiempos entre llegadas de grupos de visitantes al Museo de las Momias de Guanajuato el Sábado Santo 15 de abril
#de 2017 de las 12:00 a las 12:30pm. Los 47 tiempos x1, ..., x47 fueron medidos como parte de su tesis por Ana Paulina
#Pérez Romero, exalumna graduada de la Maestría de Probabilidad y Estadística del CIMAT. Los datos registrados
#en segundos fueron:

mm = [54, 24, 54, 6, 14, 87, 42, 30, 21, 4, 43, 34, 25, 26, 79, 35, 15, 25, 33, 20, 12, 34, 24, 29, 28, 32, 83, 40, 32,
        94, 27, 47, 52, 68, 14, 44, 34, 32, 32, 6, 18, 80, 90, 40, 100, 25, 30]
nn = length(mm)

using Plots; pyplot()
using Distributions
# StatsBase has the ecdf
using StatsBase
# StatsPlots allows to plot a desnity directly from the distribution name
using StatsPlots
using LaTeXStrings


?Distributions

?Exponential

θ_hat = mean(mm)
Dist = Exponential(θ_hat)
Empirical = ecdf(mm)

plot(sort(mm), map(Empirical, sort(mm)),
    label = "Empirical CDF",
    ylabel = L"F_n(x,θ)",
    background_color = :Lavender,
    linetype = :steppost,
    lw = 2,
    color = :RebeccaPurple)

plot!(x -> cdf(Dist, x),
    label = "Exponential(38.68)",
    lw = 2)

histogram(mm,
    normalized = true,
    background_color = :Lavender,
    fillalpha = 0.33,
    color = :RebeccaPurple)

plot!(Exponential(38.68),
    label = "Exponential(38.68)",
    xlims = [0,110],
    lw = 2)

α = range(1/(nn+1), step = 1/(nn+1), length = nn)

scatter(quantile.(Dist, α), sort(mm),
    label = "QQ_Exponential(38.68)",
    ylabel = L"x_{(i)}",
    xlabel = L"Q_{i/(n+1)}",
    background_color = :Lavender,
    lw = 2,
    color = :RebeccaPurple)

plot!(x -> x,
    label = "Identity",
    lw = 2)

# Bootstrap
M = 1000

# Parametrico
θ2 = []
for i in 1:M
    muest = rand(Dist, nn)
    θ2 = push!(θ2, mean(muest))
end
var(θ2)

# No Parametrico
mm2 = rand(Dist, nn)
θ3 = []
for i in 1:M
    muest = rand(mm2, nn)
    θ3 = push!(θ3, mean(muest))
end
var(θ3)

Fisher_Info = θ_hat^(-2)
real_var = 1/(Fisher_Info*nn)
