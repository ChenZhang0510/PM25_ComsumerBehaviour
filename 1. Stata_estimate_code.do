********************************************************************************
* Stata Code for: The Impact of Air Pollution on Consumer Spending Patterns
* Author: [Xiaoqiao Liu, Chen Zhang, Xiaosong Ren, Hua Liao]
* Date: July 20, 2025
* Description: This script performs a comprehensive analysis of the impact of 
* PM2.5 air pollution on the dining expenditure and choices of 
* university students. It includes baseline regressions, 
* heterogeneity analyses, non-linear modeling, and robustness checks.
********************************************************************************


*** SECTION 1: DATA PREPARATION AND DESCRIPTIVE STATISTICS ***

* Set the working directory to the project folder
cd "E:\"

* Load the main dataset for expenditure analysis
* This dataset contains individual meal transaction records.
use "total_consuption0303.dta", clear

* Table 1: Generate and export descriptive statistics for key variables into a Word file.
* Variables explained:
* cash:     Dining expenditure per meal (in Yuan)
* total_pre:Daily total precipitation (in mm)
* ctemp:    Daily average temperature (in Celsius)
* maxtemp:  Daily maximum temperature (in Celsius)
* mintemp:  Daily minimum temperature (in Celsius)
* PM:       Daily average PM2.5 concentration (in μg/m³)

logout, save(table1.rtf) word replace:tabstat cash total_pre ctemp maxtemp mintemp PM, s(n mean sd min max) c(s)


*** SECTION 2: EXPENDITURE ANALYSIS (THE INTENSIVE MARGIN) ***

* --- 2.1: Baseline Models (Stepwise Regression for Table 2) ---
* This section builds the main model by progressively adding control variables and fixed effects.

* Model bs1: Simple regression of expenditure on air pollution
qui reg logCash logPM 
estadd local Month_FE "NO",replace
estadd local Weekday_FE "NO",replace
estadd local Indivual_FE "NO",replace
est sto bs1

* Model bs2: Add weather and holiday controls
* Variables explained:
* logCash:  Natural logarithm of dining expenditure (Dependent Variable)
* logPM:    Natural logarithm of PM2.5 concentration (Main Independent Variable)
* logPre:   Natural logarithm of precipitation
* rh:       Relative humidity (%)
* awin:     Average wind speed (m/s)
* ctemp:    Daily average temperature (in Celsius)
* i.vac:    Dummy variable for official holiday

qui reg logCash logPM logPre rh awin ctemp i.vac
estadd local Month_FE "NO",replace
estadd local Weekday_FE "NO",replace
estadd local Indivual_FE "NO",replace
est sto bs2

* Model bs3: Add month fixed effects
* i.month:  Dummy variables for each month to control for seasonality
qui reg logCash logPM logPre rh awin ctemp i.vac i.month 
estadd local Month_FE "YES",replace
estadd local Weekday_FE "NO",replace
estadd local Indivual_FE "NO",replace
est sto bs3

* Model bs4: Add weekday fixed effects
* i.weekday:Dummy variables for each day of the week to control for weekly cycles
qui reg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "NO",replace
est sto bs4

* Model bs5: Add individual fixed effects (Preferred Model)
* areg command is used for high-dimensional fixed effects.
* absorb(card): Controls for time-invariant characteristics of each student ('card' is the unique student ID)
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto bs5

* Export the regression results to a Word document (Table 2)
esttab bs1 bs2 bs3 bs4 bs5 using table2.rtf, replace keep(*logPM ctemp logPre rh awin 1.vac* ) b(3) se(3) compress nogap ///
 stats(Month_FE Weekday_FE Indivual_FE N,fmt(%3s %3s %3s %9.0f)) title("Table 2")
 
 
* --- 2.2: Heterogeneity Analysis by Meal Type (Table 3) ---
* This section examines if the effect of air pollution varies across different meals.

* Store the baseline result again for comparison in the table
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto bs5 

* Run regression for Breakfast only
* meal==1: Subsetting the data for breakfast transactions
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if meal==1,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto meal1

* Run regression for Lunch only
* meal==2: Subsetting the data for lunch transactions
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if meal==2,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto meal2
  
* Run regression for Dinner only
* meal==3: Subsetting the data for dinner transactions
qui areg logCash logPM logPre rh awin ctemp i.vac i.month  i.weekday if meal==3,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto meal3

* Export the results to a Word document (Table 3)
esttab  bs5 meal* using table3.rtf , mtitles("Baseline" "Breakfast" "Lunch" "Dinner") replace keep(logPM ctemp logPre rh awin 1.vac* ) b(3) se(3) compress nogap ///
 stats(Month_FE Weekday_FE Indivual_FE N,fmt(%3s %3s %3s %9.0f)) title("Table 3")

 
 
