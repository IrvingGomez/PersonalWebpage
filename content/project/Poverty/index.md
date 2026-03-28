---
title: Poverty in Mexico 2018
summary: Applied statistics work on poverty measurement in Mexico using public datasets and a learned poverty index.
toc: true

tags:
- Visualization
- Real Data
- Deep Learning

image:
  focal_point: Smart
math: true
---

<style>
  .poverty-viz-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
    align-items: flex-start;
    margin: 1rem 0 1.75rem;
  }

  .poverty-viz-panel {
    min-width: 0;
    width: 100%;
  }

  .poverty-viz-panel .plotly-graph-div,
  .poverty-viz-panel .js-plotly-plot {
    width: 100% !important;
    max-width: 100% !important;
  }

  .poverty-viz-label {
    margin: 0 0 0.75rem;
    color: #2d0b57;
    font-weight: 600;
  }

  .poverty-history-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
    align-items: flex-start;
    margin: 1rem 0 1.75rem;
  }

  .poverty-history-panel {
    min-width: 0;
  }

  .poverty-figure-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
    align-items: start;
    margin: 1rem 0 1.75rem;
  }

  .poverty-figure-grid figure {
    margin: 0;
  }

  .poverty-control {
    max-width: 28rem;
    margin: 1rem 0 1.25rem;
  }

  .poverty-control label {
    display: block;
    margin-bottom: 0.5rem;
    color: #2d0b57;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
  }

  .poverty-ae-view {
    margin: 0 0 1.5rem;
  }

  .poverty-ae-view[hidden] {
    display: none !important;
  }

  .poverty-ae-description {
    margin: 0 0 1rem;
  }

  .poverty-ae-description[hidden] {
    display: none !important;
  }

  .poverty-ae-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(18rem, 1fr);
    gap: 1.5rem;
    align-items: flex-end;
    margin: 1rem 0 1.75rem;
  }

  .poverty-ae-views {
    min-width: 0;
  }

  .poverty-ae-schema {
    margin: 0;
  }

  .poverty-ae-schema img {
    display: block;
    width: 100%;
    height: auto;
  }

  .poverty-ae-schema figcaption {
    margin-top: 0.65rem;
    color: rgba(58, 74, 93, 0.78);
    text-align: center;
  }

  @media screen and (max-width: 768px) {
    .poverty-viz-grid {
      grid-template-columns: minmax(0, 1fr);
      gap: 1rem;
    }

    .poverty-history-grid {
      grid-template-columns: minmax(0, 1fr);
      gap: 1rem;
    }

    .poverty-figure-grid {
      grid-template-columns: minmax(0, 1fr);
      gap: 1rem;
    }

    .poverty-ae-layout {
      grid-template-columns: minmax(0, 1fr);
      gap: 1rem;
    }
  }
</style>

This page is a state-level exploration of Coneval's 2018 poverty data for Mexico. The raw data are public and available at <a href="https://www.coneval.org.mx/Medicion/MP/Paginas/Programas_BD_08_10_12_14_16_18.aspx">Coneval</a>.

The page has three goals:

- give a quick historical context for multidimensional poverty measurement
- explain the subset of indicators used here
- build an interpretable poverty ordering of Mexican states

# History

## Human Poverty Index
Before the Multidimensional Poverty Index, poverty was often summarized through the Human Poverty Index (HPI), introduced in 1997 as a complement to the Human Development Index.

There were two versions:

- `HPI-1` for developing countries
- `HPI-2` for high-income OECD countries

A short reference is available at <a href="https://en.wikipedia.org/wiki/Human_Poverty_Index">https://en.wikipedia.org/wiki/Human_Poverty_Index</a>.

<div class="poverty-history-grid">
<div class="poverty-history-panel">

<h3>HPI-1</h3>
<p>The HPI-1 is given by the formula:</p>

$$
\mathrm{HPI\text{-}1}
=
\left[
\frac{1}{3}
\left(
P_1^{\alpha} + P_2^{\alpha} + P_3^{\alpha}
\right)
\right]^{\frac{1}{\alpha}}
$$

<p>where</p>

<ul>
  <li> $P_1$: Probability at birth of not surviving to age 40 (times 100). </li>
  <li> $P_2$: Adult illiteracy rate. </li>
  <li> $P_3$: Arithmetic average of 3 characteristics:
    <ul>
      <li> The percentage of the population without access to safe water. </li>
      <li> The percentage of population without access to health services. </li>
      <li> The percentage of malnourished children under five. </li>
    </ul>
  </li>
  <li> $\alpha$: 3. </li>
</ul>

</div>
<div class="poverty-history-panel">

