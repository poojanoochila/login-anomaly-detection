from preprocessing import preprocess_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib

X, y = preprocess_data("../data/login_data.csv")

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# Handle imbalance
smote = SMOTE(k_neighbors=2, random_state=42)
X_res, y_res = smote.fit_resample(X_train, y_train)

# Logistic Regression Model
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_res, y_res)

y_pred_lr = lr_model.predict(X_test)

print("\n===== Logistic Regression Results =====")
print("Classification Report:\n", classification_report(y_test, y_pred_lr))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))

# Random Forest Model
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_res, y_res)

y_pred_rf = rf_model.predict(X_test)

print("\n===== Random Forest Results =====")
print("Classification Report:\n", classification_report(y_test, y_pred_rf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))

joblib.dump(rf_model, "model.pkl")
print("\nRandom Forest model saved as model.pkl")

joblib.dump(scaler, "scaler.pkl")
print("Scaler saved as scaler.pkl")