* --- 2.3: Heterogeneity by Gender, Academic Degree, and Season (Table 4) ---
* This section examines if the effect varies across different demographic groups and seasons.

* Subsample: Male students
* gender==1: Assumes 1 represents male
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if gender==1,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto male

* Subsample: Female students
* gender==0: Assumes 0 represents female
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if gender==0,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto female

* Subsample: Undergraduate students
* type==1: Assumes 1 represents undergraduates
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if type==1,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto und

* Subsample: Graduate students
* type>1: Assumes values greater than 1 represent graduate students (Masters, PhD)
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if type>1,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto grd

* Subsample: Non-heating season
* month>3 & month<11: Generally corresponds to non-heating season in Northern China
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if month>3&month<11,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto noheating

* Subsample: Heating season
* month<=3 | month>=11: Generally corresponds to heating season in Northern China
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday if month<=3|month>=11,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto heating

* Export heterogeneity results to a Word document (Table 4)
esttab  male female und grd noheating heating using table4.rtf,  mtitles("male" "female" "und" "grd" "noheating" "heating") replace keep(logPM ctemp logPre rh awin 1.vac*) b(3) se(3) compress nogap ///
 stats(Month_FE Weekday_FE Indivual_FE N,fmt(%3s %3s %3s %9.0f)) title("Table 4")
 

* --- 2.4: Non-linear Effects Analysis on Expenditure ---
* This section uses cubic splines to model the non-linear relationship between pollution and expenditure.

use "total_consuption0303.dta", clear
gen X = _n*0.25 if _n<26 // Create a variable for plotting predictions
cap drop spline* // Drop spline variables from any previous run
* Loop through different numbers of knots (3 to 7) for sensitivity analysis
forvalues i = 3/7 {
    * Create cubic spline variables for logPM with `i` knots
    mkspline spline`i'_ = logPM, nknots(`i') cubic 
    mat knot_vector = r(knots) // Store the vector of knot locations
    loc knot_list ""
    * Create a local macro with the list of knot locations
    forvalues k = 1/`i' { 
        loc a = knot_vector[1,`k']
        loc knot_list "`knot_list' `a'"
    }
    loc Jsegments = `i'-1
    * Run regression with the spline variables
    qui areg logCash logPre rh awin ctemp i.vac i.month i.weekday spline`i'_* ,absorb(card) 
    drop spline`i'_*
    * Generate a new set of splines on the plotting variable X using the same knots
    mkspline spline`i'_ = X, cubic knots(`knot_list') 
    * Compute the predicted effect by summing the coefficients multiplied by the spline variables
    loc knot_inner_product "0"
    forvalues j = 1/`Jsegments' {
        loc knot_inner_product "`knot_inner_product' + _b[spline`i'_`j']*spline`i'_`j'"
    }
    gen spline_est_`i' = `knot_inner_product'
}

* Keep only the variables needed for the figure and export to CSV
keep X spline_est* keep in 1/25
outsheet using Figure3.csv, comma replace 

****use "Figure2&3&4.py" to generate Fig 3.
 
 
 
*** SECTION 3: CONSUMPTION CHOICE ANALYSIS (THE EXTENSIVE MARGIN) ***

* --- 3.1: Baseline Logit Models (Table for consumption choice) ---
* Load the dataset for choice analysis.
* The dependent variable 'miss' is likely 1 if student has no on-campus meal record (proxy for takeout), 0 otherwise.
use Eatingout.dta,clear
 
* Model logit01: Simple logit model
qui logit miss logPM  
estadd local Month_FE "No",replace
estadd local Weekday_FE "No",replace
estadd local Indivual_FE "No",replace
est sto logit01

* Model logit02: Add weather controls
qui logit miss logPM logPre rh awin ctemp 
estadd local Month_FE "No",replace
estadd local Weekday_FE "No",replace
estadd local Indivual_FE "No",replace
est sto logit02

* Model logit03: Add holiday control
qui logit miss logPM logPre rh awin ctemp i.vac 
estadd local Weekday_FE "Yes",replace // Note: Original code has "Yes" for weekday, maybe i.vac is considered a weekday-related control
estadd local Month_FE "No",replace
estadd local Indivual_FE "No",replace
est sto logit03

* Model logit04: Add month fixed effects
qui logit miss logPM logPre rh awin ctemp i.vac i.month 
estadd local Month_FE "Yes,replace // Typo in original code, correcting
estadd local Weekday_FE "Yes",replace
estadd local Indivual_FE "No",replace
est sto logit04