<h3>HPI-2</h3>
<p>The HPI-2 is given by the formula:</p>

$$
\mathrm{HPI\text{-}2}
=
\left[
\frac{1}{4}
\left(
P_1^{\alpha} + P_2^{\alpha} + P_3^{\alpha} + P_4^{\alpha}
\right)
\right]^{\frac{1}{\alpha}}
$$

<p>where</p>

<ul>
  <li> $P_1$: Probability at birth of not surviving to age 60 (times 100). </li>
  <li> $P_2$: Adults lacking functional literacy skills. </li>
  <li> $P_3$: Population below income poverty line (50% of median adjusted household disposable income). </li>
  <li> $P_4$: Rate of long-term unemployment (lasting 12 months or more). </li>
  <li> $\alpha$: 3. </li>
</ul>

</div>
</div>

## Multidimensional Poverty Index

In 2010, poverty measurement moved toward a multidimensional framework. Mexico played a central role in that transition through Coneval, the autonomous institution responsible for evaluating social development policy.

### History of the Multidimensional Poverty Index in Mexico
The full story is documented by Coneval at <a href="https://www.coneval.org.mx/Medicion/MP/Documents/Como_logro_construir_la_medicion_de_Coneval%20(1).pdf">this report</a>. The short version is:

1. In 2001, the Mexican federal government organized the symposium `Pobreza: Conceptos y Metodologias` because there was still no consensus on how poverty should be measured.
2. The same year, the `CTMP` was created to design an official indicator.
3. That indicator was expected to be:

- simple to communicate
- consistent with common sense
- statistically robust
- easy to replicate

4. Early official indicators appeared in 2002 and 2004.
5. Distrust in government statistics helped motivate the creation of Coneval, which began operating in 2006.
6. From 2006 onward, Coneval built the conceptual and statistical framework for multidimensional poverty measurement using INEGI data sources such as the MCS and ENIGH surveys.

The key methodological shift was clear:

- poverty should not be reduced to income alone
- social rights and economic well-being should be analyzed together
- the framework should remain transparent and reproducible

Coneval's formal methodology is documented here:

<a href="https://www.coneval.org.mx/InformesPublicaciones/InformesPublicaciones/Documents/Metodologia-medicion-multidimensional-3er-edicion.pdf">Methodology for the multidimensional measurement in Mexico</a>

Mexico was the first country to implement this approach nationally, and related versions later influenced poverty measurement in several other countries as well as the UN framework adopted in 2010.

# Data Analysis

## About the Data

This is my own analysis of the 2018 Coneval data. It is inspired by the official framework, but it is not the official Coneval methodology for computing the multidimensional poverty index.

For this page I work at the state level and focus on 10 indicators. I group them into two main blocks.

<b>Social Rights</b>
<ul>
  <li> Basic education (ic rezedu) </li>
  <li> Access to health services (ic asalud) </li>
  <li> Access to social security (ic segsoc) </li>
  <li> Home's quality and space (ic cv) </li>
  <li> Access to basic services at home (ic sbv) </li>
  <li> Access to quality food (ic ali) </li>
</ul>

Two derived indicators summarize whether these deprivations accumulate:

<ul>
  <li> Privation (carencias). This equals one when a person lacks at least one of the previous social rights. </li>
  <li> Extreme privation (carencias3). This equals one when a person lacks at least three of the previous social rights. </li>
</ul>

<b>Economic Well-being</b>

Income is translated into two poverty thresholds:

<ul>
  <li> Poverty line by income (plb). This equals one when income is insufficient to cover basic needs. </li>
  <li> Extreme poverty line by income (plb m). This equals one when income is insufficient even for basic food needs. </li>
</ul>

Coneval also tracks broader inequality variables that I do not use on this page, for example:

<b>Society</b>
<ul>
  <li> Gini coefficient in income </li>
  <li> Access to paved roads </li>
</ul>

The combination of income poverty and social deprivation creates four broad situations:

<ul>
  <li> Category I: income above the poverty line and no deprivation. </li>
  <li> Category II: income above the poverty line, but with some deprivation. </li>
  <li> Category III: no deprivation, but income below the poverty line. </li>
  <li> Category IV: income below the poverty line and with deprivation. </li>
</ul>

If we replace the basic thresholds with the extreme ones, we can isolate extreme poverty.

<div class="poverty-figure-grid">
{{<figure src="pobreza_1.png" title="The four categories.">}}

{{<figure src="pobreza_extrema.png" title="The four categories and extreme poverty.">}}
</div>

## My Analysis

### The autoencoder (AE) and the construction of a poverty index
The starting point is simple: each state is represented by a 10-dimensional vector containing the average value of each indicator.

