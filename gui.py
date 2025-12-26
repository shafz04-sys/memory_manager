import customtkinter as ctk
import tkinter as tk
import hashlib
from memory_managers import ContiguousManager, PagingManager

# --- THEME SETUP ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class OSSuite(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OS Simulator: Virtual Memory & Paging")
        self.geometry("1200x850")

        # --- TABS LAYOUT ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab1 = self.tab_view.add("Older OS (Contiguous)")
        self.tab2 = self.tab_view.add("Modern OS (Paging)")

        # Initialize Logic Engines
        self.cont_mgr = ContiguousManager()
        self.cont_mgr.log_func = self.log_tab1
        
        self.page_mgr = PagingManager()
        self.page_mgr.log_func = self.log_tab2

        # Setup UI for both tabs
        self.setup_tab1()
        self.setup_tab2()

    # ========================================================
    #  TAB 1: CONTIGUOUS MEMORY (Variable Partition + Swap)
    # ========================================================
    def setup_tab1(self):
        # 1. Left Sidebar (Controls)
        frame_ctrl = ctk.CTkFrame(self.tab1, width=280)
        frame_ctrl.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(frame_ctrl, text="CONTROLS", font=("Arial", 18, "bold")).pack(pady=15)
        
        # Input Fields
        self.t1_pid = ctk.CTkEntry(frame_ctrl, placeholder_text="PID (e.g. P1)")
        self.t1_pid.pack(pady=5, padx=10)
        
        self.t1_size = ctk.CTkEntry(frame_ctrl, placeholder_text="Size (KB)")
        self.t1_size.pack(pady=5, padx=10)
        
        self.t1_algo = ctk.CTkOptionMenu(frame_ctrl, values=["First Fit", "Best Fit", "Worst Fit"])
        self.t1_algo.pack(pady=5, padx=10)
        
        # Allocate Button
        ctk.CTkButton(frame_ctrl, text="⚡ Allocate Process", fg_color="#2CC985", text_color="black", 
                      command=self.t1_alloc).pack(pady=15, padx=10)
        
        # Deallocate Section
        ctk.CTkFrame(frame_ctrl, height=2, fg_color="grey").pack(fill="x", padx=10, pady=10)
        self.t1_kill = ctk.CTkEntry(frame_ctrl, placeholder_text="PID to Kill")
        self.t1_kill.pack(pady=5, padx=10)
        ctk.CTkButton(frame_ctrl, text="💀 Kill Process", fg_color="#FF474C", 
                      command=self.t1_dealloc).pack(pady=5, padx=10)
        
        # Compaction Section
        ctk.CTkFrame(frame_ctrl, height=2, fg_color="grey").pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(frame_ctrl, text="⚙️ Run Compaction", fg_color="#3B8ED0", 
                      command=self.t1_compact).pack(pady=10, padx=10)

        # 2. Right Side (Visualization)
        frame_vis = ctk.CTkFrame(self.tab1)
        frame_vis.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # RAM Bar
        ctk.CTkLabel(frame_vis, text="RAM (Main Memory) - 500 KB", font=("Arial", 14, "bold"), text_color="#2CC985").pack(anchor="w", pady=(10, 0))
        self.cv_ram = tk.Canvas(frame_vis, height=120, bg="#1A1A1A", highlightthickness=0)
        self.cv_ram.pack(fill="x", pady=5)

        # Disk Bar
        ctk.CTkLabel(frame_vis, text="DISK (Virtual Memory) - 1000 KB", font=("Arial", 14, "bold"), text_color="#3B8ED0").pack(anchor="w", pady=(20, 0))
        self.cv_disk = tk.Canvas(frame_vis, height=120, bg="#1A1A1A", highlightthickness=0)
        self.cv_disk.pack(fill="x", pady=5)

        # Log Box
        ctk.CTkLabel(frame_vis, text="System Logs:", anchor="w").pack(fill="x", pady=(10,0))
        self.log1 = ctk.CTkTextbox(frame_vis, height=150, font=("Consolas", 12))
        self.log1.pack(fill="both", expand=True, pady=5)

    def log_tab1(self, msg): 
        self.log1.insert("end", f"> {msg}\n")
        self.log1.see("end")

    def t1_alloc(self):
        try:
            pid, size = self.t1_pid.get(), int(self.t1_size.get())
            if pid: 
                self.cont_mgr.allocate(pid, size, self.t1_algo.get())
                self.t1_draw()
        except ValueError: self.log_tab1("⚠️ Invalid Size")

    def t1_dealloc(self):
        self.cont_mgr.deallocate(self.t1_kill.get())
        self.t1_draw()

    def t1_compact(self):
        self.cont_mgr.compact()
        self.t1_draw()

    def t1_draw(self):
        self.draw_bar(self.cv_ram, self.cont_mgr.ram_map, self.cont_mgr.ram_size)
        self.draw_bar(self.cv_disk, self.cont_mgr.disk_map, self.cont_mgr.disk_size)

    # ========================================================
    #  TAB 2: PAGING MEMORY (Grid + Page Table Inspector)
    # ========================================================
    def setup_tab2(self):
        # 1. Left Sidebar
        frame_ctrl = ctk.CTkFrame(self.tab2, width=280)
        frame_ctrl.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(frame_ctrl, text="PAGING CONTROLS", font=("Arial", 18, "bold")).pack(pady=15)
        
        # Allocation Inputs
        self.t2_pid = ctk.CTkEntry(frame_ctrl, placeholder_text="PID (e.g. P1)")
        self.t2_pid.pack(pady=5, padx=10)
        self.t2_size = ctk.CTkEntry(frame_ctrl, placeholder_text="Size (KB)")
        self.t2_size.pack(pady=5, padx=10)
        
        ctk.CTkButton(frame_ctrl, text="🧩 Allocate Pages", fg_color="#9B59B6", 
                      command=self.t2_alloc).pack(pady=15, padx=10)
        
        # Kill Section
        ctk.CTkFrame(frame_ctrl, height=2, fg_color="grey").pack(fill="x", padx=10, pady=10)
        self.t2_kill = ctk.CTkEntry(frame_ctrl, placeholder_text="PID to Kill")
        self.t2_kill.pack(pady=5, padx=10)
        ctk.CTkButton(frame_ctrl, text="💀 Kill Process", fg_color="#FF474C", 
                      command=self.t2_dealloc).pack(pady=5, padx=10)

        # --- INSPECTOR ---
        ctk.CTkFrame(frame_ctrl, height=2, fg_color="grey").pack(fill="x", padx=10, pady=20)
        ctk.CTkLabel(frame_ctrl, text="🔍 INSPECTOR", font=("Arial", 14, "bold")).pack()
        
        ctk.CTkLabel(frame_ctrl, text="Select Process ID:").pack(pady=5)
        self.t2_inspect_opt = ctk.CTkOptionMenu(frame_ctrl, values=["None"])
        self.t2_inspect_opt.pack(pady=5)
        
        ctk.CTkButton(frame_ctrl, text="Show Page Table", fg_color="orange", text_color="black",
                      command=self.t2_show_table).pack(pady=10)

        # 2. Right Side (Visuals)
        frame_vis = ctk.CTkFrame(self.tab2)
        frame_vis.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Grid View
        ctk.CTkLabel(frame_vis, text="Physical Memory Frames (Scattered View)", font=("Arial", 14, "bold"), text_color="#9B59B6").pack(pady=(10,0))
        self.cv_grid = tk.Canvas(frame_vis, bg="#222", height=350, highlightthickness=0)
        self.cv_grid.pack(fill="x", pady=10)

        # Bottom Split: Log Box & Inspector Table
        frame_bottom = ctk.CTkFrame(frame_vis, fg_color="transparent")
        frame_bottom.pack(fill="both", expand=True)

        # Log Box (Left)
        frame_log = ctk.CTkFrame(frame_bottom)
        frame_log.pack(side="left", fill="both", expand=True, padx=(0,5))
        ctk.CTkLabel(frame_log, text="Event Logs:", anchor="w").pack(fill="x")
        self.log2 = ctk.CTkTextbox(frame_log, font=("Consolas", 12))
        self.log2.pack(fill="both", expand=True)

        # Inspector Output (Right)
        frame_table = ctk.CTkFrame(frame_bottom, width=250)
        frame_table.pack(side="right", fill="y", padx=(5,0))
        ctk.CTkLabel(frame_table, text="Page Table Map", font=("Arial", 12, "bold")).pack(pady=5)
        self.table_view = ctk.CTkTextbox(frame_table, width=200, font=("Consolas", 14))
        self.table_view.pack(fill="both", expand=True, pady=5)
        
        # Initial Draw
        self.tab2.update() 
        self.t2_draw()

    def log_tab2(self, msg): 
        self.log2.insert("end", f"> {msg}\n")
        self.log2.see("end")

    def update_pid_dropdown(self):
        # Refresh the dropdown with active PIDs
        active_pids = list(self.page_mgr.page_table.keys())
        if not active_pids:
            self.t2_inspect_opt.configure(values=["None"])
            self.t2_inspect_opt.set("None")
        else:
            self.t2_inspect_opt.configure(values=active_pids)
            if self.t2_inspect_opt.get() not in active_pids:
                self.t2_inspect_opt.set(active_pids[0])

    def t2_alloc(self):
        try:
            pid, size = self.t2_pid.get(), int(self.t2_size.get())
            if pid: 
                self.page_mgr.allocate(pid, size)
                self.update_pid_dropdown() 
                self.t2_draw()
        except ValueError: pass

    def t2_dealloc(self):
        self.page_mgr.deallocate(self.t2_kill.get())
        self.update_pid_dropdown() 
        self.t2_draw()
        self.table_view.delete("1.0", "end") 

    def t2_show_table(self):
        pid = self.t2_inspect_opt.get()
        self.table_view.delete("1.0", "end")
        
        if pid == "None" or pid not in self.page_mgr.page_table:
            self.table_view.insert("end", "No process selected.")
            return

        frames = self.page_mgr.page_table[pid]
        self.table_view.insert("end", f"PID: {pid}\n")
        self.table_view.insert("end", "-"*18 + "\n")
        self.table_view.insert("end", "Page # | Frame #\n")
        self.table_view.insert("end", "-"*18 + "\n")
        
        for page_num, frame_idx in enumerate(frames):
            self.table_view.insert("end", f"  {page_num:<4} ->   {frame_idx}\n")

    def t2_draw(self):
        self.cv_grid.delete("all")
        w = self.cv_grid.winfo_width()
        if w < 10: w = 600
        
        cols = 10
        box_size = w // cols
        if box_size > 40: box_size = 40 
        
        for i, pid in enumerate(self.page_mgr.frames):
            row = i // cols
            col = i % cols
            x1 = col * box_size + 2
            y1 = row * box_size + 2
            x2 = x1 + box_size - 4
            y2 = y1 + box_size - 4
            
            color = self.get_color(pid)
            
            self.cv_grid.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333")
            
            if pid:
                self.cv_grid.create_text((x1+x2)/2, (y1+y2)/2, text=pid, fill="black", font=("Arial", 9, "bold"))
            else:
                 self.cv_grid.create_text((x1+x2)/2, (y1+y2)/2, text=str(i), fill="#555", font=("Arial", 8))

    # ========================================================
    #  SHARED HELPER FUNCTIONS
    # ========================================================
    def get_color(self, pid):
        if pid is None: return "#2B2B2B"
        hash_obj = hashlib.md5(pid.encode())
        r = (int(hash_obj.hexdigest()[0:2], 16) % 100) + 100 
        g = (int(hash_obj.hexdigest()[2:4], 16) % 100) + 100
        b = (int(hash_obj.hexdigest()[4:6], 16) % 100) + 100
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_bar(self, cv, m_map, size):
        cv.delete("all")
        w = cv.winfo_width()
        if w < 10: w = 600
        scale = w / size
        
        for block in m_map:
            x1, x2 = block.start * scale, block.end * scale
            color = self.get_color(block.pid)
            
            cv.create_rectangle(x1, 5, x2, 115, fill=color, outline="black")
            
            if block.pid and (x2-x1) > 25:
                cv.create_text((x1+x2)/2, 60, text=f"{block.pid}\n{block.size}K", fill="black", font=("Arial", 10, "bold"))

if __name__ == "__main__":
    app = OSSuite()
    app.bind("<Configure>", lambda e: [app.t1_draw(), app.t2_draw()] if e.widget == app else None)
    app.mainloop()