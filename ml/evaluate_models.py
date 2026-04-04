from preprocessing import preprocess_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import seaborn as sns
import matplotlib.pyplot as plt

X, y = preprocess_data("../data/login_data.csv")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Without SMOTE
model_normal = RandomForestClassifier(random_state=42)
model_normal.fit(X_train, y_train)
y_pred_normal = model_normal.predict(X_test)

print("=== Without SMOTE ===")
print(classification_report(y_test, y_pred_normal))

# With SMOTE
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X_train, y_train)

model_smote = RandomForestClassifier(random_state=42)
model_smote.fit(X_res, y_res)
y_pred_smote = model_smote.predict(X_test)

print("=== With SMOTE ===")
print(classification_report(y_test, y_pred_smote))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_smote)
sns.heatmap(cm, annot=True, fmt='d')
plt.title("Confusion Matrix (SMOTE)")
plt.show()