To anchor the space, I added two hypothetical entities:

- `Dystopia`: nobody has access to the relevant social rights and everyone falls below the extreme poverty line
- `Utopia`: everyone enjoys the social rights and nobody falls below the poverty line

I then trained an autoencoder on the states plus those two reference points. The purpose was not prediction, but representation. The encoder learns a compact two-dimensional space where the states line up in a way that follows common sense: the more industrialized northern states lie closer to `Utopia`, while poorer southern states lie closer to `Dystopia`.

From that latent space, I took the first principal component and used it as a one-dimensional poverty scale. I call the result the `AE poverty index`:

- `Utopia` is normalized to `0`
- `Dystopia` is normalized to `1`
- each state receives a value based on its position along that line

The next plots show that latent-space ordering and the induced index.

### AE poverty index

<div class="poverty-control">
  <label for="ae_color_view"><strong>Color scale</strong></label>
  <select id="ae_color_view" name="ae_color_view">
    <option value="mexico" selected>Just Mexico</option>
    <option value="utopia">Dystopia and Utopia</option>
  </select>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  var select = document.getElementById("ae_color_view");
  var mexicoView = document.querySelector(".poverty-ae-mexico");
  var utopiaView = document.querySelector(".poverty-ae-utopia");
  var mexicoDescription = document.querySelector(".poverty-ae-description-mexico");
  var utopiaDescription = document.querySelector(".poverty-ae-description-utopia");

  if (!select || !mexicoView || !utopiaView) {
    return;
  }

  function resizeVisiblePlots(container) {
    if (typeof Plotly === "undefined" || !Plotly.Plots || !Plotly.Plots.resize) {
      return;
    }

    window.setTimeout(function() {
      Array.prototype.forEach.call(
        container.querySelectorAll(".js-plotly-plot, .plotly-graph-div"),
        function(plot) {
          Plotly.Plots.resize(plot);
        }
      );
    }, 160);
  }

  function updateAeView() {
    var showMexico = select.value === "mexico";

    mexicoView.hidden = !showMexico;
    utopiaView.hidden = showMexico;

    if (mexicoDescription && utopiaDescription) {
      mexicoDescription.hidden = !showMexico;
      utopiaDescription.hidden = showMexico;
    }

    resizeVisiblePlots(showMexico ? mexicoView : utopiaView);
  }

  select.addEventListener("change", updateAeView);
  updateAeView();
});
</script>

<div class="poverty-ae-description poverty-ae-description-mexico">
This view colors the states using only their relative positions inside Mexico. It is the better option if the goal is to compare inequality between states.
</div>

<div class="poverty-ae-description poverty-ae-description-utopia" hidden>
This view uses the full `Dystopia` to `Utopia` scale. It is useful when the goal is to compare each state to the two extreme reference cases.
</div>

<div class="poverty-ae-layout">
<div class="poverty-ae-views">
<div class="poverty-ae-view poverty-ae-utopia" hidden>

