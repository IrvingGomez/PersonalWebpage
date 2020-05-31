import plotly.graph_objects as go
import numpy as np

#To get help on how to save plotly graphs into html document
#help(fig.write_html)

Categories = ['Education', 'Cheating', 'Abilities',
                    'Connections', 'Good Luck', 'Hard Work',
                    'Entreprenurial Spirit',
                    'Initial Capital']

Values_High   = [0.28, 0.11, 0.13, 0.09, 0.13, 0.38, 0.27, 0.15]
Values_Medium = [0.33, 0.21, 0.08, 0.32, 0.15, 0.27, 0.16, 0.23]
Values_Low    = [0.18, 0.32, 0.07, 0.39, 0.12, 0.16, 0.16, 0.27]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r           = Values_Low+[Values_Low[0]],
      theta       = Categories+[Categories[0]],
      fill        = 'toself',
      showlegend  = False,
      legendgroup = 'Low',
      hoverinfo   = 'skip'
))

fig.add_trace(go.Scatterpolar(
      r           = Values_Medium+[Values_Medium[0]],
      theta       = Categories+[Categories[0]],
      fill        = 'toself',
      showlegend  = False,
      legendgroup = 'Medium',
      hoverinfo   = 'skip'
))

fig.add_trace(go.Scatterpolar(
      r           = Values_High+[Values_High[0]],
      theta       = Categories+[Categories[0]],
      fill        = 'toself',
      showlegend  = False,
      legendgroup = 'High',
      hoverinfo   = 'skip'
))

fig.add_trace(go.Scatterpolar(
      r             = Values_Low+[Values_Low[0]],
      theta         = Categories+[Categories[0]],
      name          = 'Low',
      legendgroup   = 'Low',
      hovertemplate = '%{r:.0%}'+'<br>%{theta}'
))

fig.add_trace(go.Scatterpolar(
      r             = Values_Medium+[Values_Medium[0]],
      theta         = Categories+[Categories[0]],
      name          = 'Medium',
      legendgroup   = 'Medium',
      hovertemplate = '%{r:.0%}'+'<br>%{theta}'
))

fig.add_trace(go.Scatterpolar(
      r             = Values_High+[Values_High[0]],
      theta         = Categories+[Categories[0]],
      name          = 'High',
      legendgroup   = 'High',
      hovertemplate = '%{r:.0%}'+'<br>%{theta}'
))

fig.update_layout(
    polar = dict(
        radialaxis = dict(showticklabels=False, ticks='', visible=False),
    )#,
    #title=go.layout.Title(text="The Secret of Success")
)

fig.write_html("Radar_Chart_div.html", full_html=False, include_plotlyjs='cdn')

##
##
# To add the value in each edge of the radar chart
fig.update_layout(
    polar = dict(
        radialaxis = dict(showticklabels=False, ticks='', visible=False),
    ),
    #title=go.layout.Title(text="The Secret of Success")
    autosize=False,
    width=800,
    height=800)

fig.add_trace(go.Scatterpolar(
      r=[0.28, 0.11, 0.14, 0.09, 0.135, 0.38, 0.27, 0.15]+
        [0.33, 0.21, 0.0875, 0.32, 0.16, 0.27, 0.16, 0.23]+
        [0.18, 0.32, 0.0625, 0.39, 0.11, 0.16, 0.16, 0.27],
      theta=Categories+Categories+Categories,
      mode='markers+text',
      marker=dict(size=20, color='white', line=dict(width=1.5,
                                        color='DarkSlateGrey')),
      text=((np.array(Values_High+Values_Medium+Values_Low)*100).astype(int)).tolist(),
      showlegend=False,
      hoverinfo = 'skip'
))
