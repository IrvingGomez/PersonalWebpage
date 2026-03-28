---
title: World Happines Report (WHR) 2017
summary: Applied statistical analysis of the World Happiness Report, focused on well-being and its social drivers.
toc: true

tags:
- Visualization
- Missing Values
- Real Data
- Deep Learning

image:
  focal_point: Smart
---

<style>
  .happiness-control {
    max-width: 42rem;
    margin: 1.2rem 0 1rem;
  }

  .happiness-control label {
    display: block;
    margin-bottom: 0.5rem;
    color: #2d0b57;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
  }

  .happiness-control small {
    display: block;
    margin-top: 0.45rem;
    color: rgba(58, 74, 93, 0.78);
    line-height: 1.45;
  }

  .happiness-viz-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.75fr) minmax(18rem, 1fr);
    gap: 1.5rem;
    align-items: flex-start;
    margin: 1rem 0 1.75rem;
  }

  .happiness-viz-grid .map,
  .happiness-viz-grid .histo {
    min-width: 0;
    width: 100%;
    overflow: hidden;
  }

  .happiness-viz-grid .map {
    grid-column: 1;
  }

  .happiness-viz-grid .histo {
    grid-column: 2;
  }

  .happiness-viz-grid .plotly-graph-div,
  .happiness-viz-grid .js-plotly-plot {
    width: 100% !important;
    max-width: 100% !important;
  }

  .happiness-viz-grid .map .main-svg text,
  .happiness-viz-grid .map .main-svg .gtitle,
  .happiness-viz-grid .map .main-svg .cbtitle,
  .happiness-viz-grid .map .main-svg .xtick text,
  .happiness-viz-grid .map .main-svg .ytick text {
    fill: #2d0b57 !important;
  }

  .latent-viz-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
    align-items: flex-start;
    margin: 1rem 0 1.75rem;
  }

  .latent-viz-grid .view {
    min-width: 0;
    width: 100%;
    overflow: hidden;
  }

  .latent-viz-grid .ae.view {
    grid-column: 1 / -1;
  }

  .latent-viz-pair {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
    align-items: flex-start;
  }

  .latent-viz-pair > * {
    min-width: 0;
    width: 100%;
  }

  .latent-viz-pair > p {
    display: contents;
    margin: 0;
  }

  .latent-viz-grid .plotly-graph-div,
  .latent-viz-grid .js-plotly-plot,
  .latent-viz-pair .plotly-graph-div,
  .latent-viz-pair .js-plotly-plot {
    width: 100% !important;
    max-width: 100% !important;
  }

  .latent-viz-pair figure {
    margin: 0;
  }

  .latent-viz-pair img {
    display: block;
    width: 100%;
    height: auto;
  }

  .latent-schema-figure {
    margin: 0;
  }

  .latent-schema-figure a,
  .latent-schema-figure img {
    display: block;
  }

  @media screen and (max-width: 768px) {
    .happiness-viz-grid {
      gap: 1rem;
    }

    .happiness-viz-grid .map,
    .happiness-viz-grid .histo {
      grid-column: 1;
    }

    .latent-viz-grid,
    .latent-viz-pair {
      gap: 1rem;
      grid-template-columns: minmax(0, 1fr);
    }
  }
</style>

- Data source: World Happiness Report, using only the year 2016.
- Goal: understand the drivers behind happiness, not just the final score.
- Reference points: two hypothetical countries, `"utopia"` and `"dystopia"`.
- Interpretation: `utopia` takes the best observed value for every feature, while `dystopia` takes the worst.

<section id="Imputation Process">
  <h2>Imputation Process</h2>
</section>

Many countries have missing values in 2016, so the project required a dedicated imputation strategy.

**Why imputation was needed**

- Several countries are missing one or more features in 2016.
- First pass: use previous years and average historical records when they exist.
- Limitation: countries without historical records cannot be handled in that first step.
- Temporary decision: leave those countries aside until a second-stage model is available.

**How the integrated score was built**

- Standardize the usable data so each feature lies between `0` and `1`.
- Train an Autoencoder (AE) and use the encoder to project countries into a two-dimensional non-linear latent space.
- Use Principal Component Analysis (PCA) in that latent space to define the main one-dimensional ordering.
- Project `utopia` and `dystopia` onto that ordering after training.
- Define an integrated score from `0` to `10`, where `dystopia = 0` and `utopia = 10`.

**How the missing countries were recovered**