<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
// Restyle legacy Plotly charts so they stay readable against the site background.
(function() {
  var fontColor = "#2d0b57";
  var accentColor = "#7A2BC2";
  var axisLineColor = "rgba(45, 11, 87, 0.22)";
  var gridColor = "rgba(45, 11, 87, 0.10)";
  var whiteValues = ["white", "#ffffff", "rgb(255,255,255)", "rgba(255,255,255,1)", "rgba(255,255,255,1.0)"];

  function normalizeColor(value) {
    return value ? String(value).toLowerCase().replace(/\s+/g, "") : "";
  }

  function isWhiteColor(value) {
    return whiteValues.indexOf(normalizeColor(value)) !== -1;
  }

  function repaintPovertySvg(graph) {
    if (!graph) {
      return;
    }

    [
      ".shapelayer path",
      ".shapelayer line",
      ".scatterlayer .trace path",
      ".scatterlayer .trace line"
    ].forEach(function(selector) {
      Array.prototype.forEach.call(graph.querySelectorAll(selector), function(node) {
        var stroke = normalizeColor(node.getAttribute("stroke"));
        var fill = normalizeColor(node.getAttribute("fill"));
        var styleStroke = normalizeColor(node.style && node.style.stroke);

        if (isWhiteColor(stroke) || isWhiteColor(styleStroke)) {
          node.setAttribute("stroke", accentColor);
        }

        if (isWhiteColor(fill)) {
          node.setAttribute("fill", accentColor);
        }
      });
    });

    Array.prototype.forEach.call(graph.querySelectorAll(".main-svg text"), function(node) {
      if (isWhiteColor(node.getAttribute("fill"))) {
        node.setAttribute("fill", fontColor);
      }
    });
  }

  function stylePovertyPlotlyCharts(targets) {
    if (typeof Plotly === "undefined") {
      return;
    }

    var graphs = targets && targets.length ? targets : document.querySelectorAll(".plotly-graph-div");

    Array.prototype.forEach.call(graphs, function(graph) {
      if (!graph || !graph.layout || !graph.data) {
        return;
      }

      var layoutUpdate = {
        "font.color": fontColor,
        "title.font.color": fontColor,
        "legend.font.color": fontColor,
        "legend.title.font.color": fontColor,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "xaxis.color": fontColor,
        "xaxis.title.font.color": fontColor,
        "xaxis.gridcolor": gridColor,
        "xaxis.zerolinecolor": axisLineColor,
        "xaxis.linecolor": axisLineColor,
        "yaxis.color": fontColor,
        "yaxis.title.font.color": fontColor,
        "yaxis.gridcolor": gridColor,
        "yaxis.zerolinecolor": axisLineColor,
        "yaxis.linecolor": axisLineColor,
        "scene.xaxis.color": fontColor,
        "scene.yaxis.color": fontColor,
        "scene.zaxis.color": fontColor
      };

      if (graph.layout.coloraxis && graph.layout.coloraxis.colorbar) {
        layoutUpdate["coloraxis.colorbar.title.font.color"] = fontColor;
        layoutUpdate["coloraxis.colorbar.tickfont.color"] = fontColor;
      }

      if (graph.layout.shapes && graph.layout.shapes.length) {
        graph.layout.shapes.forEach(function(shape, index) {
          if (shape.line && isWhiteColor(shape.line.color)) {
            layoutUpdate["shapes[" + index + "].line.color"] = accentColor;
          }
        });
      }

      Plotly.relayout(graph, layoutUpdate).then(function() {
        repaintPovertySvg(graph);
      });

      graph.data.forEach(function(trace, index) {
        var traceUpdate = {};

        if (trace.line && isWhiteColor(trace.line.color)) {
          traceUpdate["line.color"] = accentColor;
        }

        if (trace.marker && isWhiteColor(trace.marker.color)) {
          traceUpdate["marker.color"] = accentColor;
        }

        if (Object.keys(traceUpdate).length > 0) {
          Plotly.restyle(graph, traceUpdate, [index]).then(function() {
            repaintPovertySvg(graph);
          });
        }
      });

      if (!graph.__povertyAfterPlotBound && typeof graph.on === "function") {
        graph.on("plotly_afterplot", function() {
          repaintPovertySvg(graph);
        });
        graph.__povertyAfterPlotBound = true;
      }

      window.setTimeout(function() {
        repaintPovertySvg(graph);
      }, 200);
    });
  }

  function renderPovertyPlot(graphId, specUrl) {
    var graph = document.getElementById(graphId);

    if (!graph) {
      return;
    }

    fetch(specUrl)
      .then(function(response) {
        if (!response.ok) {
          throw new Error("Failed to load Plotly spec: " + response.status);
        }
        return response.json();
      })
      .then(function(spec) {
        return Plotly.newPlot(graphId, spec.data, spec.layout, spec.config);
      })
      .then(function() {
        if (typeof window.stylePovertyPlotlyCharts === "function") {
          window.stylePovertyPlotlyCharts([graph]);
        }
        if (typeof window.resizeVisiblePlots === "function") {
          window.resizeVisiblePlots([graph]);
        }
      })
      .catch(function(error) {
        console.error("Failed to render poverty plot", error);
      });
  }

  window.renderPovertyPlot = renderPovertyPlot;
  window.stylePovertyPlotlyCharts = stylePovertyPlotlyCharts;
  window.addEventListener("load", function() {
    window.setTimeout(function() {
      stylePovertyPlotlyCharts();
    }, 200);
  });
})();
</script>


<div>
  <div id="fddbe2f8-e752-45d3-a5a6-9b9e7977e1a0" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("fddbe2f8-e752-45d3-a5a6-9b9e7977e1a0", "/plotly/poverty/ae-utopia.json");
  </script>
</div>

</div>
<div class="poverty-ae-view poverty-ae-mexico">

<div>
  <div id="11cac3b4-ac2e-493d-9c6c-202ec2b94685" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("11cac3b4-ac2e-493d-9c6c-202ec2b94685", "/plotly/poverty/ae-mexico.json");
  </script>
</div>

</div>

</div>
<figure class="poverty-ae-schema">
  <img src="AE_draw_poverty.png" alt="Autoencoder schema">
  <figcaption>Autoencoder schema</figcaption>
