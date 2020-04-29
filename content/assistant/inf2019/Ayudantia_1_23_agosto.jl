### Irving Gomez Mendez
### January 13th 2019

using Pkg
using Plots
using LaTeXStrings
using Distributions
using StatsPlots
using Random
using StatsBase

# Apply a function to each value of an array and returns a new array
# containing the resulting values:
roundmap(vect, b) = map(x -> round(x, digits = b), vect)

# La densidad de la distribución Weibull de mínimos (de 2 parámetros) está dada por la expresión:

L"f(t;\eta,\beta)=\frac{\beta}{\eta}\left(\frac{t}{\eta}\right)^{\beta-1}
e^{-(t/\eta)^\beta}1\!\!1\,\,_{(0<t<\infty)}"

# Grafica f(x;θ) para varios valores de θ. ¿Existe alguna combinación de los parámetros
# que logre que f sea simétrica alrededor de la moda?

# Definimos la función de densidad
# eta parametro de escala
# beta parametrode forma
dweib_min(x, eta = 1, beta = 1) = beta/eta*(x/eta)^(beta-1)*exp(-(x/eta)^beta)

# Hacemos una secuencia de valores para x
xx = range(0.001, stop = 3, length = 100)

# La siguiente linea mandara un error
yy = dweib_min(xx)

# La manera correcta de hacerlo es
yy = map(dweib_min, xx)
roundmap(yy,3)

plot(xx, yy,
    seriestype = :scatter,
    label = "",
    m = (0.9, :RebeccaPurple, 5),
    background_color = :Lavender
    )
plot!(dweib_min, 0, 3,
    line = (:tomato, 1, 2),
    label = "Weibull(1,1)")

plot(dweib_min, 0, 3,
    label = "Weibull(1,1)",
    background_color = :Lavender,
    lw = 2,
    color = :RebeccaPurple)

# StatsPlots.jl extends Distributions.jl by adding a type recipe for its
# distribution types, so they can be directly interpreted as plotting data:

plot(Weibull(1,1), 0, 3,
    label = "Weibull(1,1)",
    background_color = :Lavender,
    lw = 2,
    color = :RebeccaPurple)

# Si cambiamos el parámetro de forma a 2

plot(Weibull(2,1), 0, 3,
    label = "Weibull(1,2)",
    background_color = :Lavender,
    lw = 2,
    ylabel = L"f(x,\theta)",
    color = :RebeccaPurple)

# Con varios valores de beta (2, 3, 5)

plot!(Weibull(3,1),
    label = "Weibull(1,3)",
    lw = 2,
    ls = :dash,
    color = :orange)
plot!(Weibull(5,1),
    label = "Weibull(1,5)",
    lw = 2,
    ls = :dot,
    color = :green)

# Obtener información sobre funciones y sobre atributos de plot

?plot
plotattr("linestyle")

## Teorema Integral de Probabilidad

#Si U∼Unifcont[0,1], entonces la v.a. F^(-1)(U) tiene la misma distribución que X

# Funcion cuantiles
qweib_min(x, η, β) = η*(log(1/(1-x)))^(1/β)

# Función que genera una muestra (simple) de la distribucion Weibull
function rweib_min(n, η, β)
    u = rand(n) #Generamos una muestra uniforme
    out = map(x -> qweib_min(x, η, β), u)
    return(out)
end

Random.seed!(111)
muestra = rweib_min(50, 2, 6.2)

histogram(muestra,
    label = "Empirical Weibull(2,6.2)",
    normalized = true,
    background_color = :Lavender,
    fillalpha = 0.33,
    color = :RebeccaPurple,
    legend = :topleft)

plot!(Weibull(6.2,2),
    label = "Weibull(2,6.2)",
    lw = 2)

Empirical = ecdf(muestra)

Empirical(1.23)

plot(sort(muestra), map(Empirical, sort(muestra)),
    label = "Empirical Weibull(2,6.2)",
    ylabel = L"F_n(x,\theta)",
    background_color = :Lavender,
    linetype = :steppost,
    lw = 2,
    color = :RebeccaPurple,
    legend = :topleft)

pweib_min(x, η, β) = cdf(Weibull(β, η), x)

plot!(x -> pweib_min(x, 2, 6.2),
    label = "Weibull(2,6.2)",
    lw = 2)
