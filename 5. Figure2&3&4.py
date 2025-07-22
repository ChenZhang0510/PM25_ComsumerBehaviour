# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:34:42 2024
Generates figures for the study on air quality and consumer behavior.

@author: Chen
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
import ptitprince as pt
from scipy import interpolate

# --- SCRIPT CONFIGURATION ---

# Set Matplotlib parameters to correctly display fonts
# Ensure you have a font that supports the required characters if any non-ASCII are used.
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
plt.rcParams['axes.unicode_minus'] = False # Allows the display of the minus sign

# Set the working directory for the project
os.chdir("E://") 
Data_Base0 = pd.read_stata("./data0327.dta")
pd.set_option('display.max_rows', 10)
# Filter out extreme outliers for better visualization
Data_Base = Data_Base0[Data_Base0.cash < 5000]

# --- FIGURE 2: DESCRIPTIVE STATISTICS PLOTS ---
fig = plt.figure(figsize=(35, 16))
# Define a grid layout for the subplots
gs1 = gridspec.GridSpec(nrows=2, ncols=3, left=0.05, right=0.48)
# Define properties for the median line in boxplots
medianprops = dict(linestyle='-', linewidth=2, color='red')

# Fig 2(a): Time-series of expenditure and PM2.5 concentration
# Create a pivot table to get daily mean/max of cash and PM2.5
Fig2_Data = pd.pivot_table(Data_Base, index='Date', values=['cash', 'APM25'], aggfunc=[np.mean, np.max])
Date = range(len(Fig1_Data))
Cash = Fig2_Data['mean', 'cash'] / 100 * 3 # Adjusting scale for visualization
AQI = Fig2_Data['amax', 'APM25']

ax1 = fig.add_subplot(gs1[0, :])
ax1y = ax1.twinx() # Create a second y-axis

ax1.set_ylim(15, 40)
ax1.tick_params(axis='both', labelsize=14)
ax1.set_xlim(-5, 252)
ax1.text(-1, 38.5, "(a)", fontsize=14)
ax1.plot(Date, Cash, color='tab:blue', label="Daily Expenditure per capita")
ax1.set_ylabel('Daily expenditure per capita($CNY)', fontsize=18, color='b')

ax1y.plot(Date, AQI, color='tab:orange', label="Daily maximum PM2.5 concentration")
ax1y.set_ylabel('Daily maximum PM2.5 concentration($\mathit{ug/{m^3}}$)', fontsize=18, color='b')
ax1y.set_ylim(-10, 600)
ax1y.tick_params(axis='y', labelsize=14)

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax1y.get_legend_handles_labels()
ax1y.legend(lines + lines2, labels + labels2, fontsize=14)

# Format x-axis ticks to show dates
LableAx1 = Fig1_Data.index.tolist()
date = []
tick = np.arange(0, 250, 25)
ticks = np.append(tick, 244)
ax1.set_xticks(ticks, minor=False)
for i in range(len(LableAx1)):
    date.append(str(LableAx1[i])[0:10])
ticks_label = [date[j] for j in ticks]    
ax1.set_xticklabels(ticks_label, rotation=45)


# Fig 2(b): Expenditure by meal type (Raincloud Plot)
ax2 = fig.add_subplot(gs1[-1, 0])
pal = sns.color_palette(n_colors=3)
ax2 = pt.half_violinplot(x=Data_Base.Meal, y=Data_Base.cash / 100, data=Data_Base, 
                         palette=pal, bw=.2, cut=0.,
                         scale="count", width=.6, inner=None, orient="v")
ax2 = sns.stripplot(x=Data_Base.Meal, y=Data_Base.cash / 100, data=Data_Base, 
                    palette=pal, edgecolor="white",
                    size=0.25, jitter=1, zorder=0, orient="v")
bp2 = sns.boxplot(x=Data_Base.Meal, y=Data_Base.cash / 100, data=Data_Base,
                  color="black", width=.1, zorder=10,
                  showcaps=True, boxprops={'facecolor':'none', "zorder":10},
                  showfliers=False, whiskerprops={'linewidth':2, "zorder":10},
                  saturation=1, notch=True, medianprops=medianprops, orient="v")
