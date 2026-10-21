# 🎓 EduFinder – College Recommendation Platform

EduFinder is a web-based college recommendation platform that helps students find suitable colleges based on their preferred course, city, college ratings, fees, and other preferences.

The main goal of EduFinder is to make the college selection process easier by providing college information in one place.

## ✨ Features

- 🔍 Search colleges by course or college name.
- 🎯 Filter colleges according to student preferences.
- 📍 Filter colleges by city.
- ⭐ View college ratings.
- 💰 Sort colleges by fees.
- ❤️ Add colleges to your favorites.
- 🏫 View detailed college information.
- 📊 Explore placement details, average packages, and highest packages where available.
- 📱 Simple and user-friendly interface.
- 📞 Contact page for inquiries.

## 🛠️ Technologies Used

**Frontend**
- React.js
- Vite
- HTML5
- CSS3
- JavaScript
- React Router
- Axios

**Backend**
- Node.js
- Express.js

**Database**
- MongoDB Atlas

## 📂 Project Structure

```text
EduFinder/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── data/
│   │   │   └── colleges.js
│   │   ├── page/
│   │   │   └── CollegeDetails.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── index.html
│
├── backend/
│   ├── routes/
│   ├── models/
│   ├── server.js
│   └── package.json
│
└── README.md
```

*Note: Adjust the folder structure above if your actual project uses different filenames or folders.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your GitHub repository URL.

### 2. Navigate to the Project

```bash
cd EduFinder
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Start the Frontend

```bash
npm run dev
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:5173
```

### 5. Start the Backend

Open a new terminal:

```bash
cd backend
npm install
node server.js
```

Configure your MongoDB Atlas connection and required environment variables before starting the backend.

## 🔐 Environment Variables

Create a `.env` file inside the backend folder if your backend requires environment variables.

Example:

```env
PORT=5000
MONGODB_URI=your_mongodb_connection_string
```

**Important:** Never upload database passwords, API keys, or other secrets to GitHub. Add `.env` to your `.gitignore` file.

## 🎯 Project Objectives

- Help students discover colleges that match their preferences.
- Make college comparison easier.
- Provide useful information about courses, fees, ratings, and placements.
- Reduce the time required to research colleges.
- Build a simple and accessible college discovery platform.

## 🚀 Future Enhancements

- Add more colleges and verified course details.
- Implement advanced filtering based on marks and budget.
- Add user authentication and saved favorites.
- Integrate a recommendation algorithm.
- Provide college comparisons.
- Improve mobile responsiveness.
- Add admission eligibility information.

## 👩‍💻 Project Information

**Project Name:** EduFinder

**Project Type:** Web Development / College Recommendation System

**Purpose:** To help students discover and compare colleges according to their preferences.

## 📄 License

This project is created for educational and learning purposes.