- Train a Random Forest (RF) on countries that already have an integrated score.
- Use that RF to estimate the score of countries with missing values and no historical records.
- Feed the final scores through the decoder part of the AE.
- Use the decoder reconstruction as the final imputation for the missing 2016 values.

This approach is more informative than simply averaging historical values, because the AE can capture more complex non-linear relationships among countries. An imputed version of the data was created as part of this project.

**Workflow summary**

<ol>
 <li>Train an AE and use its encoder.</li>
 <li>Use PCA in the latent space to assign an integrated score to each country.</li>
 <li>Use a RF to estimate the integrated score of countries with missing values.</li>
 <li>Use the AE decoder to reconstruct the missing features.</li>
</ol>

<section id="Visualizations">
  <h2>Visualizations</h2>
</section>

<section id="Maps and Histograms">
  <h3>Maps and Histograms</h3>
</section>

<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<script>
  function styleHappinessPlotlyCharts(targets) {
    if (typeof Plotly === "undefined" || !Plotly.relayout) {
      return;
    }

    var plotTargets = targets && targets.length ? targets : $(".plotly-graph-div");
    var fontColor = "#2d0b57";
    var accentColor = "#7A2BC2";
    var axisLineColor = "rgba(45, 11, 87, 0.22)";
    var whiteValues = ["white", "#ffffff", "rgb(255,255,255)", "rgba(255,255,255,1)", "rgba(255,255,255,1.0)"];

    function normalizeColor(value) {
      return value ? String(value).toLowerCase().replace(/\s+/g, "") : "";
    }

    function isWhiteColor(value) {
      return whiteValues.indexOf(normalizeColor(value)) !== -1;
    }

    function restyleRenderedWhiteVectors(graph) {
      var svgRoot = graph.querySelector(".main-svg");
      if (!svgRoot) {
        return;
      }

      svgRoot.querySelectorAll(".scatterlayer .trace .js-line").forEach(function(path) {
        var stroke = normalizeColor(path.getAttribute("stroke")) || normalizeColor(window.getComputedStyle(path).stroke);
        if (isWhiteColor(stroke) || stroke === "rgb(255,255,255)") {
          path.style.stroke = accentColor;
        }
      });

      svgRoot.querySelectorAll(".scatterlayer .trace .point").forEach(function(point) {
        var fill = normalizeColor(point.getAttribute("fill")) || normalizeColor(window.getComputedStyle(point).fill);
        if (isWhiteColor(fill) || fill === "rgb(255,255,255)") {
          point.style.fill = accentColor;
          point.style.stroke = accentColor;
        }
      });
    }

    window.setTimeout(function() {
      plotTargets.each(function() {
        var graph = this;
        if (!graph || !graph.data || !graph.layout) {
          return;
        }

        var hasGeoTrace = graph.layout.geo || graph.data.some(function(trace) {
          return trace.type === "choropleth" || trace.type === "scattergeo";
        });

        var layoutUpdate = {
          "font.color": fontColor,
          "title.font.color": fontColor,
          "legend.font.color": fontColor,
          "legend.title.font.color": fontColor,
          "paper_bgcolor": "rgba(0,0,0,0)",
          "plot_bgcolor": "rgba(0,0,0,0)"
        };

        if (!hasGeoTrace) {
          layoutUpdate["xaxis.color"] = fontColor;
          layoutUpdate["xaxis.title.font.color"] = fontColor;
          layoutUpdate["xaxis.zerolinecolor"] = axisLineColor;
          layoutUpdate["xaxis.linecolor"] = axisLineColor;
          layoutUpdate["yaxis.color"] = fontColor;
          layoutUpdate["yaxis.title.font.color"] = fontColor;
          layoutUpdate["yaxis.zerolinecolor"] = axisLineColor;
          layoutUpdate["yaxis.linecolor"] = axisLineColor;
          layoutUpdate["scene.xaxis.color"] = fontColor;
          layoutUpdate["scene.yaxis.color"] = fontColor;
          layoutUpdate["scene.zaxis.color"] = fontColor;
        }

        if (!hasGeoTrace) {
          Plotly.relayout(graph, layoutUpdate);
        }

        graph.data.forEach(function(trace, index) {
          var traceUpdate = {};
          var lineColor = trace.line && trace.line.color ? normalizeColor(trace.line.color) : "";
          var markerColor = trace.marker && trace.marker.color ? normalizeColor(trace.marker.color) : "";

          if (trace.line && isWhiteColor(lineColor)) {
            traceUpdate["line.color"] = accentColor;
          }
          if (trace.marker && isWhiteColor(markerColor)) {
            traceUpdate["marker.color"] = accentColor;
          }
          if (Object.keys(traceUpdate).length > 0) {
            Plotly.restyle(graph, traceUpdate, [index]);
          }
        });

        window.requestAnimationFrame(function() {
          restyleRenderedWhiteVectors(graph);
        });
      });
    }, 120);
  }
