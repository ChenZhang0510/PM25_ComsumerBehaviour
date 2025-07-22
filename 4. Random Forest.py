import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Data ---
# Replace 'your_data.dta' with the actual path to your Stata file
file_path = 'data0327.dta' 
try:
    df = pd.read_stata(file_path)
    print("Stata .dta file loaded successfully.")



# --- 2. Define Variables ---
# Define the dependent variable (target) Y
target_variable = 'logCash'
Y = df[target_variable]

# Define numerical and categorical independent variables (features)
numerical_features = ['logPM', 'logPre', 'rh', 'awin', 'ctemp']
categorical_features = ['vacation', 'month', 'weekday', 'card']

# Verify that all specified columns exist in the DataFrame
all_cols_needed = [target_variable] + numerical_features + categorical_features
for col in all_cols_needed:
    if col not in df.columns:
        raise ValueError(f"Error: Column '{col}' not found in the DataFrame. Please check spelling and case.")

# Extract numerical features into a separate DataFrame
X_numerical = df[numerical_features]


# --- 3. One-Hot Encode Categorical/Factor Variables ---
print(f"\nPerforming one-hot encoding on the following categorical variables: {categorical_features}")
# Use pd.get_dummies() to convert categorical variables into dummy/indicator variables.
# drop_first=True is used to avoid multicollinearity, which is important for linear models but not essential for Random Forest.
# dtype=int converts the resulting dummy variables to integers (0/1) to save memory.
X_categorical_encoded = pd.get_dummies(df[categorical_features], columns=categorical_features, drop_first=True, dtype=int)


# --- 4. Combine Features into the Final Feature Matrix X ---
# Concatenate the numerical features and the encoded categorical features horizontally (axis=1)
X_final = pd.concat([X_numerical, X_categorical_encoded], axis=1)

print(f"Original number of features: {len(all_cols_needed) - 1}")
print(f"Shape of the final feature matrix X after encoding (rows, columns): {X_final.shape}")
print("Preview of the first 5 rows of the final feature matrix:")
print(X_final.head())


# --- 5. Train Random Forest Model and Get Feature Importance ---
# Note: This can be a computationally intensive step, especially with many dummy variables.
print("\nTraining Random Forest model...")

# Initialize the model
# n_estimators is the number of trees in the forest. Starting with 100 is a good practice.
# n_jobs=-1 uses all available CPU cores to speed up computation.
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

# Train (fit) the model on the data
rf_model.fit(X_final, Y)

print("Model training complete.")


# --- 6. Extract and Visualize the Most Important Features ---
importances = rf_model.feature_importances_
feature_names = X_final.columns

# Create a DataFrame with feature names and their importance scores, then sort it
feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
feature_importance_df = feature_importance_df.sort_values('importance', ascending=False)

# Print the top 20 most important features
print("\nTop 20 most important features and their scores:")
print(feature_importance_df.head(20))

# Visualize the top 20 most important features
plt.figure(figsize=(12, 10))
top_n = 20
plt.barh(feature_importance_df['feature'][:top_n], feature_importance_df['importance'][:top_n])
plt.xlabel('Feature Importance (Gini Importance)')
plt.ylabel('Feature')
plt.title(f'Top {top_n} Most Important Features in Predicting {target_variable}')
plt.gca().invert_yaxis()  # Display the most important feature at the top
plt.tight_layout()
# Save the figure
plt.savefig('feature_importance.png')
print("\nFeature importance plot saved as 'feature_importance.png'")