# ## Solution
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import unittest


def draw_plot():
  # Read data from file
  df = pd.read_csv(
      "./epa-sea-level.csv",
      float_precision="legacy").rename(columns={
          "Year": "year",
          "CSIRO Adjusted Sea Level": "sea",
      })

  # Create scatter plot
  plt.figure(1, figsize=(16, 9))
  plt.scatter(df["year"], df["sea"])

  # Create first line of best fit, with existing data
  regress = linregress(df["year"], df["sea"])

  # increase data size for future prediction
  last_year = df["year"].max()
  df = df.append([{"year": y} for y in range(last_year + 1, 2050)])
  plt.plot(
      df["year"],
      regress.intercept + regress.slope * df["year"],
      c="r",
      label="fit all",
  )

  # Create second line of best fit
  df_recent = df.loc[(df["year"] >= 2000) & (df["year"] <= last_year)]
  bestfit = linregress(df_recent["year"], df_recent["sea"])
  df_recent = df_recent.append([{
      "year": y
  } for y in range(last_year + 1, 2050)])
  plt.plot(
      df_recent["year"],
      bestfit.intercept + bestfit.slope * df_recent["year"],
      c="b",
      label="fit recent",
  )

  # Add labels and title
  plt.xlabel("Year")
  plt.ylabel("Sea Level (inches)")
  plt.title("Rise in Sea Level")

  return plt.gca()
