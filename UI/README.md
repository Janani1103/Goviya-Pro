# Goviya Pro | Smart Farm UI Design System

Internal documentation for the user interface, design language, and visual architecture of the Goviya Pro platform.

## 🎨 Visual Identity & Color Palette

The UI follows a professional "Agri-SaaS" aesthetic, utilizing a deep green-centric palette to symbolize growth, stability, and agricultural precision.


## 📐 Layout Architecture

The application uses a **fixed-sidebar navigation** with a **dynamic main content area**.

1.  **Sidebar (Left)**: 240px wide, dark themed. Contains branding, navigation links, and session controls.
2.  **Top Navigation**: Present in external pages (Landing/Login) with branding and CTA buttons.
3.  **Main Canvas (Right)**: Flexible space for modules. Utilizes `CTkScrollableFrame` for data-heavy views like the Dashboard.
4.  **Module Layout**: Typically features a **Header** (back button + title), a **Stats/Entry Section**, and a **Data Table**.

## 🏗️ Core UI Components

### 1. Data Tables (Zebra-Striped)
Optimized for readability. Uses alternating row colors (`#FFFFFF` and `#F8FAFC`) to help users track data rows across large datasets.

### 2. Information Cards
Used in the Dashboard to present "At-a-Glance" metrics. Each card includes an icon, a primary value, and a trend indicator (e.g., "+12% this month").

### 3. Smart Forms
- **Date Pickers**: Integrated `tkcalendar` for precise planting and harvest recording.
- **Option Menus**: Styled dropdowns for Field and Crop selection.
- **Validation-Ready Entries**: Border-highlighted entry fields for data integrity.

### 4. AI Predictor Interface
A specialized module featuring:
- **Intelligence Summaries**: List items with predicted yields.
- **Confidence Visualization**: A circular gauge component (mocked via frames/labels) representing the AI's prediction accuracy.

## 📂 Asset Manifest

Located in the `UI/` directory, these assets serve as visual foundations:

- `Landing.png`: UI blueprint for the landing page.
- `logo.png` & `landing_hero.png`: Brand assets used in the live app.
- `dash.png`, `field.png`, `crop.png`, etc.: High-fidelity mockups for reference.
- `ai.png`: Reference for the yield forecasting interface.

## 🛠️ Technology Stack
- **Framework**: `CustomTkinter` (Modernized Tkinter fork).
- **Rendering Engine**: `PIL` (Pillow) for high-definition asset handling.
- **Graphing**: `Matplotlib` + `FigureCanvasTkAgg` for data visualization.
- **Typography**: Primary typeface is **Inter** (system fallback to Sans-Serif).

## 💡 UX Principles
- **Clarity over Clutter**: Minimize distractions on the dashboard.
- **Visual Feedback**: Hover effects on all primary actions.
- **Persistence**: Navigation state is preserved across module switches.
