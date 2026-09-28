# CareerForge AI - React Frontend Dashboard

## Overview

The `frontend/` directory houses the interactive student-focused dashboard for **CareerForge AI**, built using **React**, **Vite**, **Tailwind CSS**, **React Router**, **Axios**, and **Recharts**.

It communicates directly with the FastAPI REST API backend (`http://localhost:8000/api`) to render real-time skill-gap coverage, machine learning baseline predictions, PyTorch deep neural network confidence scores, market insights, and personalized 3-stage learning roadmaps.

---

## Tech Stack

* **UI Framework**: React 18
* **Build Tool**: Vite 5
* **Styling**: Tailwind CSS
* **Navigation**: React Router 6
* **HTTP Client**: Axios
* **Charts**: Recharts
* **Icons**: Lucide React

---

## Installation & Startup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start Development Server**:
   ```bash
   npm run dev
   ```

4. **Access Dashboard**:
   - **Local URL**: [http://localhost:3000](http://localhost:3000)

---

## Backend API Configuration

The API client layer is located at `src/services/api.js`. It points to:

```js
const API_BASE_URL = 'http://localhost:8000/api';
```

Ensure the FastAPI server is running (`python -m uvicorn app.main:app --reload --port 8000` in `backend/`) to enable real-time predictions and database queries.

---

## Project Structure

```
frontend/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── index.html
├── README.md
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css
    ├── context/
    │   └── CareerContext.jsx       # State management for profile & REST responses
    ├── services/
    │   └── api.js                 # Axios REST client targeting FastAPI endpoints
    ├── components/
    │   ├── Navbar.jsx             # Top bar with backend health indicator
    │   ├── Sidebar.jsx            # Desktop navigation sidebar
    │   ├── MetricCard.jsx         # Metric display card
    │   ├── LoadingSpinner.jsx     # API loading state
    │   ├── ErrorAlert.jsx         # API error handling component
    │   └── SkillBadge.jsx         # Color-coded skill badge
    └── pages/
        ├── Home.jsx               # Landing page & platform overview
        ├── Profile.jsx            # Student Profile form with presets
        ├── Dashboard.jsx          # Master Dashboard aggregating all widgets
        ├── CareerAnalysis.jsx     # Ranked recommendations & ML/DL predictions
        ├── SkillGap.jsx           # Skill match % & matched vs missing gaps
        ├── MarketInsights.jsx     # Recharts market demand visualizations
        └── LearningRoadmap.jsx    # 3-stage personalized learning roadmap
```
