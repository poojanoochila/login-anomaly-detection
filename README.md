# Login Anomaly Detection System

This system implements a supervised machine learning pipeline to identify suspicious login activity, simulating detection workflows used in Security Operations Centers (SOC).

### Algorithms Used
- Random Forest Classifier
- SMOTE (Synthetic Minority Oversampling Technique)

### Problem Context
Login anomaly detection is inherently an **imbalanced classification problem**, where:
- Normal logins = majority class  
- Anomalous/suspicious logins = minority class  

This imbalance can lead to poor detection of real threats if not handled properly.

### Solution Approach

#### 1. Data Preprocessing
- Extracted time-based features (e.g., login hour)
- Encoded categorical data (IP/user behavior patterns)
- Cleaned and structured dataset for model training

#### 2. Handling Class Imbalance (SMOTE)
- Applied SMOTE to generate synthetic anomalous samples
- Balanced the dataset to improve detection of rare events
- Prevented bias toward normal login predictions

#### 3. Model Training (Random Forest)
- Trained a Random Forest classifier on balanced data
- Leveraged ensemble learning for robust predictions
- Captured non-linear relationships in login behavior

### Why This Approach?

- **Random Forest**
  - High accuracy on structured data
  - Resistant to overfitting
  - Suitable for security event classification

- **SMOTE**
  - Essential for cybersecurity datasets with rare attack events
  - Improves recall for anomaly detection

### Detection Logic

The system flags a login as suspicious based on:
- Unusual login time (e.g., late night activity)
- Change in IP address patterns
- Deviation from user’s normal behavior

### Output Interpretation

- The model classifies each login attempt as:
  - **Normal**
  - **Anomalous (Potential Threat)**

### Example Detection

Input:
- Login at 03:12 AM  
- New/unrecognized IP address  

Output:
- **Risk Level: HIGH**
- **Reason:**
  - Unusual login time  
  - Suspicious IP deviation  

### Objectives

This project simulates real-world SOC detection scenarios:
- Behavioral anomaly detection  
- Suspicious login monitoring  
- Early-stage threat identification  

It reflects how security teams detect:
- Account compromise attempts  
- Credential misuse  
- Insider threats  

## Features
- Time-based anomaly detection (odd-hour logins)
- IP-based anomaly detection
- Synthetic dataset generation for realistic scenarios
- Machine learning model for anomaly detection
- Web interface using Flask

## Tech Stack

- **Backend:** Flask  
- **Machine Learning:** Scikit-learn (Random Forest), Imbalanced-learn (SMOTE)  
- **Data Processing:** Pandas, NumPy  
- **Visualization/UI:** HTML, CSS  
- **Dataset:** Synthetic login activity dataset  

## Project Structure
login-anomaly-detection/
│
├── app.py # Main Flask application
├── requirements.txt # Dependencies
│
├── ml/ # Machine learning modules
│ ├── train_model.py
| ├── evaluate_models.py
│ ├── preprocessing.py
│
├── templates/ # HTML templates
├── static/ # CSS, JS files
│
├── data/ # Dataset
│ └── login_sample_1000.csv

## Dataset
A synthetic dataset is used to simulate login behavior:
- Timestamp
- User ID
- IP Address
- Device / Location (if applicable)

Anomalies include:
- Unusual login times
- Suspicious IP changes
- Rapid login attempts

## Installation

```bash
git clone https://github.com/yourusername/login-anomaly-detection.git
cd login-anomaly-detection
pip install -r requirements.txt
```

## Interface Preview

### Login Page
![Home](screenshots/login.png)

### Home Page
![Home](screenshots/home.png)

### Detection Result
![Result](screenshots/report.png)
![Result](screenshots/table.png)

## Usage

```bash
python app.py
```

Then open in browser:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Model Training

```bash
python ml/train_model.py
```

## Security Relevance (SOC Perspective)

This project demonstrates:

* Behavioral anomaly detection
* Threat identification logic
* Practical application of ML in cybersecurity
* Understanding of login-based attack patterns

## Limitations

* Uses synthetic dataset
* Not production-scale
* Limited feature engineering

## Future Improvements

* Integrate real-world datasets
* Add risk scoring system
* Implement real-time alerting
* Improve feature engineering

## Real-World Application

This system can be applied in:
- Security Operations Centers (SOC)
- Fraud detection systems
- User behavior analytics (UBA)
- Insider threat detection
  
## Academic Context

This project was developed as part of a 3rd semester MCA mini-project, with a focus on applying machine learning techniques to cybersecurity use cases such as login anomaly detection.

## Note

Large datasets and trained model files are excluded for efficiency.
The model can be retrained using the provided scripts.

