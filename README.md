# Login Anomaly Detection System

This project implements a machine learning-based anomaly detection system to identify suspicious login behavior. It simulates real-world SOC (Security Operations Center) scenarios by analyzing login patterns such as time, IP address, and user behavior.

## Key Objectives
- Detect unusual login activity
- Simulate security monitoring workflows
- Apply anomaly detection techniques used in SOC environments

## Features
- Time-based anomaly detection (odd-hour logins)
- IP-based anomaly detection
- Synthetic dataset generation for realistic scenarios
- Machine learning model for anomaly detection
- Web interface using Flask

## Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Flask
- SQLite

## Project Structure
login-anomaly-detection/
│
├── app.py # Main Flask application
├── requirements.txt # Dependencies
│
├── ml/ # Machine learning modules
│ ├── train_model.py
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

## Usage
python app.py
Then open:
http://127.0.0.1:5000/

## Model Training
python ml/train_model.py

## Security Relevance (SOC Perspective)

#### This project demonstrates:
- Behavioral anomaly detection
- Threat identification logic
- Practical application of ML in cybersecurity
- Understanding of login-based attack patterns

## Limitations
- Uses synthetic dataset
- Not production-scale
- Limited feature engineering

## Future Improvements
- Integrate real-world datasets
- Add risk scoring system
- Implement real-time alerting
- Improve feature engineering

## Note
Large datasets and trained model files are excluded for efficiency. The model can be retrained using the provided scripts.
