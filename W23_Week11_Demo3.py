import pandas as pd
import statsmodels.formula.api as smf
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import column, row, layout
from bokeh.models import Div, Range1d, LinearAxis, RangeSlider

import bokeh.palettes as bp


smokingData = pd.read_csv('Table1_SmokingVsCancer.csv')
model = smf.ols('LungCancerPer100 ~ PercentSmokers', smokingData).fit()

model2 = smf.ols('LungCancerPer100 ~ UnemploymentRate', smokingData).fit()

# Define the data
regressionLine = model.fittedvalues
summaryValues = model.get_prediction().summary_frame()

print(model.summary())

x_data = smokingData['PercentSmokers']
y_data = smokingData['LungCancerPer100']

# Specify the output file
output_file("index.html")

# Create a new figure with a title and axis labels
fig = figure(title="Smoking vs. Lung Cancer Rate Regression", 
             x_axis_label="% Smokers", 
             y_axis_label="Lung Cancer Per 100,000")

fig.line(x_data, 
         regressionLine,
         legend_label = 'Regression Line',
         line_width = 2,
         line_dash = 'dashed',
         color = bp.Spectral4[3])

fig.line(x_data, 
         summaryValues['obs_ci_lower'],
         legend_label = 'Confidence Interval',
         line_width = 2,
         line_dash = 'dashed',
         color = bp.Spectral4[2])

fig.line(x_data, 
         summaryValues['obs_ci_upper'],
         legend_label = 'Confidence Interval',
         line_width = 2,
         line_dash = 'dashed',
         color = bp.Spectral4[2])

# Add a line to the figure
fig.circle(x_data, 
           y_data,
           legend_label = 'Lung Cancer Incidence')

unemploymentFig = figure(title = 'Unemployment vs. Lung Cancer Rate Regression',
                         x_axis_label = "Unemployment Rate",
                         y_axis_label = "Lung Cancer Per 100,000")

model2RegressionLine = model2.fittedvalues
unempSummaryValues = model2.get_prediction().summary_frame()

xDataUnemp = smokingData['UnemploymentRate']

unemploymentFig.line(xDataUnemp, 
         model2RegressionLine,
         legend_label = 'Regression Line',
         line_width = 2,
         line_dash = 'dashed',
         color = bp.Spectral4[3])

unemploymentFig.line(xDataUnemp, 
         unempSummaryValues['obs_ci_lower'],
         legend_label = 'Confidence Interval',
         line_width = 2,
         line_dash = 'dashed',
         color = bp.Spectral4[2])

unemploymentFig.line(xDataUnemp, 
         unempSummaryValues['obs_ci_upper'],
         legend_label = 'Confidence Interval',
         line_width = 2,
         line_dash = 'dashed',
         color = bp.Spectral4[2])

# Add a line to the figure
unemploymentFig.circle(xDataUnemp, 
           y_data,
           legend_label = 'Lung Cancer Incidence')

fig.legend.location = 'top_left'
unemploymentFig.legend.location = 'top_left'


htmlSummary = model.summary().tables[0].as_html()
summaryDiv = Div(text = htmlSummary)

htmlSummaryUnemp = model2.summary().tables[0].as_html()
summaryUnempDiv = Div(text = htmlSummaryUnemp)


dataFig = figure(title = 'Smoking Rates Over Time',
                         x_axis_label = "Year",
                         y_axis_label = "Lung Cancer Per 100,000",
                         y_range = (65, 130))

dataFig.extra_y_ranges['smokers'] = \
    Range1d(start = 0, end = 36)
    
dataFig.add_layout(
    LinearAxis(axis_label = '% Smokers', y_range_name = 'smokers'), 'right')

dataXAxis = smokingData['Year']
dataYAxis = smokingData['LungCancerPer100']
dataY2Axis = smokingData['PercentSmokers']

dataFig.circle(dataXAxis, 
           dataYAxis,
           legend_label = 'Lung Cancer Incidence',
           color = bp.Spectral4[0])

dataFig.circle(dataXAxis, 
           dataY2Axis,
           legend_label = '% Smokers',
           y_range_name = 'smokers',
           color = bp.Spectral4[1])

dataFig.circle(dataXAxis, 
           smokingData['UnemploymentRate'],
           legend_label = 'Unemployment Rate',
           y_range_name = 'smokers',
           color = bp.Spectral4[2])

yearFilter = RangeSlider(
    start = 1985,
    end = 2011,
    value = (1985, 2011),
    step = 1,
    title = "Year Filter")

yearFilter.js_link('value', dataFig.x_range, 'start', attr_selector = 0)
yearFilter.js_link('value', dataFig.x_range, 'end', attr_selector = 1)

# Show the figure
save(layout(dataFig, 
            yearFilter,
            [fig, unemploymentFig], 
            [summaryDiv, summaryUnempDiv], 
            sizing_mode = 'stretch_width'))

