**Code for: "The Impact of Air Pollution on Consumer Spending Patterns: Evidence from China"**

**Last updated: July 20, 2025**

**Corresponding Author: Chen Zhang (zhangc@clas.ac.cn)**

================================================================================


A. GENERAL INFORMATION
--------------------------------------------------------------------------------
This replication package contains the code and simulated data to reproduce the analysis in the paper "The Impact of Air Pollution on Consumer Spending Patterns: Evidence from China."

The package is organized to allow for the replication of all main econometric models, heterogeneity analyses, robustness checks, and figures presented in the manuscript.


B. SYSTEM REQUIREMENTS
--------------------------------------------------------------------------------
The analysis was conducted using the following software:

1.  **Stata**: Version 16 MP or higher.
    - Required user-written packages: `estout` (for creating regression tables), `logout` (for exporting statistics). You can install these in Stata by running: `ssc install estout, replace` and `ssc install logout, replace`.

2.  **Python**: Version 3.8 or higher.
    - Required libraries:
        - pandas
        - numpy
        - matplotlib
        - seaborn
        - ptitprince
        - scipy
        - scikit-learn
        - xgboost
        - lightgbm
    - You can install these packages using pip:
      `pip install pandas numpy matplotlib seaborn ptitprince scipy scikit-learn xgboost lightgbm`


C. DATA AVAILABILITY
--------------------------------------------------------------------------------
The raw, individual-level transaction data used in this study are proprietary and cannot be shared publicly due to data privacy agreements with the providing institution.


D. INSTRUCTIONS FOR REPLICATION
--------------------------------------------------------------------------------
Please follow the steps below to replicate the analysis.

**Step 1: Setup**
- Place all provided files (Stata .do files, Python .py files, and the simulated .dta data files) in the same working directory.
- In the Stata .do file, ensure the `cd "..."` command points to this working directory.
- In the Python scripts, ensure the `file_path` variables point to the correct .dta file names within the directory.

**Step 2: Main Econometric Analysis (Stata)**
- Run the main Stata script (e.g., `main_analysis.do`).
- This script will perform the following analyses and generate the corresponding tables as .rtf files:
    - **Descriptive Statistics:** `table1.rtf`
    - **Baseline Regressions:** `table2.rtf` (Table 2 in the manuscript)
    - **Heterogeneity by Meal Type:** `table3.rtf` (Table 3 in the manuscript)
    - **Heterogeneity by Demographics/Season:** `table4.rtf` (Table 4 in the manuscript)
    - **Consumption Choice Models:** `table5.rtf` and `table6.rtf` (Tables for the logit models)
    - **Robustness Checks:** `table6.rtf` (Table 7 in the manuscript)

**Step 3: Machine Learning Robustness Checks (Python)**
- To run the machine learning robustness checks described in the paper, execute the following Python scripts individually. Each script trains a model and saves a feature importance plot as a .png file.
    - `Random Forest.py`
    - `Xgboost.py`
    - `LightGBM.py`

**Step 4: Figure Generation (Python)**
- To generate the main figures presented in the paper, run the following script:
    - `5. Figure2&3&4.py` 
- This script will read the data and the output from the Stata spline analysis (`Figure3.csv`, `Figure4.csv`) to produce the final plots.


E. EXPECTED OUTPUT
--------------------------------------------------------------------------------
After running all the scripts, the following output files should be generated in your working directory:

- **Tables (.rtf format):**
  - `table1.rtf`
  - `table2.rtf`
  - `table3.rtf`
  - `table4.rtf`
  - `table5.rtf` (for logit baseline)
  - `table6.rtf` (for logit heterogeneity)
  - `table7.rtf`

- **Figures (.png or .jpg format):**
  - `feature_importance.png` (from Random Forest)
  - `feature_importance_xgb_gain.png` (from XGBoost)
  - `feature_importance_lgbm.png` (from LightGBM)
  - `Fig2.JPG`, `Fig3.JPG`, `Fig4.JPG` (from the main figure generation script)

- **Data for Figures (.csv format):**
  - `Figure3.csv`
  - `Figure4.csv`

=====================================

**End of README.**
