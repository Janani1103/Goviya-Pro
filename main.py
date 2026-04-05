import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime
import sqlite3
import os
from PIL import Image
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class SmartRiceFarmingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Goviya Pro | Smart Rice Farming System")
        self.geometry("1280x800")
        self.minsize(1000, 700)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
 
        self.primary_color = "#0B2E24"    
        self.secondary_color = "#155D4E" 
        self.accent_color = "#3CC47C"    
        self.success_color = "#10B981"   
        self.warning_color = "#F59E0B"    
        self.danger_color = "#EF4444"   
        self.text_main = "#1E293B"       
        self.text_dim = "#64748B"        
        self.bg_color = "#FDFDFD"        
        self.sidebar_bg = "#0B2E24"      
        self.card_bg = "#FFFFFF"
        self.border_color = "#E2E8F0"

        self.configure(fg_color=self.bg_color)

        self.init_db()

        self.title_font = ctk.CTkFont(family="Inter", size=36, weight="bold")
        self.header_font = ctk.CTkFont(family="Inter", size=24, weight="bold")
        self.sub_header_font = ctk.CTkFont(family="Inter", size=18, weight="bold")
        self.normal_font = ctk.CTkFont(family="Inter", size=14, weight="normal")
        self.button_font = ctk.CTkFont(family="Inter", size=14, weight="bold")
        self.small_font = ctk.CTkFont(family="Inter", size=12, weight="normal")

        self.load_assets()

        self.create_main_container()
        self.create_all_pages()
        
        self.show_page("Landing")

    def init_db(self):
        self.conn = sqlite3.connect("goviya_farm.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS fields (id INTEGER PRIMARY KEY, name TEXT, location TEXT, size REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS crops (id INTEGER PRIMARY KEY, field_id INTEGER, variety TEXT, planting_date TEXT, stage TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS water_schedules (id INTEGER PRIMARY KEY, field_id INTEGER, date TEXT, quantity REAL, notes TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS fertilizers (id INTEGER PRIMARY KEY, field_id INTEGER, type TEXT, quantity REAL, date TEXT, notes TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS harvests (id INTEGER PRIMARY KEY, field_id INTEGER, date TEXT, yield REAL, profit REAL, notes TEXT)''')
        self.conn.commit()

    def load_assets(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        def safe_load(filename, size):
            path = os.path.join(script_dir, filename)
            if os.path.exists(path):
                img = Image.open(path)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            return None

        self.logo_img = safe_load("logo.png", (40, 40))
        self.hero_img = safe_load("landing_hero.png", (600, 400))

        if not self.logo_img: self.logo_img = None
        if not self.hero_img: self.hero_img = None

    def create_main_container(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.sidebar_bg)
        self.sidebar.grid_rowconfigure(4, weight=1)

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(30, 40), padx=20, fill="x")
        
        if self.logo_img:
            logo_l = ctk.CTkLabel(logo_frame, image=self.logo_img, text="")
            logo_l.pack(side="left")
        
        ctk.CTkLabel(logo_frame, text="GOVIYA", font=ctk.CTkFont(family="Inter", size=24, weight="bold"), text_color="white").pack(side="left", padx=10)

        self.sidebar_btns = {}
        nav_items = [
            ("Dashboard", "🏠"),
            ("Fields", "🌱"),
            ("Crops", "🌾"),
            ("Irrigation", "💧"),
            ("Fertilizer", "🧪"),
            ("Harvest", "📈"),
            ("Reports", "📊"),
            ("AI Predictor", "💡"),
        ]
        
        for name, icon in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=f"  {icon}  {name}", 
                font=self.normal_font,
                height=42, 
                anchor="w",
                fg_color="transparent",
                text_color="#94A3B8",
                hover_color="#155D4E",
                corner_radius=10,
                command=lambda n=name: self.show_page(n)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.sidebar_btns[name] = btn

        pro_card = ctk.CTkFrame(self.sidebar, fg_color="#1E293B", corner_radius=12)
        pro_card.pack(side="bottom", fill="x", padx=15, pady=(10, 20))
        ctk.CTkLabel(pro_card, text="Goviya Pro v2.4", font=self.small_font, text_color=self.accent_color).pack(pady=(12, 2))
        ctk.CTkLabel(pro_card, text="Enterprise Account", font=ctk.CTkFont(size=10), text_color="#64748B").pack(pady=(0, 12))

        ctk.CTkButton(
            self.sidebar, 
            text="  🔒 Logout", 
            font=self.normal_font,
            fg_color="transparent",
            text_color="#F87171",
            hover_color="#450A0A",
            height=40,
            command=lambda: self.show_page("Login")
        ).pack(side="bottom", fill="x", padx=15, pady=5)

        self.main_content = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        self.main_content.pack(fill="both", expand=True, side="right")

    def create_all_pages(self):
        self.pages = {}

        self.pages["Landing"] = self.create_landing_page()
        self.pages["Login"] = self.create_login_page()
        self.pages["Register"] = self.create_register_page()
        self.pages["Dashboard"] = self.create_dashboard_page()
        self.pages["Fields"] = self.create_fields_page()
        self.pages["Crops"] = self.create_crops_page()
        self.pages["Irrigation"] = self.create_irrigation_page()
        self.pages["Fertilizer"] = self.create_fertilizer_page()
        self.pages["Harvest"] = self.create_harvest_page()
        self.pages["Reports"] = self.create_reports_page()
        self.pages["AI Predictor"] = self.create_ai_predictor_page()

    def show_page(self, page_name, save_history=True):
        if not hasattr(self, 'page_stack'):
            self.page_stack = []
        
        if save_history:
            if not self.page_stack or self.page_stack[-1] != page_name:
                self.page_stack.append(page_name)

        for name, btn in self.sidebar_btns.items():
            if name == page_name:
                btn.configure(fg_color=self.secondary_color, text_color="white", font=self.button_font)
            else:
                btn.configure(fg_color="transparent", text_color="#94A3B8", font=self.normal_font)

        external_pages = ["Landing", "Login", "Register"]
        
        if page_name in external_pages:
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side="left", fill="y")
            self.main_content.pack(side="right", fill="both", expand=True)

        for p in self.pages.values():
            p.pack_forget()

        if page_name == "Dashboard":
            self.refresh_dashboard_stats()
        elif page_name == "Fields":
            self.load_fields_table()
        elif page_name == "Crops":
            self.load_crops_table()
            self.load_fields_for_dropdown(self.crop_field_option)
        elif page_name == "Irrigation":
            self.load_irrigation_table()
            self.load_fields_for_dropdown(self.irr_field_option)
        elif page_name == "Fertilizer":
            self.load_fert_table()
            self.load_fields_for_dropdown(self.fert_field_option)
        elif page_name == "Harvest":
            self.load_harvest_table()
            self.load_fields_for_dropdown(self.harv_field_option)
        elif page_name == "Reports":
            self.load_fields_for_dropdown(self.rep_field_option, include_all=True)
        elif page_name == "AI Predictor":
            self.load_ai_forecasts()

        self.pages[page_name].pack(fill="both", expand=True)

    def go_back(self):
        if hasattr(self, 'page_stack') and len(self.page_stack) > 1:
            self.page_stack.pop()
            prev_page = self.page_stack[-1]
            self.show_page(prev_page, save_history=False)
        else:
            self.show_page("Landing")

    def create_landing_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)

        nav = ctk.CTkFrame(page, fg_color="white", height=70, corner_radius=0)
        nav.pack(fill="x", side="top")
        nav.pack_propagate(False)
        
        ctk.CTkLabel(nav, text="🌾 Goviya Pro", font=self.header_font, text_color=self.primary_color).pack(side="left", padx=40)
        
        ctk.CTkButton(nav, text="Login", width=100, height=35, fg_color="transparent", text_color=self.primary_color, hover_color="#EDF2F7", command=lambda: self.show_page("Login")).pack(side="right", padx=10)
        ctk.CTkButton(nav, text="Join Free", width=100, height=35, fg_color=self.primary_color, command=lambda: self.show_page("Register")).pack(side="right", padx=40)

        hero = ctk.CTkFrame(page, fg_color="transparent")
        hero.pack(expand=True, fill="both", padx=80)

        text_f = ctk.CTkFrame(hero, fg_color="transparent")
        text_f.pack(side="left", expand=True, fill="both", pady=80)
        
        ctk.CTkLabel(text_f, text="Cultivate the Future\nWith Rice Precision AI.", font=ctk.CTkFont("Inter", 56, "bold"), text_color=self.primary_color, justify="left").pack(anchor="w")
        ctk.CTkLabel(text_f, text="Digitalize your farm cycles. Monitor growth, track irrigation,\nand optimize yields with Sri Lanka's leading agri-tech suite.", font=self.sub_header_font, text_color=self.text_dim, justify="left").pack(anchor="w", pady=30)
        
        btn_row = ctk.CTkFrame(text_f, fg_color="transparent")
        btn_row.pack(anchor="w")
        ctk.CTkButton(btn_row, text="Launch Dashboard  →", font=self.button_font, height=55, width=280, corner_radius=12, fg_color=self.primary_color, hover_color=self.secondary_color, command=lambda: self.show_page("Register")).pack(side="left")
        ctk.CTkButton(btn_row, text="Watch Demo", font=self.button_font, height=55, width=180, corner_radius=12, fg_color="white", text_color=self.primary_color, border_width=2, border_color=self.primary_color, hover_color="#F1F5F9").pack(side="left", padx=20)

        if self.hero_img:
            img_c = ctk.CTkLabel(hero, image=self.hero_img, text="")
            img_c.pack(side="right", padx=20)
            
        return page

    def create_login_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)

        back_btn = ctk.CTkButton(
            page, text=" ← Back to Home", font=self.normal_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=20, width=140, height=40,
            command=self.go_back
        )
        back_btn.place(x=40, y=30)

        card = ctk.CTkFrame(page, fg_color="white", width=420, height=520, corner_radius=24, border_width=1, border_color="#E2E8F0")
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="Welcome Back", font=self.title_font, text_color=self.primary_color).pack(pady=(45, 10))
        ctk.CTkLabel(card, text="Access your smart farm dashboard", font=self.normal_font, text_color=self.text_dim).pack()
        
        entry_f = ctk.CTkFrame(card, fg_color="transparent")
        entry_f.pack(pady=40)
        
        self.login_mail = ctk.CTkEntry(entry_f, placeholder_text="Email Address", width=340, height=48, corner_radius=12, border_color="#CBD5E0", fg_color="#F8FAFC")
        self.login_mail.pack(pady=10)
        
        self.login_pass = ctk.CTkEntry(entry_f, placeholder_text="Password", show="*", width=340, height=48, corner_radius=12, border_color="#CBD5E0", fg_color="#F8FAFC")
        self.login_pass.pack(pady=10)
        
        ctk.CTkButton(card, text="Sign In to Goviya", font=self.button_font, width=340, height=50, corner_radius=12, fg_color=self.primary_color, hover_color=self.secondary_color, command=lambda: self.handle_auth("login")).pack()
        
        btn_f = ctk.CTkFrame(card, fg_color="transparent")
        btn_f.pack()
        ctk.CTkLabel(btn_f, text="New here?", font=self.small_font).pack(side="left")
        ctk.CTkButton(btn_f, text="Create Account", font=self.small_font, fg_color="transparent", text_color=self.secondary_color, hover=False, command=lambda: self.show_page("Register")).pack(side="left")
        
        return page

    def create_register_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)

        back_btn = ctk.CTkButton(
            page, text=" ← Back", font=self.normal_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=20, width=100, height=40,
            command=self.go_back
        )
        back_btn.place(x=40, y=30)

        card = ctk.CTkFrame(page, fg_color="white", width=440, height=620, corner_radius=24, border_width=1, border_color="#E2E8F0")
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="Get Started", font=self.title_font, text_color=self.primary_color).pack(pady=(40, 5))
        ctk.CTkLabel(card, text="Begin your precision farming journey", font=self.normal_font, text_color=self.text_dim).pack()
        
        entry_f = ctk.CTkFrame(card, fg_color="transparent")
        entry_f.pack(pady=30)

        self.reg_name = ctk.CTkEntry(entry_f, placeholder_text="Full Name", width=340, height=45, corner_radius=10, fg_color="#F8FAFC")
        self.reg_name.pack(pady=6)
        self.reg_mail = ctk.CTkEntry(entry_f, placeholder_text="Email Address", width=340, height=45, corner_radius=10, fg_color="#F8FAFC")
        self.reg_mail.pack(pady=6)
        self.reg_pass = ctk.CTkEntry(entry_f, placeholder_text="Create Password", show="*", width=340, height=45, corner_radius=10, fg_color="#F8FAFC")
        self.reg_pass.pack(pady=6)
        self.reg_conf = ctk.CTkEntry(entry_f, placeholder_text="Confirm Password", show="*", width=340, height=45, corner_radius=10, fg_color="#F8FAFC")
        self.reg_conf.pack(pady=6)
        
        ctk.CTkButton(card, text="Create Professional Account", font=self.button_font, width=340, height=50, corner_radius=12, fg_color=self.secondary_color, hover_color=self.primary_color, command=lambda: self.handle_auth("register")).pack()
        
        btn_f = ctk.CTkFrame(card, fg_color="transparent")
        btn_f.pack()
        ctk.CTkLabel(btn_f, text="Already a member?", font=self.small_font).pack(side="left")
        ctk.CTkButton(btn_f, text="Sign In", font=self.small_font, fg_color="transparent", text_color=self.primary_color, hover=False, command=lambda: self.show_page("Login")).pack(side="left")
        
        return page

    def handle_auth(self, mode):
        if mode == "login":
            self.show_page("Dashboard")
        else:
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_page("Login")

    def create_dashboard_page(self):
        page = ctk.CTkScrollableFrame(self.main_content, fg_color=self.bg_color)

        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkLabel(header, text="Farm Dashboard", font=self.title_font, text_color=self.primary_color).pack(side="left")
        
        date_f = ctk.CTkFrame(header, fg_color="white", corner_radius=12)
        date_f.pack(side="right")
        ctk.CTkLabel(date_f, text=datetime.now().strftime("%A, %d %B %Y"), font=self.normal_font, text_color=self.text_dim, padx=20, pady=10).pack()

        stats_container = ctk.CTkFrame(page, fg_color="transparent")
        stats_container.pack(fill="x", padx=40)
        
        self.dash_stats = {}
        metrics = [
            ("Total Fields", "0", "🌱", "#10B981", "+12% this month"), 
            ("Active Crops", "0", "🌾", "#F59E0B", "Optimal stage"), 
            ("Water Logs", "0", "💧", "#3B82F6", "Scheduled today"), 
            ("AI Yield Est.", "0 kg", "💡", "#3CC47C", "Smart Predictor Active")
        ]
        
        for i, (label, val, icon, color, subtext) in enumerate(metrics):
            card = ctk.CTkFrame(stats_container, fg_color="white", corner_radius=20, border_width=1, border_color="#F1F5F9")
            card.pack(side="left", expand=True, fill="both", padx=(0 if i==0 else 15, 0), ipady=20)
            
            icon_f = ctk.CTkFrame(card, fg_color="#F8FAFC", width=50, height=50, corner_radius=12, border_width=1, border_color=color) # Use themed border instead of alpha
            icon_f.pack(anchor="w", padx=25, pady=(25, 0))
            icon_f.pack_propagate(False)
            ctk.CTkLabel(icon_f, text=icon, font=ctk.CTkFont(size=24), text_color=color).place(relx=0.5, rely=0.5, anchor="center")
            
            ctk.CTkLabel(card, text=label, font=self.normal_font, text_color=self.text_dim).pack(anchor="w", padx=25, pady=(15, 0))
            v_l = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(family="Inter", size=28, weight="bold"), text_color=self.primary_color)
            v_l.pack(anchor="w", padx=25)
            self.dash_stats[label] = v_l
            
            ctk.CTkLabel(card, text=subtext, font=ctk.CTkFont(size=11), text_color=self.success_color if "+" in subtext else self.text_dim).pack(anchor="w", padx=25, pady=(5, 10))

        middle = ctk.CTkFrame(page, fg_color="transparent")
        middle.pack(fill="both", expand=True, padx=40, pady=30)

        actions = ctk.CTkFrame(middle, fg_color="white", corner_radius=20, width=320, border_width=1, border_color="#F1F5F9")
        actions.pack(side="left", fill="y", padx=(0, 25))
        
        ctk.CTkLabel(actions, text="Productivity Tools", font=self.sub_header_font, text_color=self.primary_color).pack(anchor="w", padx=25, pady=(30, 20))
        
        cmds = [("Add New Field", "🌱", lambda: self.show_page("Fields")), ("Log Irrigation", "💧", lambda: self.show_page("Irrigation")), ("Record Harvest", "📈", lambda: self.show_page("Harvest"))]
        for txt, icn, cmd in cmds:
            btn = ctk.CTkButton(
                actions, text=f"  {icn}  {txt}", 
                font=self.normal_font, 
                fg_color="#F8FAFC", # Light slate
                text_color=self.text_main, 
                hover_color="#F1F5F9", 
                height=50, 
                corner_radius=12,
                anchor="w",
                command=cmd
            )
            btn.pack(fill="x", padx=20, pady=6)
        
        ctk.CTkFrame(actions, fg_color="#F1F5F9", height=1).pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(actions, text="Tips: Check analytics to optimize fertilizer usage for better yields.", font=self.small_font, text_color=self.text_dim, wraplength=250).pack(padx=20)

        recent = ctk.CTkFrame(middle, fg_color="white", corner_radius=20, border_width=1, border_color="#F1F5F9")
        recent.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(recent, text="Market Performance Insights", font=self.sub_header_font, text_color=self.primary_color).pack(anchor="w", padx=25, pady=(30, 20))

        chart_f = ctk.CTkFrame(recent, fg_color="#F8FBFA", corner_radius=16, border_width=2, border_color="#E2E8F0")
        chart_f.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        ctk.CTkLabel(chart_f, text="✨ Analytics Visualizations Enhanced", font=self.button_font, text_color=self.secondary_color).place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(chart_f, text="Connect more data points to see AI predictions", font=self.small_font, text_color=self.text_dim).place(relx=0.5, rely=0.55, anchor="center")

        return page

    def create_fields_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)
        
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        back_btn = ctk.CTkButton(
            header, text="←", font=self.header_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=8, width=40, height=40,
            command=lambda: self.show_page("Dashboard")
        )
        back_btn.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(header, text="Field Management", font=self.title_font, text_color=self.primary_color).pack(side="left")
 
        search_f = ctk.CTkFrame(header, fg_color="white", height=40, corner_radius=20)
        search_f.pack(side="left", padx=30, fill="x", expand=True)
        search_f.pack_propagate(False)
        
        search_icon = ctk.CTkLabel(search_f, text=" 🔍", font=self.normal_font, text_color=self.text_dim)
        search_icon.pack(side="left", padx=(10, 5))
        
        self.field_search = ctk.CTkEntry(search_f, placeholder_text="Search fields by name or location...", border_width=0, fg_color="transparent", font=self.normal_font)
        self.field_search.pack(side="left", fill="both", expand=True, padx=5)
        self.field_search.bind("<KeyRelease>", lambda e: self.load_fields_table(self.field_search.get()))

        ctk.CTkButton(header, text="+ Add New Field", font=self.sub_header_font, fg_color=self.secondary_color, corner_radius=8, width=180, height=40, command=self.add_field_popup).pack(side="right")

        # Optimized Table Container
        container = ctk.CTkFrame(page, fg_color="white", corner_radius=20, border_width=1, border_color="#E2E8F0")
        container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Fixed Headers
        headers_f = ctk.CTkFrame(container, fg_color="#F8FAFC", height=32, corner_radius=0)
        headers_f.pack(fill="x")
        
        cols = [("#", 60), ("Information", 450), ("Acreage", 150), ("Actions", 150)]
        for text, width in cols:
            lbl = ctk.CTkLabel(headers_f, text=text.upper(), font=ctk.CTkFont(size=9, weight="bold"), text_color=self.text_dim, width=width, anchor="w" if text != "#" else "center")
            lbl.pack(side="left", padx=15)

        self.fields_table = ctk.CTkScrollableFrame(container, fg_color="transparent")
        self.fields_table.pack(fill="both", expand=True, padx=5, pady=5)
        
        return page

    def create_crops_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)

        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 0))
        
        back_btn = ctk.CTkButton(
            header, text="←", font=self.header_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=8, width=40, height=40,
            command=lambda: self.show_page("Dashboard")
        )
        back_btn.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(header, text="Crop Registry", font=self.title_font, text_color=self.primary_color).pack(side="left")

        form_f = ctk.CTkFrame(page, fg_color="white", width=350, corner_radius=16)
        form_f.pack(side="left", fill="y", padx=(40, 20), pady=40)
        form_f.pack_propagate(False)
        
        ctk.CTkLabel(form_f, text="Register New Crop", font=self.header_font, text_color=self.primary_color).pack(pady=30)
        
        ctk.CTkLabel(form_f, text="Link to Field", font=self.small_font, text_color=self.text_dim).pack(anchor="w", padx=25)
        self.crop_field_option = ctk.CTkOptionMenu(form_f, values=["No fields"], width=300, height=38, fg_color="#F7FAFC", text_color="black")
        self.crop_field_option.pack(pady=(5, 15))
        
        ctk.CTkLabel(form_f, text="Rice Variety", font=self.small_font, text_color=self.text_dim).pack(anchor="w", padx=25)
        self.crop_variety = ctk.CTkComboBox(form_f, values=["Nadu", "Samba", "Keeri Samba", "Red Nadu", "Red Samba", "Sudu Samba", "Suwandel"], width=300, height=38)
        self.crop_variety.pack(pady=(5, 15))
        
        ctk.CTkLabel(form_f, text="Planting Date", font=self.small_font, text_color=self.text_dim).pack(anchor="w", padx=25)
        date_container = ctk.CTkFrame(form_f, fg_color="transparent")
        date_container.pack(fill="x", padx=25, pady=(5, 15))
        
        self.crop_date = ctk.CTkEntry(date_container, placeholder_text="DD/MM/YYYY", width=220, height=38)
        self.crop_date.pack(side="left")
        ctk.CTkButton(date_container, text="📅", width=70, height=38, fg_color="#E2E8F0", text_color="black", hover_color="#CBD5E0", command=lambda: self.pick_date(self.crop_date)).pack(side="right")
        
        ctk.CTkLabel(form_f, text="Initial Stage", font=self.small_font, text_color=self.text_dim).pack(anchor="w", padx=25)
        self.crop_stage = ctk.CTkOptionMenu(form_f, values=["Seedling", "Vegetative", "Ripening"], width=300, height=38)
        self.crop_stage.pack(pady=(5, 30))
        
        ctk.CTkButton(form_f, text="Register Crop", font=self.sub_header_font, height=45, width=300, fg_color=self.secondary_color, command=self.save_crop).pack()

        list_f = ctk.CTkFrame(page, fg_color="white", corner_radius=16)
        list_f.pack(side="left", fill="both", expand=True, padx=(0, 40), pady=40)

        search_f = ctk.CTkFrame(list_f, fg_color="#F8F9FA", height=35, corner_radius=8)
        search_f.pack(fill="x", padx=25, pady=(0, 10))
        
        self.crop_search = ctk.CTkEntry(search_f, placeholder_text="Search crops by variety or field...", border_width=0, fg_color="transparent", font=self.small_font)
        self.crop_search.pack(fill="both", expand=True, padx=10)
        self.crop_search.bind("<KeyRelease>", lambda e: self.load_crops_table(self.crop_search.get()))

        self.crops_list = ctk.CTkScrollableFrame(list_f, fg_color="transparent")
        self.crops_list.pack(fill="both", expand=True, padx=10, pady=10)

        return page

    def create_irrigation_page(self):
        page = self.create_module_base("Irrigation Management", "💧")
        self.irr_field_option = self.module_field_option
        self.irr_table = self.module_table

        ctk.CTkLabel(self.module_form, text="Water Quantity (L)", font=self.small_font).pack(anchor="w", padx=25)
        self.irr_qty = ctk.CTkEntry(self.module_form, width=300, height=38)
        self.irr_qty.pack(pady=(5, 15))
        
        ctk.CTkLabel(self.module_form, text="Notes", font=self.small_font).pack(anchor="w", padx=25)
        self.irr_notes = ctk.CTkEntry(self.module_form, width=300, height=38)
        self.irr_notes.pack(pady=(5, 20))
        
        ctk.CTkButton(self.module_form, text="Log Irrigation", font=self.sub_header_font, height=45, fg_color=self.secondary_color, command=self.save_irrigation).pack(fill="x", padx=25)
        
        return page

    def create_fertilizer_page(self):
        page = self.create_module_base("Fertilizer Tracker", "🧪")
        self.fert_field_option = self.module_field_option
        self.fert_table = self.module_table
        
        ctk.CTkLabel(self.module_form, text="Fertilizer Type", font=self.small_font).pack(anchor="w", padx=25)
        self.fert_type = ctk.CTkComboBox(self.module_form, values=["Urea", "TSP", "MOP", "NPK Mix", "Compost", "Cow dung", "Poultry Manure", "Green Manure", "Liquid Fertilizer", "Bio Fertilizer"], width=300, height=38)
        self.fert_type.pack(pady=(5, 15))
        
        ctk.CTkLabel(self.module_form, text="Quantity (kg)", font=self.small_font).pack(anchor="w", padx=25)
        self.fert_qty = ctk.CTkEntry(self.module_form, width=300, height=38)
        self.fert_qty.pack(pady=(5, 20))
        
        ctk.CTkButton(self.module_form, text="Apply Fertilizer", font=self.sub_header_font, height=45, fg_color=self.secondary_color, command=self.save_fert).pack(fill="x", padx=25)
        
        return page

    def create_harvest_page(self):
        page = self.create_module_base("Harvest Yields", "📈")
        self.harv_field_option = self.module_field_option
        self.harv_table = self.module_table
        
        ctk.CTkLabel(self.module_form, text="Yield Weight (kg)", font=self.small_font).pack(anchor="w", padx=25)
        self.harv_yield = ctk.CTkEntry(self.module_form, width=300, height=38)
        self.harv_yield.pack(pady=(5, 15))
        
        ctk.CTkLabel(self.module_form, text="Profit Estimation (Rs.)", font=self.small_font).pack(anchor="w", padx=25)
        self.harv_profit = ctk.CTkEntry(self.module_form, width=300, height=38)
        self.harv_profit.pack(pady=(5, 20))
        
        ctk.CTkButton(self.module_form, text="Record Harvest", font=self.sub_header_font, height=45, fg_color=self.secondary_color, command=self.save_harvest).pack(fill="x", padx=25)
        
        return page

    def create_module_base(self, title, icon):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)
        
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        back_btn = ctk.CTkButton(
            header, text="←", font=self.header_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=8, width=40, height=40,
            command=lambda: self.show_page("Dashboard")
        )
        back_btn.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(header, text=f"{icon} {title}", font=self.title_font, text_color=self.primary_color).pack(side="left")

        search_f = ctk.CTkFrame(header, fg_color="white", height=40, corner_radius=20)
        search_f.pack(side="right", padx=20, fill="x", expand=True)
        search_f.pack_propagate(False)
        
        search_box = ctk.CTkEntry(search_f, placeholder_text=f"Filter {title} records...", border_width=0, fg_color="transparent", font=self.normal_font)
        search_box.pack(side="left", fill="both", expand=True, padx=15)

        if "Irrigation" in title:
            search_box.bind("<KeyRelease>", lambda e: self.load_irrigation_table(search_box.get()))
        elif "Fertilizer" in title:
            search_box.bind("<KeyRelease>", lambda e: self.load_fert_table(search_box.get()))
        elif "Harvest" in title:
            search_box.bind("<KeyRelease>", lambda e: self.load_harvest_table(search_box.get()))

        self.module_table_container = ctk.CTkFrame(page, fg_color="white", corner_radius=20, border_width=1, border_color="#E2E8F0")
        self.module_table_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        # Fixed Headers for Modules
        headers_m = ctk.CTkFrame(self.module_table_container, fg_color="#F8FAFC", height=32, corner_radius=0)
        headers_m.pack(fill="x")
        
        m_cols = [("Field Name", 300), ("Metric", 200), ("Date/Summary", 250), ("Action", 120)]
        for text, width in m_cols:
            ctk.CTkLabel(headers_m, text=text.upper(), font=ctk.CTkFont(size=9, weight="bold"), text_color=self.text_dim, width=width, anchor="w").pack(side="left", padx=15)

        self.module_table = ctk.CTkScrollableFrame(self.module_table_container, fg_color="transparent")
        self.module_table.pack(fill="both", expand=True, padx=5, pady=5)

        # Form Section (at Bottom)
        self.module_form = ctk.CTkFrame(page, fg_color="white", height=200, corner_radius=20, border_width=1, border_color="#E2E8F0")
        self.module_form.pack(fill="x", padx=40, pady=(0, 40))
        
        form_row = ctk.CTkFrame(self.module_form, fg_color="transparent")
        form_row.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(form_row, text=f"Log {title}", font=self.header_font, text_color=self.primary_color).pack(side="left")
        
        f_select = ctk.CTkFrame(form_row, fg_color="transparent")
        f_select.pack(side="right")
        ctk.CTkLabel(f_select, text="Target Field", font=self.small_font, text_color=self.text_dim).pack(side="left", padx=10)
        self.module_field_option = ctk.CTkOptionMenu(f_select, values=["Loading..."], width=200)
        self.module_field_option.pack(side="left")

        return page

    def pick_date(self, target_widget):
        popup = ctk.CTkToplevel(self)
        popup.title("Select Date")
        popup.geometry("350x400")
        popup.attributes("-topmost", True)
        popup.grab_set() 
        
        cal = Calendar(popup, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20, padx=20, fill="both", expand=True)
        
        def set_date():
            target_widget.delete(0, 'end')
            target_widget.insert(0, cal.get_date())
            popup.destroy()
            
        ctk.CTkButton(popup, text="Confirm", command=set_date, fg_color=self.secondary_color).pack(pady=10)

    def add_field_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("New Field")
        popup.geometry("450x500")
        popup.attributes("-topmost", True)
        
        ctk.CTkLabel(popup, text="Add Field Detail", font=self.header_font, text_color=self.primary_color).pack(pady=30)
        
        name_e = ctk.CTkEntry(popup, placeholder_text="Field Name (e.g. North Plain)", width=350, height=40)
        name_e.pack(pady=10)
        loc_e = ctk.CTkEntry(popup, placeholder_text="Location (e.g. Village A)", width=350, height=40)
        loc_e.pack(pady=10)
        size_e = ctk.CTkEntry(popup, placeholder_text="Size in Acres", width=350, height=40)
        size_e.pack(pady=10)
        
        def save():
            n, l, s = name_e.get(), loc_e.get(), size_e.get()
            if not n or not l or not s: return
            try:
                self.cursor.execute("INSERT INTO fields (name, location, size) VALUES (?, ?, ?)", (n, l, float(s)))
                self.conn.commit()
                popup.destroy()
                self.load_fields_table()
            except: messagebox.showerror("Error", "Check numeric values")

        ctk.CTkButton(popup, text="Save Field", height=45, width=350, fg_color=self.secondary_color, command=save).pack(pady=30)


    def create_ai_predictor_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)
        
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        back_btn = ctk.CTkButton(
            header, text="←", font=self.header_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=8, width=40, height=40,
            command=lambda: self.show_page("Dashboard")
        )
        back_btn.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(header, text="💡 Goviya AI Yield Predictor", font=self.title_font, text_color=self.primary_color).pack(side="left")

        # Layout
        container = ctk.CTkFrame(page, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Left Panel: Intelligence Insights
        left = ctk.CTkFrame(container, fg_color="white", width=400, corner_radius=24, border_width=1, border_color="#E2E8F0")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left, text="Intelligence Summary", font=self.header_font, text_color=self.primary_color).pack(pady=(30, 10), padx=30, anchor="w")
        ctk.CTkLabel(left, text="Using historical averages and variety factors.", font=self.normal_font, text_color=self.text_dim).pack(padx=30, anchor="w")
        
        self.ai_summary_f = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.ai_summary_f.pack(fill="both", expand=True, padx=20, pady=20)

        # Right Panel: Confidence Chart (Mock)
        right = ctk.CTkFrame(container, fg_color="#F8FBFA", corner_radius=24, border_width=2, border_color="#E2E8F0")
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        # Center Mock visualization
        viz_f = ctk.CTkFrame(right, fg_color="white", width=250, height=250, corner_radius=125)
        viz_f.place(relx=0.5, rely=0.45, anchor="center")
        self.ai_conf_label = ctk.CTkLabel(viz_f, text="--%", font=ctk.CTkFont("Inter", 64, "bold"), text_color=self.accent_color)
        self.ai_conf_label.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(right, text="Prediction Confidence Score", font=self.button_font, text_color=self.primary_color).place(relx=0.5, rely=0.7, anchor="center")
        ctk.CTkLabel(right, text="Based on data consistency and historical variance", font=self.small_font, text_color=self.text_dim).place(relx=0.5, rely=0.75, anchor="center")

        return page

    def load_ai_forecasts(self):
        for w in self.ai_summary_f.winfo_children(): w.destroy()
        
        # Logic: Predict for all active crops
        self.cursor.execute("SELECT crops.id, fields.id, fields.name, crops.variety FROM crops LEFT JOIN fields ON crops.field_id = fields.id")
        active_crops = self.cursor.fetchall()
        
        total_predicted = 0
        
        variety_factors = {
            "Nadu": 1.0, "Samba": 0.95, "Keeri Samba": 0.85, 
            "Red Nadu": 1.05, "Red Samba": 0.98, "Sudu Samba": 0.92, "Suwandel": 0.75
        }

        for c_id, f_id, f_name, variety in active_crops:
            # Get Field Average
            self.cursor.execute("SELECT AVG(yield) FROM harvests WHERE field_id=?", (f_id,))
            avg_res = self.cursor.fetchone()[0]
            avg_yield = avg_res if avg_res else 500 # Default baseline
            
            prediction = round(avg_yield * variety_factors.get(variety, 1.0), 2)
            total_predicted += prediction
            
            # Show in UI
            item = ctk.CTkFrame(self.ai_summary_f, fg_color="#F8FAFC", height=90, corner_radius=16)
            item.pack(fill="x", pady=6, padx=10)
            
            ctk.CTkLabel(item, text=f"Field: {f_name}", font=self.button_font, text_color=self.text_main).pack(side="left", padx=20)
            ctk.CTkLabel(item, text=f"Variety: {variety}", font=self.small_font, text_color=self.text_dim).pack(side="left")
            
            pred_f = ctk.CTkFrame(item, fg_color="white", width=140, height=50, corner_radius=12, border_width=1, border_color=self.accent_color)
            pred_f.pack(side="right", padx=20)
            pred_f.pack_propagate(False)
            ctk.CTkLabel(pred_f, text=f"{prediction} kg", font=self.button_font, text_color=self.primary_color).place(relx=0.5, rely=0.45, anchor="center")
            ctk.CTkLabel(pred_f, text="AI Est. Yield", font=ctk.CTkFont(size=9), text_color=self.text_dim).place(relx=0.5, rely=0.75, anchor="center")

        # Update Dashboard Metric too
        if hasattr(self, 'dash_stats') and "AI Yield Est." in self.dash_stats:
            self.dash_stats["AI Yield Est."].configure(text= f"{round(total_predicted, 1)} kg")
            
        # Dynamic Confidence Score based on data volume
        self.cursor.execute("SELECT COUNT(*) FROM harvests")
        h_count = self.cursor.fetchone()[0]
        # Start at 55% baseline, +3% per record, max 98%
        conf = min(55 + (h_count * 3), 98)
        if hasattr(self, 'ai_conf_label'):
            self.ai_conf_label.configure(text=f"{conf}%")

    def refresh_dashboard_stats(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM fields")
            f_count = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(*) FROM crops")
            c_count = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(*) FROM water_schedules")
            w_count = self.cursor.fetchone()[0]
            
            self.dash_stats["Total Fields"].configure(text=str(f_count))
            self.dash_stats["Active Crops"].configure(text=str(c_count))
            self.dash_stats["Water Logs"].configure(text=str(w_count))
            
            self.load_ai_forecasts()
        except Exception as e:
            print(f"Stats refresh error: {e}")

    def load_fields_for_dropdown(self, widget, include_all=False):
        self.cursor.execute("SELECT id, name FROM fields")
        rows = self.cursor.fetchall()
        options = [f"{r[0]} - {r[1]}" for r in rows]
        if include_all:
            options = ["All Fields"] + options
        if not options:
            options = ["No fields"]
        widget.configure(values=options)
        widget.set(options[0])

    def load_fields_table(self, query=""):
        for w in self.fields_table.winfo_children(): w.destroy()
        if query:
            self.cursor.execute("SELECT * FROM fields WHERE name LIKE ? OR location LIKE ?", (f"%{query}%", f"%{query}%"))
        else:
            self.cursor.execute("SELECT * FROM fields")
        
        for i, r in enumerate(self.cursor.fetchall()):
            bg = "white" if i % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(self.fields_table, fg_color=bg, height=30, corner_radius=0)
            row.pack(fill="x")
            
            # Link ID column
            ctk.CTkLabel(row, text=str(r[0]), font=self.small_font, text_color=self.secondary_color, width=60).pack(side="left", padx=15)
            
            # Field Info column
            info_f = ctk.CTkFrame(row, fg_color="transparent", width=450)
            info_f.pack(side="left", padx=15)
            info_f.pack_propagate(False)
            
            lbl = ctk.CTkLabel(info_f, text=f"{r[1]}", font=self.small_font, text_color=self.text_main, anchor="w")
            lbl.pack(side="left")
            ctk.CTkLabel(info_f, text=f"  •  {r[2]}", font=ctk.CTkFont(size=10), text_color=self.text_dim, anchor="w").pack(side="left")
            
            # Acreage column
            ctk.CTkLabel(row, text=f"{r[3]} ac", font=self.small_font, text_color=self.primary_color, width=150, anchor="w").pack(side="left", padx=15)
            
            # Actions column
            act_f = ctk.CTkFrame(row, fg_color="transparent", width=150)
            act_f.pack(side="left", padx=15)
            act_f.pack_propagate(False)
            ctk.CTkButton(act_f, text="🗑 Delete", width=65, height=22, fg_color="#FEF2F2", text_color="#EF4444", hover_color="#FEE2E2", corner_radius=4, font=ctk.CTkFont(size=9), command=lambda id=r[0]: self.delete_record("fields", id, self.load_fields_table)).pack(side="left", pady=4)

    def load_crops_table(self, query=""):
        for w in self.crops_list.winfo_children(): w.destroy()
        sql = "SELECT crops.id, fields.name, crops.variety, crops.stage FROM crops LEFT JOIN fields ON crops.field_id = fields.id"
        if query:
            sql += f" WHERE variety LIKE '%{query}%' OR fields.name LIKE '%{query}%'"
            
        self.cursor.execute(sql)
        for r in self.cursor.fetchall():
            card = ctk.CTkFrame(self.crops_list, fg_color="white", height=80, corner_radius=16, border_width=1, border_color="#F1F5F9")
            card.pack(fill="x", pady=6, padx=10)
            
            icon_f = ctk.CTkFrame(card, fg_color="#F0FDF4", width=50, height=50, corner_radius=12)
            icon_f.pack(side="left", padx=15)
            icon_f.pack_propagate(False)
            ctk.CTkLabel(icon_f, text="🌾", font=ctk.CTkFont(size=20)).place(relx=0.5, rely=0.5, anchor="center")
            
            details = ctk.CTkFrame(card, fg_color="transparent")
            details.pack(side="left", fill="both", expand=True, padx=5)
            ctk.CTkLabel(details, text=f"{r[2]}", font=self.button_font, text_color=self.text_main, anchor="w").pack(side="top", pady=(15, 0), fill="x")
            ctk.CTkLabel(details, text=f"at {r[1]} field", font=self.small_font, text_color=self.text_dim, anchor="w").pack(side="top", fill="x")
            
            stage_colors = {"Seedling": self.success_color, "Vegetative": self.warning_color, "Ripening": self.danger_color}
            color = stage_colors.get(r[3], self.text_dim)
            
            badge = ctk.CTkFrame(card, fg_color="#FDFDFD", width=120, height=32, corner_radius=8, border_width=1, border_color=color)
            badge.pack(side="right", padx=20)
            badge.pack_propagate(False)
            ctk.CTkLabel(badge, text=r[3], font=ctk.CTkFont(size=12, weight="bold"), text_color=color).place(relx=0.5, rely=0.5, anchor="center")

    def load_irrigation_table(self, query=""):
        for w in self.irr_table.winfo_children(): w.destroy()
        sql = "SELECT water_schedules.id, fields.name, quantity, date FROM water_schedules LEFT JOIN fields ON field_id = fields.id"
        if query:
            sql += f" WHERE fields.name LIKE '%{query}%' OR quantity LIKE '%{query}%' OR date LIKE '%{query}%'"
        
        self.cursor.execute(sql)
        for i, r in enumerate(self.cursor.fetchall()):
            bg = "white" if i % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(self.irr_table, fg_color=bg, height=30, corner_radius=0)
            row.pack(fill="x")
            
            ctk.CTkLabel(row, text=r[1], font=self.small_font, width=300, anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row, text=f"{r[2]} L", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#3B82F6", width=200, anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row, text=r[3], font=ctk.CTkFont(size=11), text_color=self.text_dim, width=250, anchor="w").pack(side="left", padx=15)
            
            ctk.CTkButton(row, text="🗑", width=28, height=20, fg_color="#FEF2F2", text_color="#EF4444", font=ctk.CTkFont(size=8), command=lambda id=r[0]: self.delete_record("water_schedules", id, self.load_irrigation_table)).pack(side="left", padx=15)

    def load_fert_table(self, query=""):
        for w in self.fert_table.winfo_children(): w.destroy()
        sql = "SELECT fertilizers.id, fields.name, type, quantity FROM fertilizers LEFT JOIN fields ON field_id = fields.id"
        if query:
            sql += f" WHERE fields.name LIKE '%{query}%' OR type LIKE '%{query}%'"
            
        self.cursor.execute(sql)
        for i, r in enumerate(self.cursor.fetchall()):
            bg = "white" if i % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(self.fert_table, fg_color=bg, height=30, corner_radius=0)
            row.pack(fill="x")
            
            ctk.CTkLabel(row, text=r[1], font=self.small_font, width=300, anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row, text=f"{r[2]} ({r[3]}kg)", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#8B5CF6", width=200, anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row, text="Nutrient", font=ctk.CTkFont(size=11), text_color=self.text_dim, width=250, anchor="w").pack(side="left", padx=15)
            
            ctk.CTkButton(row, text="🗑", width=28, height=20, fg_color="#FEF2F2", text_color="#EF4444", font=ctk.CTkFont(size=8), command=lambda id=r[0]: self.delete_record("fertilizers", id, self.load_fert_table)).pack(side="left", padx=15)

    def load_harvest_table(self, query=""):
        for w in self.harv_table.winfo_children(): w.destroy()
        sql = "SELECT harvests.id, fields.name, yield, profit FROM harvests LEFT JOIN fields ON field_id = fields.id"
        if query:
            sql += f" WHERE fields.name LIKE '%{query}%' OR yield LIKE '%{query}%'"
            
        self.cursor.execute(sql)
        for i, r in enumerate(self.cursor.fetchall()):
            bg = "white" if i % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(self.harv_table, fg_color=bg, height=30, corner_radius=0)
            row.pack(fill="x")
            
            ctk.CTkLabel(row, text=r[1], font=self.small_font, width=300, anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row, text=f"{r[2]} kg", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color=self.success_color, width=200, anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row, text=f"Rs. {r[3]}", font=ctk.CTkFont(size=11), text_color=self.text_dim, width=250, anchor="w").pack(side="left", padx=15)
            
            ctk.CTkButton(row, text="🗑", width=28, height=20, fg_color="#FEF2F2", text_color="#EF4444", font=ctk.CTkFont(size=8), command=lambda id=r[0]: self.delete_record("harvests", id, self.load_harvest_table)).pack(side="left", padx=15)

    def save_crop(self):
        f_str = self.crop_field_option.get()
        if f_str == "No fields": return
        fid = f_str.split(" - ")[0]
        self.cursor.execute("INSERT INTO crops (field_id, variety, planting_date, stage) VALUES (?, ?, ?, ?)", (fid, self.crop_variety.get(), self.crop_date.get(), self.crop_stage.get()))
        self.conn.commit()
        self.load_crops_table()

    def save_irrigation(self):
        f_str = self.irr_field_option.get()
        if f_str == "No fields": return
        fid = f_str.split(" - ")[0]
        self.cursor.execute("INSERT INTO water_schedules (field_id, quantity, date) VALUES (?, ?, ?)", (fid, self.irr_qty.get(), datetime.now().strftime("%d/%m/%Y")))
        self.conn.commit()
        self.load_irrigation_table()

    def save_fert(self):
        f_str = self.fert_field_option.get()
        if f_str == "No fields": return
        fid = f_str.split(" - ")[0]
        self.cursor.execute("INSERT INTO fertilizers (field_id, type, quantity, date) VALUES (?, ?, ?, ?)", (fid, self.fert_type.get(), self.fert_qty.get(), datetime.now().strftime("%d/%m/%Y")))
        self.conn.commit()
        self.load_fert_table()

    def save_harvest(self):
        f_str = self.harv_field_option.get()
        if f_str == "No fields": return
        fid = f_str.split(" - ")[0]
        self.cursor.execute("INSERT INTO harvests (field_id, yield, profit, date) VALUES (?, ?, ?, ?)", (fid, self.harv_yield.get(), self.harv_profit.get(), datetime.now().strftime("%d/%m/%Y")))
        self.conn.commit()
        self.load_harvest_table()

    def delete_record(self, table, id, callback):
        if messagebox.askyesno("Confirm", "Delete this record?"):
            self.cursor.execute(f"DELETE FROM {table} WHERE id=?", (id,))
            self.conn.commit()
            callback()

    def create_reports_page(self):
        page = ctk.CTkFrame(self.main_content, fg_color=self.bg_color)

        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        back_btn = ctk.CTkButton(
            header, text="←", font=self.header_font, 
            fg_color="white", text_color=self.primary_color, 
            hover_color="#EDF2F7", corner_radius=8, width=40, height=40,
            command=lambda: self.show_page("Dashboard")
        )
        back_btn.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(header, text="📊 Reports & Analytics", font=self.title_font, text_color=self.primary_color).pack(side="left")

        controls = ctk.CTkFrame(page, fg_color="white", corner_radius=16)
        controls.pack(fill="x", padx=40, pady=(0, 20))

        row1 = ctk.CTkFrame(controls, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=20)

        f1 = ctk.CTkFrame(row1, fg_color="transparent")
        f1.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(f1, text="Report Type", font=self.small_font).pack(anchor="w")
        self.rep_type = ctk.CTkOptionMenu(f1, values=["Yield Overview", "Water Usage", "Fertilizer Usage", "Profit Analysis"], width=200)
        self.rep_type.pack(pady=5, anchor="w")

        f2 = ctk.CTkFrame(row1, fg_color="transparent")
        f2.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(f2, text="Select Field", font=self.small_font).pack(anchor="w")
        self.rep_field_option = ctk.CTkOptionMenu(f2, values=["All Fields"], width=200)
        self.rep_field_option.pack(pady=5, anchor="w")

        f3 = ctk.CTkFrame(row1, fg_color="transparent")
        f3.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(f3, text="Start Date", font=self.small_font).pack(anchor="w")
        d_f1 = ctk.CTkFrame(f3, fg_color="transparent")
        d_f1.pack(anchor="w")
        self.rep_start = ctk.CTkEntry(d_f1, width=120, placeholder_text="DD/MM/YYYY")
        self.rep_start.pack(side="left")
        ctk.CTkButton(d_f1, text="📅", width=40, font=("Inter", 12), command=lambda: self.pick_date(self.rep_start)).pack(side="left", padx=5)

        f4 = ctk.CTkFrame(row1, fg_color="transparent")
        f4.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(f4, text="End Date", font=self.small_font).pack(anchor="w")
        d_f2 = ctk.CTkFrame(f4, fg_color="transparent")
        d_f2.pack(anchor="w")
        self.rep_end = ctk.CTkEntry(d_f2, width=120, placeholder_text="DD/MM/YYYY")
        self.rep_end.pack(side="left")
        ctk.CTkButton(d_f2, text="📅", width=40, font=("Inter", 12), command=lambda: self.pick_date(self.rep_end)).pack(side="left", padx=5)

        ctk.CTkButton(controls, text="📊 Generate Report", font=self.sub_header_font, width=200, height=45, fg_color=self.secondary_color, command=self.generate_report).pack(pady=(0, 20))

        self.viz_container = ctk.CTkFrame(page, fg_color="white", corner_radius=16)
        self.viz_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        self.viz_label = ctk.CTkLabel(self.viz_container, text="Configure filters and click Generate to view report", font=self.normal_font, text_color=self.text_dim)
        self.viz_label.place(relx=0.5, rely=0.5, anchor="center")

        export_f = ctk.CTkFrame(page, fg_color="transparent")
        export_f.pack(fill="x", padx=40, pady=(0, 20))
        ctk.CTkButton(export_f, text="📄 Export as PDF", width=150, fg_color="#718096").pack(side="right", padx=10)
        ctk.CTkButton(export_f, text="Excel", width=100, fg_color="#718096").pack(side="right")

        return page

    def generate_report(self):
        for widget in self.viz_container.winfo_children():
            widget.destroy()
            
        rtype = self.rep_type.get()

        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')
        
        try:
            if rtype == "Yield Overview":
                self.cursor.execute("SELECT fields.name, SUM(yield) FROM harvests LEFT JOIN fields ON field_id = fields.id GROUP BY fields.id")
                result = self.cursor.fetchall()
                if result:
                    names, yields = zip(*result)
                    ax.bar(names, yields, color=self.secondary_color)
                    ax.set_title("Total Yield by Field (kg)")
                    ax.set_ylabel("kg")
                else: ax.text(0.5, 0.5, "No data available", ha='center')
                
            elif rtype == "Profit Analysis":
                self.cursor.execute("SELECT fields.name, SUM(profit) FROM harvests LEFT JOIN fields ON field_id = fields.id GROUP BY fields.id")
                result = self.cursor.fetchall()
                if result:
                    names, profits = zip(*result)
                    ax.pie(profits, labels=names, autopct='%1.1f%%', colors=[self.primary_color, self.secondary_color, self.accent_color, self.success_color])
                    ax.set_title("Profit Analysis by Field")
                else: ax.text(0.5, 0.5, "No data available", ha='center')
                
            elif rtype == "Water Usage":
                self.cursor.execute("SELECT fields.name, SUM(quantity) FROM water_schedules LEFT JOIN fields ON field_id = fields.id GROUP BY fields.id")
                result = self.cursor.fetchall()
                if result:
                    names, qty = zip(*result)
                    ax.barh(names, qty, color="#3B82F6")
                    ax.set_title("Water Usage by Field (L)")
                    ax.set_xlabel("Liters")
                else: ax.text(0.5, 0.5, "No data available", ha='center')
            
            elif rtype == "Fertilizer Usage":
                self.cursor.execute("SELECT type, SUM(quantity) FROM fertilizers GROUP BY type")
                result = self.cursor.fetchall()
                if result:
                    types, sums = zip(*result)
                    ax.bar(types, sums, color="#8B5CF6")
                    ax.set_title("Fertilizer Consumption by Type")
                else: ax.text(0.5, 0.5, "No data available", ha='center')
        except Exception as e:
            ax.text(0.5, 0.5, f"Error generating chart: {str(e)}", ha='center')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.viz_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = SmartRiceFarmingApp()
    app.mainloop()
