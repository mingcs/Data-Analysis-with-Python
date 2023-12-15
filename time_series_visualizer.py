import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import unittest
import matplotlib as mpl
import matplotlib.ticker as mticker
from pandas.plotting import register_matplotlib_converters
from datetime import datetime

register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
def parse_date(x):
    return datetime.strptime(x, "%Y-%m-%d")

df = pd.read_csv(
    "./fcc-forum-pageviews.csv",
    index_col="date",
    parse_dates=["date"],
)

# Clean data
df = df.loc[(df["value"] >= df["value"].quantile(0.025))
            & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(16, 6))

  ax = sns.lineplot(data=df, x="date", y="value")

  ax.set(
      xlabel="Date",
      ylabel="Page Views",
  )

  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = (df.copy().groupby(
      pd.Grouper(freq="M")).mean().rename(columns={"value": "avg"}))

  df_bar["year"] = pd.DatetimeIndex(df_bar.index).year
  df_bar["month"] = pd.DatetimeIndex(df_bar.index).strftime("%B")

  # Convert data to long form
  df_bar = pd.melt(
      df_bar,
      id_vars=["year", "month"],
      value_vars=["avg"],
  )

  sns.set_theme(style="ticks")

  # Draw the chart
  fig = sns.catplot(
      data=df_bar,
      x="year",
      y="value",
      hue="month",
      kind="bar",
      legend=False,
  )

  # Config legend, axes and title
  fig.set_xlabels("Years")
  fig.set_ylabels("Average Page Views")
  plt.legend(
      title="Months",
      loc="upper left",
      labels=[
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
      ],
  )
  return fig.fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.strftime('%b')
    df_box.rename(columns={"value": "views"}, inplace=True)  # Ensure the 'views' column exists

    # Set up the matplotlib figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(ax=ax1, x='year', y='views', data=df_box)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Month-wise Box Plot (Seasonality)
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(ax=ax2, x='month', y='views', data=df_box, order=month_order)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    plt.show()
    return fig