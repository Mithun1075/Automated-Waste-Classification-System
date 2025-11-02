# 🧠 Automated Waste Classification System

The **Automated Waste Classification System** is a machine learning–based web application that classifies waste images into multiple categories such as *Plastic*, *Metal*, *Paper*, *Glass*, *E-waste*, and *Organic*.  
It automates the waste sorting process, promoting efficient recycling and sustainable waste management practices.

---

## 🚀 Features
- Upload waste images for instant classification  
- Predicts waste type using a trained machine learning model  
- User-friendly and responsive web interface  
- Admin dashboard to view and manage classified records  
- Database integration to store image and prediction data  

---

## 🛠️ Tech Stack
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, Django  
**Machine Learning:** TensorFlow / Keras, NumPy, Pandas, OpenCV  
**Database:** MySQL  
**Tools:** Git, GitHub, VS Code  

---

## ⚙️ How It Works
1. User uploads a waste image through the web interface.  
2. The trained CNN (Convolutional Neural Network) model processes the image.  
3. The model predicts the waste category (e.g., Plastic, Metal, Paper, Glass, E-waste, Organic).  
4. The result is displayed instantly, and the data is saved in the database.  

---

## 📂 Project Structure
Automated-Waste-Classification-System/
│
├── dataset/ # Waste image dataset
├── model/ # Trained ML model files
├── static/ # CSS, JS, and images
├── templates/ # HTML templates
├── app/ # Django application folder
├── manage.py # Django management file
└── requirements.txt # Python dependencies


---

## 🧩 Installation & Setup

### Prerequisites
- Python 3.x  
- MySQL Server  
- Virtual Environment (recommended)


---

## 🧩 Installation & Setup

### Prerequisites
- Python 3.x  
- MySQL Server  
- Virtual Environment (recommended)

### Steps
```
# 1️⃣ Clone the repository
git clone https://github.com/<your-username>/Automated-Waste-Classification-System.git

# 2️⃣ Navigate to the project directory
cd Automated-Waste-Classification-System

# 3️⃣ Install required dependencies
pip install -r requirements.txt

# 4️⃣ Run database migrations
python manage.py migrate

# 5️⃣ Start the development server
python manage.py runserver
```
---

📊 Machine Learning Model

- Model trained using CNN (Convolutional Neural Network)
- Dataset includes categorized images of Plastic, Metal, Paper, Glass, E-waste, and Organic waste
- Achieves high accuracy in real-time image classification
- Built using TensorFlow/Keras for image recognition

---

💡 Future Enhancements

- Expand dataset for improved accuracy
- Add real-time camera detection feature
- Include multilingual support for users
- Deploy on cloud platforms (e.g., AWS, Heroku)

---

🧑‍💻 Author

Mithun R
- 🎓 BCA Graduate | 💻 Aspiring Full Stack Developer
- 📫 LinkedIn : https://www.linkedin.com/in/mithun1075/ | Email : mithungugan007@gmail.com
