import pandas as pd
import random
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def creatingBellCurve(datapoints, type):

    # VARIABLES
    # DATAPOINTS VARIABLE: is a series of data that you want to run the bell curve calculation on. Can be list or dataframe series.     Ex. df.Column2
    # TYPE VARIABLE: indicates whether the data is whole numbers or percentages. This enables it to be formatted correctly.             2 Choices: 'whole' or 'percent'
    # TYPE VARIABLE: percentages should be in decimal form. For example, 2% should be listed in the data as .02, not 2.

    # disabling case sensitivity in type variable
    type = type.upper()
    print(type)
    
    # creating the graph.
    fig2,ax2 = plt.subplots()

    # calculate the mean and standard deviation
    mean = datapoints.mean()
    stDev = datapoints.std()

    # calculating the values on the graph
    x = np.linspace(mean - 3*stDev, mean + 3*stDev, 100)    # generating random set of x values that are in line with the bell curve relating to the mean and stDev.
    y = stats.norm.pdf(x, mean, stDev)                      # calculating the value on bell curve
    ax2.plot(x, y)                                          # plotting the bell curve line.

    # next we are drawing the vertical lines. We have to start by obtaining the minimum and maximum values being shown on th axes and calculating the range.
    ax2 = plt.gca()                         # initializes
    y_max = ax2.get_ylim()[1]
    y_min = ax2.get_ylim()[0]
    x_max = ax2.get_xlim()[1]
    x_min = ax2.get_xlim()[0]
    x_range = x_max - x_min
    y_range = y_max - y_min

    # AVERAGE LINE
    # Adding vertical line at the mean. axvline draws a vertical line at the value on the x axis, and spans the y min to y max.
    plt.axvline(    x = mean,
                    ymin = 0,
                    ymax = (stats.norm.pdf(mean, mean, stDev) / y_max),
                    linestyle='--', 
                    color='red',
                    linewidth = 1.5
                )
    # adding label to the mean line
    label = f'{round(mean,2)} %' if type == 'PERCENT' else f'{round(mean,2)}' if type == 'WHOLE' else 'invalid type variable'
    plt.text(   x = mean + (.10 * x_range), 
                y =  y_min + (.93 * y_range) ,                  # places it at the top of the y axis, and then moves it slightly to the left on the x-axis
                s = label, 
                fontsize=12, 
                verticalalignment='bottom', 
                horizontalalignment='center'
        )

    # STANDARD DEVIATION LINES
    # adding vertical lines at the standard deviations
    stDevNumbers = [1,2,3]
    stDevNumbers = stDevNumbers + [-a for a in stDevNumbers]            # this adds on the negative values.
    for stDevNum in stDevNumbers:
        stDevValue_X = (stDev * stDevNum) + mean
        stDevValue_Y = stats.norm.pdf(stDevValue_X, mean, stDev)
        plt.axvline(    x = stDevValue_X,
                        ymin = 0,
                        ymax = (stDevValue_Y / y_max),
                        linestyle='solid', 
                        color='black',
                        linewidth = 1.5)

        # Add a label to each standard deviation line
        label = f'{round(stDevValue_X,2)} %' if type == 'PERCENT' else f'{round(stDevValue_X,2)}' if type == 'WHOLE' else 'invalid type variable'
        
        # the labels were overlapping the line. So we had to adjust it. I've made the adjustments around a focal point. See the video "plotting bell curve in MatPlotLib" for explanation.
        # this calculates the x-axis adjustment needed to move the labels around.
        x_focalPoint = x_min + (x_range * .88) if stDevNum >0 else x_min + (x_range * .12)
        diff = (x_focalPoint - stDevValue_X)
        x_adjust = (diff * .3) * (2 if stDevNum == 2 else 1)                            # doubling the adjustment for SD 2 to get it off the bell curve line.

        # this calculates the y-axis adjustment needed to move the labels around
        y_focalPoint = y_min + (y_range * .6)
        diff = (y_focalPoint - stDevValue_Y)
        y_adjust = diff * .1

        plt.text(   x = (stDevValue_X + x_adjust), 
                    y = (stDevValue_Y + y_adjust), 
                    s = label, 
                    fontsize=12, 
                    verticalalignment='bottom', 
                    horizontalalignment='center'
                )
    
    # OVERALL LABELS
    # placing the overall standard deviation label on the chart
    plt.text(   x = x_max * .97, 
                y =  y_max * .89 ,                          # places it at the top of the y axis, and then moves it slightly to the left on the x-axis
                s = f'St Dev: {round(stDev,2)} %' if type == 'PERCENT' else f'St Dev: {round(stDev,2)}' if type == 'WHOLE' else 'invalid type variable', 
                fontsize=10, 
                verticalalignment='top', 
                horizontalalignment='right',
                bbox=dict(facecolor='grey', alpha=0.5)      # creates a grey box around the text
            )

    # placing label on chart that shows overall % of finishes that were positive and negative
    countOfPositivePercentChanges = (datapoints > 0).sum()
    countOfNegativePercentChanges = (datapoints < 0).sum()
    percentOfPositivePercentChanges = round((countOfPositivePercentChanges / len(datapoints)) * 100,1)
    percentOfNegativePercentChanges = round((countOfNegativePercentChanges / len(datapoints)) * 100,1)
    #pd.set_option('display.max_rows', None)

    # positive label
    plt.text(   x = x_max * .97, 
                y =  y_max * .97 ,                          # places it at the top of the y axis, and then moves it slightly to the left on the x-axis
                s = f'Pos: {round(percentOfPositivePercentChanges,2)} %', 
                fontsize=10, 
                verticalalignment='top', 
                horizontalalignment='right',
                bbox=dict(facecolor='green', alpha=0.5)      # creates a grey box around the text
            )  

    # negative label
    plt.text(   x = x_min * .91, 
                y =  y_max * .97 ,                          # places it at the top of the y axis, and then moves it slightly to the left on the x-axis
                s = f'Neg: {round(percentOfNegativePercentChanges,2)} %', 
                fontsize=10, 
                verticalalignment='top', 
                horizontalalignment='left',
                bbox=dict(facecolor='red', alpha=0.5)      # creates a grey box around the text
            ) 

    # adding title and subtitle
    title = f'   Title Here'
    subtitle = f'      Subtitle Here'
    fig2.text(0.5, 0.97, title , ha='center', va='center', fontsize=18)
    fig2.text(0.5, 0.91, subtitle , ha='center', va='center', fontsize=11)

    # miscellaneous tasks
    plt.yticks([])                      # turning off the visibility of the y axis values.
    ax2.grid(True)                      # turning the grid on
    ax2.set_facecolor('#EAECEA')        # coloring the backdrop grey. 
    plt.xlabel('percent_change')        # creating x axis label

    # plotting
    plt.show()

# Number of rows in the DataFrame
num_rows = 10  # You can change this to any desired number

# Create a dictionary to store the random data
data = {
    'Column1': np.random.randint(1, 70, num_rows),
    'Column2': np.random.randint(-.40,40, num_rows),
    'Column3': np.random.randint(1, 70, num_rows)
}

# Create the DataFrame
df = pd.DataFrame(data)

print(df)

creatingBellCurve(df.Column2,'whole')