</figure>
</div>

### Use of PCA to explain the poverty index
The weakness of the autoencoder approach is interpretability. It gives a sensible ordering, but not a simple explanation of why that ordering appears.

To make the result more interpretable, I also ran a PCA on the same 10-dimensional state vectors and kept the first two principal components. This gives a linear approximation of the data and allows a biplot.

The main takeaways are:

- the first principal component behaves like a weighted average of deprivation variables
- `Access to basic services at home` has the strongest loading, suggesting that it captures one of the largest dimensions of inequality across states
- `Access to health services` has the weakest loading, suggesting less variation across states for that indicator
- the second principal component is harder to interpret, especially because both `Dystopia` and `Utopia` fall on the same side of it

So I treat the first component as informative and the second one with caution.

### PCA, colors considering Dystopia and Utopia


<div class="poverty-viz-grid">
<div class="poverty-viz-panel">
<p class="poverty-viz-label">PCA projection</p>

<div>
  <div id="bd764fad-f588-4c19-a75f-05c532f4fd2d" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("bd764fad-f588-4c19-a75f-05c532f4fd2d", "/plotly/poverty/pca-projection.json");
  </script>
</div>

</div>
<div class="poverty-viz-panel">
<p class="poverty-viz-label">Biplot</p>

<div>
  <div id="4dc6992c-6ebb-4984-9669-00033a3bd3b4" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("4dc6992c-6ebb-4984-9669-00033a3bd3b4", "/plotly/poverty/pca-biplot.json");
  </script>
</div>
</div>
</div>

### Histograms

These histograms focus on five variables that I consider especially important to reduce: privation, extreme privation, poverty by income, extreme poverty by income, and lack of food.

<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>

<!-- Script to say the function of the dropdwon button 'Select Variable -->
<script>
$(document).ready(function(){
    $("#select_var").change(function(){
        $(this).find("option:selected").each(function(){
            var optionValue = $(this).attr("value");
            if(optionValue){
                $(".histo").not("." + optionValue).hide();
                $("." + optionValue).show();
            } else{
                $(".histo").hide();
            }
        });
    }).change();
});
</script>

<!-- Dropdwon button 'Select Variable' -->
<div>
<select id="select_var">
    <option value="privation">Privation</option>
    <option value="extreme_privation">Extreme Privation</option>
    <option value="poverty_income">Poverty by Income</option>
    <option value="extreme_poverty_income">Extreme Poverty by Income</option>
    <option value="lack_food">Lack of Food</option>
</select>
</div>

<div class="privation histo">
<b>Histogram of Privation</b>
<div>
  <div id="9d83b84d-8994-4c97-bbe1-d1cac38323c6" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("9d83b84d-8994-4c97-bbe1-d1cac38323c6", "/plotly/poverty/privation-histogram.json");
  </script>
</div>
</div>

<div class="extreme_privation histo">
<b>Histogram of Extreme Privation</b>
<div>
  <div id="87352969-ff3e-4a96-8be5-3f93b7f7de27" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("87352969-ff3e-4a96-8be5-3f93b7f7de27", "/plotly/poverty/extreme-privation-histogram.json");
  </script>
</div>
</div>

<div class="poverty_income histo">
<b>Histogram of Poverty by Income</b>
<div>
  <div id="212c420e-773b-4ffa-8813-6f71aa3d9513" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("212c420e-773b-4ffa-8813-6f71aa3d9513", "/plotly/poverty/poverty-income-histogram.json");
  </script>
</div>
</div>

<div class="extreme_poverty_income histo">
<b>Histogram of Extreme Poverty by Income</b>
<div>
  <div id="c7615071-634e-4e57-bb1c-e04546fbf798" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("c7615071-634e-4e57-bb1c-e04546fbf798", "/plotly/poverty/extreme-poverty-income-histogram.json");
  </script>
</div>
</div>

<div class="lack_food histo">
<b>Histogram of Lack of Food</b>
<div>
  <div id="ecaf5bf1-21b1-4adc-9a97-95dac5e96fc2" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("ecaf5bf1-21b1-4adc-9a97-95dac5e96fc2", "/plotly/poverty/lack-food-histogram.json");
  </script>
</div>
</div>

### Boxplot

The boxplot summarizes the same indicators in a more compact way. It makes medians, spread, and outliers easier to compare at a glance.

<div>
  <div id="e8acf2b6-6490-4932-b316-05e24ce01e7e" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderPovertyPlot("e8acf2b6-6490-4932-b316-05e24ce01e7e", "/plotly/poverty/poverty-sources-boxplot.json");
  </script>
</div>
