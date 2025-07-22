import pandas as pd
import xgboost as xgb  # Import the XGBoost library
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Data ---
# Replace 'your_data.dta' with the actual path to your Stata file
file_path = 'data0327.dta' 
try:
    df = pd.read_stata(file_path)
    print("Stata .dta file loaded successfully.")



# --- 2. Define Variables and One-Hot Encode ---
# This part is identical to the previous script
target_variable = 'logCash'
Y = df[target_variable]
numerical_features = ['logPM', 'logPre', 'rh', 'awin', 'ctemp']
categorical_features = ['vacation', 'month', 'weekday', 'card']
X_numerical = df[numerical_features]
X_categorical_encoded = pd.get_dummies(df[categorical_features], columns=categorical_features, drop_first=True, dtype=int)
X_final = pd.concat([X_numerical, X_categorical_encoded], axis=1)
print(f"Shape of the final feature matrix X (rows, columns): {X_final.shape}")


# --- 3. Initialize and Train the XGBoost Model ---
print("\nTraining XGBoost model...")

# Initialize the XGBoost Regressor model
# objective='reg:squarederror' is the standard setting for regression tasks.
# n_estimators, learning_rate, max_depth are key hyperparameters that can be tuned.
xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=100,       # Number of trees
    learning_rate=0.1,      # Learning rate (eta)
    max_depth=5,            # Maximum depth of each tree
    random_state=42,
    n_jobs=-1               # Use all available CPU cores
)

# Train the model
xgb_model.fit(X_final, Y)

print("XGBoost model training complete.")


# --- 4. Extract and Visualize Feature Importance ---
# XGBoost offers several ways to measure importance, 'weight' and 'gain' are most common.
# 'weight': The total number of times a feature is used to split the data across all trees.
# 'gain': The average gain (contribution to reducing loss) of splits which use the feature. 'gain' is often more informative.

# Method 1: Visualize by 'gain'
fig, ax = plt.subplots(figsize=(12, 10))
xgb.plot_importance(xgb_model, max_num_features=20, ax=ax, importance_type='gain', title='Top 20 Features by Gain (XGBoost)')
plt.tight_layout()
plt.savefig('feature_importance_xgb_gain.png')
print("\nXGBoost feature importance plot (by gain) saved as 'feature_importance_xgb_gain.png'")

# Method 2: Visualize by 'weight' (frequency)
fig, ax = plt.subplots(figsize=(12, 10))
xgb.plot_importance(xgb_model, max_num_features=20, ax=ax, importance_type='weight', title='Top 20 Features by Weight (XGBoost)')
plt.tight_layout()
plt.savefig('feature_importance_xgb_weight.png')
print("XGBoost feature importance plot (by weight) saved as 'feature_importance_xgb_weight.png'")


# You can also manually extract the importance data for analysis
importance_gain_data = xgb_model.get_booster().get_score(importance_type='gain')
importance_gain_df = pd.DataFrame(importance_gain_data.items(), columns=['feature', 'gain']).sort_values('gain', ascending=False)
print("\nTop 20 most important features and their gain scores (XGBoost):")
print(importance_gain_df.head(20))