</script>

<script>
  function renderHappinessPlot(graphId, specUrl) {
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
        if (typeof styleHappinessPlotlyCharts === "function" && window.jQuery) {
          styleHappinessPlotlyCharts(window.jQuery(graph));
        }
        if (typeof Plotly !== "undefined" && Plotly.Plots && Plotly.Plots.resize) {
          Plotly.Plots.resize(graph);
        }
      })
      .catch(function(error) {
        console.error("Failed to render happiness plot", error);
      });
  }

  window.renderHappinessPlot = renderHappinessPlot;
</script>

<!-- Script to say the function of the dropdwon button 'Select Variable' -->
<script>
  $(document).ready(function(){
    function resizeVisiblePlots() {
      if (typeof Plotly === "undefined" || !Plotly.Plots || !Plotly.Plots.resize) {
        return;
      }

      window.setTimeout(function() {
        $(".happiness-viz-grid .map:visible .plotly-graph-div, .happiness-viz-grid .histo:visible .plotly-graph-div").each(function() {
          Plotly.Plots.resize(this);
        });
        styleHappinessPlotlyCharts($(".happiness-viz-grid .map:visible .plotly-graph-div, .happiness-viz-grid .histo:visible .plotly-graph-div"));
      }, 80);
    }

    $("#select_var").change(function(){
      $(this).find("option:selected").each(function(){
        var optionVar = $(this).attr("value");
        if(optionVar){
          $(".explanation").hide();
          $(".map").hide();
          $(".histo").hide();
          $(".explanation." + optionVar).show();
          $(".map." + optionVar).show();
          $(".histo." + optionVar).show();
          resizeVisiblePlots();
        } else{
          $(".explanation").hide();
          $(".map").hide();
          $(".histo").hide();
        }
      });
    }).change();

    $(window).on("resize", resizeVisiblePlots);
    $(window).on("load", function() {
      styleHappinessPlotlyCharts($(".plotly-graph-div"));
    });
  });
</script>



<!-- Variable selector -->
<div class="happiness-control">
    <label for="select_var"><strong>Variable</strong></label>
    <select class="happiness-select" name="select_var" id="select_var">
      <option value="ladder">Happiness score or subjective well-being</option>
      <option value="social">Someone to count on in times of trouble (Social Support)</option>
      <option value="corrupt">Perception of corruption</option>
    </select>
</div>

<div class="ladder explanation">
It is the national average response to the question: "Please imagine a ladder, with
steps numbered from 0 at the bottom to 10 at the top. The top of the ladder represents the best possible life for you and the bottom of the ladder
represents the worst possible life for you. On which step of the ladder would you say you personally feel you stand at this time?"
</div>

<div class="corrupt explanation">
The measure is the national average responses to two questions: "Is corruption widespread throughout the government or not?" and
"Is corruption widespread within businesses or not?" The overall perception is just the average of the responses.
</div>

<div class="social explanation">
Social support (or having someone to count on in times of trouble) is the national average of the responses to the question "If you were in trouble,
do you have relatives or friends you can count on to help you whenever you need them, or not?"
</div>

<!-- Map of Ladder in low resolution -->
<div class="happiness-viz-grid">
<div class="ladder low map">
  <div id="f196c5e3-aa2e-4202-9669-ef736ec9e28c" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("f196c5e3-aa2e-4202-9669-ef736ec9e28c", "/plotly/happiness/ladder-map.json");
  </script>
</div>

<!-- Map of Social Support in low resolution -->
<div class="social low map">
  <div id="8c151ae0-eb5c-4683-b306-dc1dc3ec8cf5" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("8c151ae0-eb5c-4683-b306-dc1dc3ec8cf5", "/plotly/happiness/social-support-map.json");
  </script>
</div>

<!-- Map of Corruption in low resolution -->
<div class="corrupt low map">
  <div id="b89d7239-dd64-44e8-b9df-153b92466074" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("b89d7239-dd64-44e8-b9df-153b92466074", "/plotly/happiness/corruption-map.json");
  </script>
</div>

<!-- Hitogram of Ladder -->
<div class="ladder histo">
  <div id="31cf412f-ada3-4aba-8b52-1b6e432a216b" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("31cf412f-ada3-4aba-8b52-1b6e432a216b", "/plotly/happiness/ladder-histogram.json");
  </script>