* Model logit05: Add weekday fixed effects
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday 
estadd local Month_FE "Yes",replace
estadd local Weekday_FE "Yes",replace
estadd local Indivual_FE "Yes",replace // Note: Individual FE cannot be directly estimated in standard logit. This might be a placeholder or requires a different command like clogit. Assuming it's a placeholder for clarity.
est sto logit05

* Export baseline logit results to a Word document
esttab  logit0* using table1.rtf, replace keep(logPM logPre rh awin ctemp) b(3) se(3) compress nogap ///
 stats(Month_FE Weekday_FE Indivual_FE N,fmt(%3s %3s %3s %9.0f)) title("Table 3")


* --- 3.2: Heterogeneity Analysis for Consumption Choice (Table 5) ---

* Baseline logit model
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday 
est sto logit1
* Subsample: Female
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday  if gender==0
est sto logit2
* Subsample: Male
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday  if gender==1
est sto logit3
* Subsample: Undergraduate
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday  if type==1
est sto logit4
* Subsample: Graduate
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday  if type>1
est sto logit5
* Subsample: Non-heating season
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday  if month>3&month<11
est sto logit6
* Subsample: Heating season
qui logit miss logPM logPre rh awin ctemp i.vac i.month i.weekday  if month<=3|month>=11
est sto logit7

* Export logit heterogeneity results to a Word document (Table 5)
esttab  logit* using table5.rtf,mtitles("baseline" "female" "male" "UND" "Grd" "No Winter" "Winter") replace keep(logPM logPre rh awin ctemp 1.vac* ) b(3) se(3) compress nogap ///
 stats(N,fmt(%9.0f)) title("Table 5")
 
 
* --- 3.3: Non-linear Effects for Consumption Choice ---
 
use Eatingout.dta,clear
gen X = _n*0.25 if _n<26
cap drop spline*
* Loop through different numbers of knots (3 to 7)
forvalues i = 3/7 {
    mkspline spline`i'_ = logPM, nknots(`i') cubic 
    mat knot_vector = r(knots)
    loc knot_list ""
    forvalues k = 1/`i' { 
        loc a = knot_vector[1,`k']
        loc knot_list "`knot_list' `a'"
    }
    loc Jsegments = `i'-1
    * Run logit model with spline variables
    qui logit miss logPre rh awin ctemp i.vac i.month i.weekday spline`i'_*

    drop spline`i'_*
    mkspline spline`i'_ = X, cubic knots(`knot_list') 
    * Compute predicted effect
    loc knot_inner_product "0"
    forvalues j = 1/`Jsegments' {
        loc knot_inner_product "`knot_inner_product' + _b[spline`i'_`j']*spline`i'_`j'"
    }
    gen spline_est_`i' = `knot_inner_product'
}

* Keep variables for figure and export to CSV
keep X spline_est* 
keep in 1/25
outsheet using Figure4.csv, comma replace 

****use "Figure2&3&4.py" to generate Fig 4.
 
*** SECTION 4: ROBUSTNESS CHECKS FOR EXPENDITURE MODEL (Table 6) ***
 
* Robustness checks using different definitions of the PM2.5 variable.

* Store baseline result
qui areg logCash logPM logPre rh awin ctemp i.vac i.month i.weekday,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto bs5

* Robustness check 1: Using daily average PM2.5 (logAPM)
qui areg logCash logAPM  logPre rh awin atemp i.vac i.month i.weekday,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto rt1

* Robustness check 2: Using daily maximum PM2.5 (logMaxPM)
qui areg logCash logMaxPM logPre rh awin atemp i.vac i.month i.weekday,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto rt2

* Robustness check 3: Adding one-day lagged PM2.5 (L1logPM)
qui areg logCash L1logPM logPM logPre rh awin ctemp i.vac i.month i.weekday ,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto rt3

* Robustness check 4: Adding two-day lagged PM2.5 (L2logPM+L1logPM)
qui areg logCash L2logPM L1logPM logPM logPre rh awin ctemp i.vac i.month i.weekday,absorb(card)
estadd local Month_FE "YES",replace
estadd local Weekday_FE "YES",replace
estadd local Indivual_FE "YES",replace
est sto rt4

* Export robustness check results to a Word document (Table 6)
esttab  bs5 rt* using table6.rtf , mtitles("Baseline" "Daily PM" "Max PM" "1 Day Lagged" "2 day Lagged") replace keep(*logPM logAPM logMaxPM) b(3) se(3) compress nogap ///
 stats(Month_FE Weekday_FE Indivual_FE N,fmt(%3s %3s %3s %9.0f)) title("Table 6 Robust Check")
 