ax2.tick_params(axis='both', labelsize=14)
ax2.text(-0.4, 33, "(b)", fontsize=14)
ax2.set_ylim(0, 35)
ax2.set_ylabel('Expenditure per capita($CNY)', fontsize=18, color='b')


# Fig 2(c): Daily expenditure by gender (Raincloud Plot)
ax3 = fig.add_subplot(gs1[-1, 1])
pal = sns.color_palette(n_colors=2)
ax3 = pt.half_violinplot(x=Data_Base.Gender, y=Data_Base.cash / 100 * 3, data=Data_Base, palette=pal, bw=.2, cut=0, 
                         scale="count", width=0.6, inner=None, orient="v")
ax3 = sns.stripplot(x=Data_Base.Gender, y=Data_Base.cash / 100 * 3, data=Data_Base, palette=pal, edgecolor="white",
                    size=0.25, jitter=1, zorder=0, orient="v")
ax3 = sns.boxplot(x=Data_Base.Gender, y=Data_Base.cash / 100 * 3, data=Data_Base, color="black", width=.1, zorder=10,
                  showcaps=True, boxprops={'facecolor':'none', "zorder":10},
                  showfliers=False, whiskerprops={'linewidth':2, "zorder":10},
                  saturation=1, notch=True, medianprops=medianprops, orient="v")

ax3.tick_params(axis='both', labelsize=14)
ax3.text(-0.4, 95, "(c)", fontsize=14)
ax3.set_ylim(0, 100)
ax3.set_ylabel('Daily meal expenditure($CNY)', fontsize=18, color='b')

# Fig 2(d): Daily expenditure by academic degree (Raincloud Plot)
ax4 = fig.add_subplot(gs1[-1, -1])
pal = sns.color_palette(n_colors=3)
labels = ['Undergraduate', 'Master\nStudent', 'Ph.D\nStudent']

ax4.tick_params(axis='both', labelsize=14)
ax4.text(-0.4, 95, "(d)", fontsize=14)
ax4.set_ylim(0, 100)

ax4 = pt.half_violinplot(x=Data_Base.Type, y=Data_Base.cash / 100 * 3, data=Data_Base, palette=pal, bw=.2, cut=0, 
                         scale="count", width=0.6, inner=None, orient="v")
ax4 = sns.stripplot(x=Data_Base.Type, y=Data_Base.cash / 100 * 3, data=Data_Base, palette=pal, edgecolor="white",
                    size=0.25, jitter=1, zorder=0, orient="v")
ax4 = sns.boxplot(x=Data_Base.Type, y=Data_Base.cash / 100 * 3, data=Data_Base, color="black", width=.1, zorder=10,
                  showcaps=True, boxprops={'facecolor':'none', "zorder":10},
                  showfliers=False, whiskerprops={'linewidth':2, "zorder":10},
                  saturation=1, notch=True, orient="v", medianprops=medianprops)
ax4.set_xticklabels(labels, rotation=30)
ax4.set_ylabel('Daily meal expenditure($CNY)', fontsize=18, color='b')
        
# Save the combined Figure 2
fig.savefig('Fig2.JPG', dpi=600, bbox_inches='tight', pad_inches=0)