</div>

<!-- Hitogram of Social Support -->
<div class="social histo">
  <div id="f382d1bd-199d-4959-b1d7-3d34dee56805" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("f382d1bd-199d-4959-b1d7-3d34dee56805", "/plotly/happiness/social-support-histogram.json");
  </script>
</div>

<!-- Hitogram of Corruption -->
<div class="corrupt histo">
  <div id="ae546f4a-d007-49a9-8733-851329db12f2" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("ae546f4a-d007-49a9-8733-851329db12f2", "/plotly/happiness/corruption-histogram.json");
  </script>
</div>
</div>

<section id="Data Visualization in Latent Spaces">
  <h3>Data Visualization in Latent Spaces</h3>
</section>

<script>
  $(document).ready(function(){
    function resizeVisibleLatentPlots() {
      if (typeof Plotly === "undefined" || !Plotly.Plots || !Plotly.Plots.resize) {
        return;
      }

      window.setTimeout(function() {
        $(".latent-viz-grid .view:visible .plotly-graph-div").each(function() {
          Plotly.Plots.resize(this);
        });
        styleHappinessPlotlyCharts($(".latent-viz-grid .view:visible .plotly-graph-div"));
      }, 80);
    }

    $("#select_view").change(function(){
      $(this).find("option:selected").each(function(){
        var optionValue = $(this).attr("value");
        if(optionValue){
          $(".view").not("." + optionValue).hide();
          $("." + optionValue).show();
          resizeVisibleLatentPlots();
        } else{
	  $(".view").hide();
        }
      });
    }).change();

    $(window).on("resize", resizeVisibleLatentPlots);
  });
</script>

<!-- Visualization selector -->
<div class="happiness-control">
    <label for="select_view"><strong>Latent-space view</strong></label>
    <select class="happiness-select" name="select_view" id="select_view">
      <option value="pca_continent">Visualization: PCA (colored by continent)</option>
      <option value="pca_score">Visualization: PCA (colored by integrated score)</option>
      <option value="ae">Visualization: AE</option>
      <option value="hide">Hide visualization</option>
    </select>
    <small>Choose how to display the dimensionality-reduction view below.</small>
</div>

<div class="latent-viz-grid">
<!-- PCA Plot -->
<div class="pca_continent view ">
  <div id="c9ce7005-9013-4f14-a570-ddb8bfc93311" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("c9ce7005-9013-4f14-a570-ddb8bfc93311", "/plotly/happiness/pca-continent.json");
  </script>
</div>

<div class="pca_score view ">
  <div id="d8259f7b-0196-44da-a023-fadf3468d8e6" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("d8259f7b-0196-44da-a023-fadf3468d8e6", "/plotly/happiness/pca-score.json");
  </script>
</div>

<!-- Biplot -->
<div class="pca_continent pca_score view">
  <div id="f43d9085-eefc-4502-b24d-360bd42fc4e6" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("f43d9085-eefc-4502-b24d-360bd42fc4e6", "/plotly/happiness/pca-line.json");
  </script>
</div>

<!-- Auto-Encoder -->
<div class="ae view latent-viz-pair">
  <div>
  <div id="e8784cf9-6052-499a-8ac3-23aba344e0ec" class="plotly-graph-div" style="height:100%; width:100%;"></div>
  <script type="text/javascript">
    window.renderHappinessPlot("e8784cf9-6052-499a-8ac3-23aba344e0ec", "/plotly/happiness/ae-latent-space.json");
  </script>
  </div>

  <figure class="latent-schema-figure">
    <a data-fancybox="" href="AE_draw_happiness.png" data-caption="Autoencoder schema">
      <img src="AE_draw_happiness.png" alt="Autoencoder schema">
    </a>
    <figcaption>Autoencoder schema</figcaption>
  </figure>
</div>
</div>

<section id="Some comments about the world">
  <h3>Some comments about the world</h3>
</section>

**Main takeaways**

- Global inequality is enormous.
- Qatar reaches a GDP per capita of roughly 136,000 USD, while much of the world remains below 20,000 USD, and Burundi does not reach 400 USD.
- In parts of America and Africa, household income inequality is especially severe.
- Some countries combine low freedom with high sadness and anger.
- Large areas of the map turn red when we look at perceived corruption or generosity.
- There are also more hopeful signals.
- Countries such as Rwanda or Somalia stand out for their efforts against corruption.
- Much of the Americas appears stronger in happiness and enjoyment.
- Across much of the world, people still report that they have someone to count on in times of trouble.
