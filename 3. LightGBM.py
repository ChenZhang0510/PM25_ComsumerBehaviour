import pandas as pd
import lightgbm as lgb  # Import the LightGBM library
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Data ---
# Replace 'your_data.dta' with the actual path to your Stata file
file_path = 'data0327.dta' 
try:
    df = pd.read_stata(file_path)
    print("Stata .dta file loaded successfully.")


# --- 2. Define Variables and One-Hot Encode ---
# This part is identical to the previous scripts
target_variable = 'logCash'
Y = df[target_variable]
numerical_features = ['logPM', 'logPre', 'rh', 'awin', 'ctemp']
categorical_features = ['vacation', 'month', 'weekday', 'card']
X_numerical = df[numerical_features]
X_categorical_encoded = pd.get_dummies(df[categorical_features], columns=categorical_features, drop_first=True, dtype=int)
X_final = pd.concat([X_numerical, X_categorical_encoded], axis=1)
print(f"Shape of the final feature matrix X (rows, columns): {X_final.shape}")


# --- 3. Initialize and Train the LightGBM Model ---
print("\nTraining LightGBM model...")

# Initialize the LightGBM Regressor model
# Default parameters are often very fast and effective.
lgbm_model = lgb.LGBMRegressor(random_state=42, n_jobs=-1)

# Train the model on the full dataset
lgbm_model.fit(X_final, Y)

print("LightGBM model training complete.")

# --- 4. Extract and Visualize Feature Importance ---
# LightGBM has a convenient built-in plotting function.
# max_num_features=20 displays only the top 20 most important features.
# importance_type='gain' measures importance by the total gains of splits which use the feature.
fig, ax = plt.subplots(figsize=(12, 10))
lgb.plot_importance(lgbm_model, max_num_features=20, ax=ax, importance_type='gain')
plt.title('Top 20 Important Features (LightGBM)')
plt.tight_layout()
# Save the figure
plt.savefig('feature_importance_lgbm.png')
print("\nLightGBM feature importance plot saved as 'feature_importance_lgbm.png'")

# You can also manually extract the importance data
feature_importance_df_lgbm = pd.DataFrame({
    'feature': X_final.columns,
    'importance': lgbm_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 20 most important features and their scores (LightGBM):")
print(feature_importance_df_lgbm.head(20))