# --- FIGURE 3: NON-LINEAR EFFECT ON EXPENDITURE ---
DataFig2 = pd.read_csv("./Figure3.csv")
fig2, (ax2_1, ax2_2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
Fig2_X_linear = DataFig2.X.apply(lambda x: np.exp(x))
Knot3 = DataFig2.spline_est_3
Knot4 = DataFig2.spline_est_4
Knot5 = DataFig2.spline_est_5
Knot6 = DataFig2.spline_est_6
Knot7 = DataFig2.spline_est_7

# Panel (a): Effect on ln(PM2.5) scale
ax2_1.axhline(y=0, color='grey', linestyle='--')
splines3 = interpolate.splrep(DataFig2.X, Knot3, k=1)
y_bspline3 = interpolate.splev(DataFig2.X, splines3)
Fit3 = ax2_1.plot(DataFig2.X, y_bspline3, "o-", fillstyle='none', color='xkcd:aqua', label="knots=3")

splines4 = interpolate.splrep(DataFig2.X, Knot4, k=2)
y_bspline4 = interpolate.splev(DataFig2.X, splines4)
Fit4 = ax2_1.plot(DataFig2.X, y_bspline4, "o-", fillstyle='none', color='xkcd:coral', label="knots=4")

splines5 = interpolate.splrep(DataFig2.X, Knot5, k=3)
y_bspline5 = interpolate.splev(DataFig2.X, splines5)
Fit5 = ax2_1.plot(DataFig2.X, y_bspline5, "o-", fillstyle='none', color='xkcd:azure', label="knots=5")

splines6 = interpolate.splrep(DataFig2.X, Knot6, k=4)
y_bspline6 = interpolate.splev(DataFig2.X, splines6)
Fit6 = ax2_1.plot(DataFig2.X, y_bspline6, "o-", fillstyle='none', color='xkcd:dark blue', label="knots=6")

splines7 = interpolate.splrep(DataFig2.X, Knot7, k=5)
y_bspline7 = interpolate.splev(DataFig2.X, splines7)
Fit7 = ax2_1.plot(DataFig2.X, y_bspline7, "o-", fillstyle='none', color='xkcd:dark pink', label="knots=7")

ax2_1.set_xlabel('ln daily PM2.5 concentration($\mathit{ug/{m^3}}$)', fontsize=14, color='b')
ax2_1.set_ylabel('Effect on the expenditures(%)', fontsize=14, color='b')
ax2_1.set_ylim(-0.16, 0.09)
ax2_1.tick_params(axis='both', labelsize=14)
ax2_1.set_yticks(np.arange(-0.16, 0.09, 0.04))
ax2_1.text(6, -0.14, "(a)", fontsize=14)

# Panel (b): Effect on original PM2.5 scale
ax2_2.axhline(y=0, color='grey', linestyle='--')
ax2_2.plot(Fig2_X_linear, Knot3, "o", fillstyle='none', color='xkcd:aqua')
splines3 = interpolate.splrep(Fig2_X_linear, Knot3)
y_bspline3 = interpolate.splev(Fig2_X_linear, splines3)
ax2_2.plot(Fig2_X_linear, y_bspline3, color='xkcd:aqua', label="knots=3")

ax2_2.plot(Fig2_X_linear, Knot4, "o", fillstyle='none', color='xkcd:coral')
splines4 = interpolate.splrep(Fig2_X_linear, Knot4)
y_bspline4 = interpolate.splev(Fig2_X_linear, splines4)
ax2_2.plot(Fig2_X_linear, y_bspline4, color='xkcd:coral', label="knots=4")

ax2_2.plot(Fig2_X_linear, Knot5, "o", fillstyle='none', color='xkcd:azure')
splines5 = interpolate.splrep(Fig2_X_linear, Knot5)
y_bspline5 = interpolate.splev(Fig2_X_linear, splines5)
ax2_2.plot(Fig2_X_linear, y_bspline5, color='xkcd:azure', label="knots=5")

ax2_2.plot(Fig2_X_linear, Knot6, "o", fillstyle='none', color='xkcd:dark blue')
splines6 = interpolate.splrep(Fig2_X_linear, Knot6)
y_bspline6 = interpolate.splev(Fig2_X_linear, splines6)
ax2_2.plot(Fig2_X_linear, y_bspline6, color='xkcd:dark blue', label="knots=6")

ax2_2.plot(Fig2_X_linear, Knot7, "o", fillstyle='none', color='xkcd:dark pink')
splines7 = interpolate.splrep(Fig2_X_linear, Knot7)
y_bspline7 = interpolate.splev(Fig2_X_linear, splines7)
ax2_2.plot(Fig2_X_linear, y_bspline7, color='xkcd:dark pink', label="knots=7")

ax2_2.set_xlabel('Daily PM2.5 concentration($\mathit{ug/{m^3}}$)', fontsize=14, color='b')
ax2_2.set_ylim(-0.16, 0.09)
ax2_2.set_yticks(np.arange(-0.16, 0.09, 0.04))
ax2_2.tick_params(axis='both', labelsize=14)
ax2_2.text(500, -0.14, "(b)", fontsize=14)

# Create a shared legend for Figure 3
lines, labels = ax2_1.get_legend_handles_labels()
fig2.legend(lines, labels, loc='upper center', ncol=5, fontsize=14, frameon=False)
fig2.savefig('Fig3.JPG', dpi=600, bbox_inches='tight', pad_inches=0)


# --- FIGURE 4: NON-LINEAR EFFECT ON CONSUMPTION CHOICE ---
DataFig3 = pd.read_csv("./Figure4.csv")
fig3, (ax3_1, ax3_2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
Fig3_X_linear = DataFig3.X.apply(lambda x: np.exp(x))
Knot3 = DataFig3.spline_est_3
Knot4 = DataFig3.spline_est_4
Knot5 = DataFig3.spline_est_5

# Panel (a): Effect on ln(PM2.5) scale, converted to odds ratio effect
splines3 = interpolate.splrep(DataFig3.X, Knot3, k=1)
y_bspline3 = interpolate.splev(DataFig3.X, splines3)
y_bspline3 = np.exp(y_bspline3) - 1
Fit3 = ax3_1.plot(DataFig3.X, y_bspline3, "o-", fillstyle='none', color='xkcd:aqua', label="knots=3")

splines4 = interpolate.splrep(DataFig3.X, Knot4, k=2)
y_bspline4 = interpolate.splev(DataFig3.X, splines4)
y_bspline4 = np.exp(y_bspline4) - 1
Fit4 = ax3_1.plot(DataFig3.X, y_bspline4, "o-", fillstyle='none', color='xkcd:coral', label="knots=4")

splines5 = interpolate.splrep(DataFig3.X, Knot5, k=3)
y_bspline5 = interpolate.splev(DataFig3.X, splines5)
y_bspline5 = np.exp(y_bspline5) - 1
Fit5 = ax3_1.plot(DataFig3.X, y_bspline5, "o-", fillstyle='none', color='xkcd:azure', label="knots=5")

ax3_1.set_xlabel('ln(daily PM2.5 concentration($\mathit{ug/{m^3}}$))', fontsize=14, color='b')
ax3_1.set_ylabel('Effect on the odds ratio for online takeout(%)', fontsize=14, color='b')
ax3_1.set_ylim(0, 5.01)
ax3_1.tick_params(axis='both', labelsize=14)
ax3_1.set_yticks(np.arange(0, 5.01, 1))
ax3_1.legend(loc='best', fontsize=14)
ax3_1.text(6, 0.25, "(a)", fontsize=14)

# Panel (b): Effect on original PM2.5 scale, converted to odds ratio effect
splines3 = interpolate.splrep(Fig3_X_linear, Knot3)
y_bspline3 = interpolate.splev(Fig3_X_linear, splines3)
y_bspline3 = np.exp(y_bspline3) - 1
ax3_2.plot(Fig3_X_linear, y_bspline3, "o-", fillstyle='none', color='xkcd:aqua', label="knots=3")

splines4 = interpolate.splrep(Fig3_X_linear, Knot4)
y_bspline4 = interpolate.splev(Fig3_X_linear, splines4)
y_bspline4 = np.exp(y_bspline4) - 1
ax3_2.plot(Fig3_X_linear, y_bspline4, "o-", fillstyle='none', color='xkcd:coral', label="knots=4")

splines5 = interpolate.splrep(Fig3_X_linear, Knot5)
y_bspline5 = interpolate.splev(Fig3_X_linear, splines5)
y_bspline5 = np.exp(y_bspline5) - 1
ax3_2.plot(Fig3_X_linear, y_bspline5, "o-", fillstyle='none', color='xkcd:azure', label="knots=5")

ax3_2.set_xlabel('Daily PM2.5 concentration($\mathit{ug/{m^3}}$)', fontsize=14, color='b')
ax3_2.set_yticks(np.arange(0, 5.01, 1))
ax3_2.tick_params(axis='both', labelsize=14)
ax3_2.text(500, 0.2, "(b)", fontsize=14)

fig3.savefig('Fig4.JPG', dpi=600, bbox_inches='tight', pad_inches=0)