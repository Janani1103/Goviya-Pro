# 🌾 Goviya Pro | Smart Rice Farming Ecosystem

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework: CustomTkinter](https://img.shields.io/badge/Framework-CustomTkinter-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Database: SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)

Goviya Pro is a professional, high-end farm management system designed specifically for the rice farming industry in Sri Lanka. It leverages data-driven insights and AI yield forecasting to help farmers digitalize their workflow and optimize production.

---

## 🎨 UI Design System

For maximum impact and clarity, the system uses a **"Deep Nature"** theme. Below is the direct documentation for our visual architecture.

### 🎨 Visual Identity

| Component | Color Hex | Sample | Description |
| :--- | :--- | :--- | :--- |
| **Primary** | `#0B2E24` | ⬛ | Sidebar Background, Main Headers |
| **Secondary** | `#155D4E` | ⬛ | Nav Hover States, Accent Icons |
| **Accent** | `#3CC47C` | ⬛ | AI Metrics, Growth Indicators |
| **Background** | `#FDFDFD` | ⬜ | Main Application Canvas |
| **Card BG** | `#FFFFFF` | ⬜ | Metric Cards, Input Forms |

### 🖼️ UI Previews & Modules

#### 🏢 Main Dashboard
![Main Dashboard](UI/dash.png)
The central hub for all farm insights, featuring micro-stat cards and historical trend tracking.

#### 🌱 Field & Crop Management
![Field Management](UI/field.png)
Digital registry for all active fields and rice varieties. Supports precision location tracking.

#### 🧪 Input Tracking (Irrigation & Fertilizer)
![Irrigation](UI/irrigation.png)
Record and monitor resource usage with automatic efficiency calculations.

#### 💡 AI Yield Forecaster
![AI Predictor](UI/ai.png)
A smart engine that predicts your next harvest yield with a dynamic confidence score.

---

## ✨ Key Features

- **📊 Management Dashboard**: Real-time overview of field health.
- **🌱 Precision Field Tracking**: Digital record-keeping of field data.
- **🌾 Crop Lifecycle Registry**: Monitor growth stages from seedling to harvest.
- **💡 AI Yield Forecaster**: Predictive engine for harvest outcomes.
- **📄 Professional Reporting**: Analytics module for data-driven decisions.

---

## 📂 Visual Asset Manifest

| Screen | Preview | Description |
| :--- | :--- | :--- |
| **Landing Page** | ![Landing](UI/Landing.png) | High-fidelity entrance flow. |
| **Login/Reg** | ![Reg](UI/registration.png) | Secure user access. |
| **Dashboard** | ![Dash](UI/dash.png) | Farm health overview. |
| **Registry** | ![Field](UI/field.png) | Data management system. |
| **AI Section** | ![AI](UI/ai.png) | Smart predictive engine. |

---

## 🛠️ Technology Stack

- **Frontend**: CustomTkinter, Pillow (Image processing)
- **Backend**: Python, SQLite (Local storage)
- **Analytics**: Matplotlib, Pandas
- **UI Architecture**: Fixed-sidebar navigation with dynamic module switching.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Janani1103/Goviya-Pro.git
   ```
2. Install dependencies:
   ```bash
   pip install customtkinter Pillow tkcalendar matplotlib pandas
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---
*Developed for the future of Sri Lankan Agriculture.*
