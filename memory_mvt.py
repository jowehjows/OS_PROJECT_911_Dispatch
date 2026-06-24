import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MemoryModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f171e")
        self.TOTAL_RESPONDERS = 32
        self.responder_fleet_map = ["Free"] * self.TOTAL_RESPONDERS
        self.allocated_incidents_mem = []
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.LabelFrame(self, text=" DEPLOY EMERGENCY RESPONDER TEAM (MVT ALLOCATION) ", bg="#0f171e", fg="#ffcc00", font=("Courier", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Incident Name:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.mem_desc_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=15)
        self.mem_desc_ent.pack(side=tk.LEFT, padx=5)
        self.mem_desc_ent.insert(0, "Fire-Squad")

        tk.Label(form_frame, text="Units Needed (Blocks):", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.mem_size_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=8)
        self.mem_size_ent.pack(side=tk.LEFT, padx=5)
        self.mem_size_ent.insert(0, "6")

        tk.Label(form_frame, text="Fit Strategy:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.mem_fit_var = tk.StringVar(value="First Fit")
        self.mem_fit_box = ttk.Combobox(form_frame, textvariable=self.mem_fit_var, values=["First Fit", "Best Fit", "Worst Fit"], width=12, state="readonly")
        self.mem_fit_box.pack(side=tk.LEFT, padx=5)

        tk.Button(form_frame, text="Deploy & Allocate Fleet", bg="#1c2d3d", fg="white", font=("Courier", 9, "bold"), command=self.add_memory_incident, width=22).pack(side=tk.LEFT, padx=10)
        tk.Button(form_frame, text="🎲 Randomize 4", bg="#1c2d3d", fg="white", font=("Courier", 9, "bold"), command=self.randomize_mem_incidents).pack(side=tk.LEFT, padx=2)

        table_frame = tk.Frame(self, bg="#0f171e")
        table_frame.pack(fill=tk.X, pady=5)
        
        self.mem_tree = ttk.Treeview(table_frame, columns=("ID", "Incident Name", "Size (Units)", "Sector Range"), show='headings', height=5)
        self.mem_tree.heading("ID", text="DEPLOY ID")
        self.mem_tree.heading("Incident Name", text="Emergency Sector Name")
        self.mem_tree.heading("Size (Units)", text="Allocated Fleet Units")
        self.mem_tree.heading("Sector Range", text="Physical RAM Block Indices")
        self.mem_tree.pack(fill=tk.X, expand=True)

        bottom_workspace = tk.Frame(self, bg="#0f171e")
        bottom_workspace.pack(fill=tk.BOTH, expand=True, pady=5)
        
        left_ctrls = tk.Frame(bottom_workspace, bg="#0f171e")
        left_ctrls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        action_row = tk.Frame(left_ctrls, bg="#0f171e")
        action_row.pack(fill=tk.X, anchor="w", pady=2)
        
        tk.Label(action_row, text="Terminate Deploy ID:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=2)
        self.mem_term_ent = tk.Entry(action_row, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.mem_term_ent.pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_row, text="Recall / Free Fleet", bg="#d35400", fg="white", font=("Courier", 9, "bold"), command=self.terminate_memory_incident).pack(side=tk.LEFT, padx=5)
        tk.Button(action_row, text="⚡ Run Fleet Compaction ⚡", bg="#2980b9", fg="white", font=("Courier", 9, "bold"), command=self.execute_fleet_compaction).pack(side=tk.LEFT, padx=2)

        tk.Label(left_ctrls, text="Fleet Allocation Core Log", bg="#0f171e", fg="#1abc9c", font=("Courier", 10, "bold")).pack(anchor="w", pady=(8,2))
        self.mem_log_txt = tk.Text(left_ctrls, bg="#111111", fg="#ffffff", font=("Courier", 10), height=15, width=45)
        self.mem_log_txt.pack(fill=tk.BOTH, expand=True)

        right_graph = tk.Frame(bottom_workspace, bg="#16222f", relief="solid", bd=1)
        right_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.mem_fig = Figure(figsize=(6, 4), dpi=95, facecolor='#16222f')
        self.mem_ax = self.mem_fig.add_subplot(111)
        self.mem_canvas = FigureCanvasTkAgg(self.mem_fig, master=right_graph)
        self.mem_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sync_mem_table_ui()
        self.repaint_responder_grid()

    def sync_mem_table_ui(self):
        for item in self.mem_tree.get_children(): self.mem_tree.delete(item)
        for i in self.allocated_incidents_mem:
            range_str = f"Blocks {i['start']:02d} - {i['start'] + i['size'] - 1:02d}"
            self.mem_tree.insert("", tk.END, values=(i["id"], i["name"], i["size"], range_str))

    def repaint_responder_grid(self):
        self.mem_ax.clear()
        self.mem_ax.set_facecolor('#0f171e')
        self.mem_ax.set_title("Physical RAM Structure Layout (Dynamic Size Blocks)", color="white", fontname="Courier", fontsize=11, fontweight="bold")
        self.mem_ax.set_xlabel("Physical RAM Blocks (0 to 31)", color="white", fontname="Courier")
        self.mem_ax.tick_params(colors='white')
        self.mem_ax.set_xlim(0, self.TOTAL_RESPONDERS)
        self.mem_ax.set_ylim(-0.5, len(self.allocated_incidents_mem) + 0.5 if self.allocated_incidents_mem else 1.5)

        if not self.allocated_incidents_mem:
            self.mem_ax.barh(0, self.TOTAL_RESPONDERS, left=0, height=0.5, color="#2c3e50", edgecolor="#ffffff")
            self.mem_ax.text(self.TOTAL_RESPONDERS/2, 0, "Entire Fleet Empty (32 Blocks Free)", color="white", ha="center", va="center", fontname="Courier", weight="bold")
        else:
            for idx, item in enumerate(self.allocated_incidents_mem):
                self.mem_ax.barh(idx, item["size"], left=item["start"], height=0.6, color="#27ae60", edgecolor="#ffffff")
                self.mem_ax.text(item["start"] + item["size"]/2, idx, f"{item['name']}\n[{item['size']} Units]", 
                                 color="white", ha="center", va="center", fontsize=8, weight="bold")
            
            i = 0
            void_idx = len(self.allocated_incidents_mem)
            while i < self.TOTAL_RESPONDERS:
                if self.responder_fleet_map[i] == "Free":
                    start_void = i
                    while i < self.TOTAL_RESPONDERS and self.responder_fleet_map[i] == "Free": i += 1
                    void_size = i - start_void
                    self.mem_ax.barh(void_idx, void_size, left=start_void, height=0.4, color="#e74c3c", edgecolor="#ffffff", alpha=0.4, linestyle="--")
                    self.mem_ax.text(start_void + void_size/2, void_idx, f"Free Hole\n({void_size} Unallocated)", color="#ff4a4a", ha="center", va="center", fontsize=8)
                    void_idx += 1
                else:
                    i += 1
                    
        self.mem_canvas.draw()

    def add_memory_incident(self):
        try:
            name = self.mem_desc_ent.get().strip()
            size = int(self.mem_size_ent.get())
            strategy = self.mem_fit_var.get()
            if size <= 0 or not name: raise ValueError
            
            holes = []
            in_hole = False
            start_h = -1
            length = 0
            
            for i in range(self.TOTAL_RESPONDERS):
                if self.responder_fleet_map[i] == "Free":
                    if not in_hole:
                        in_hole = True
                        start_h = i
                    length += 1
                else:
                    if in_hole:
                        holes.append({"start": start_h, "size": length})
                        in_hole = False
                        length = 0
            if in_hole:
                holes.append({"start": start_h, "size": length})

            viable_holes = [h for h in holes if h["size"] >= size]
            
            if not viable_holes:
                self.mem_log_txt.insert(tk.END, f"[REJECTED] Cannot fit {size} units for '{name}'. External Fragmentation detected!\n")
                messagebox.showwarning("Memory Error", "No available continuous sector block matches requirements. Trigger Compaction.")
                return

            if strategy == "First Fit":
                target_hole = viable_holes[0]
            elif strategy == "Best Fit":
                target_hole = min(viable_holes, key=lambda x: x["size"])
            elif strategy == "Worst Fit":
                target_hole = max(viable_holes, key=lambda x: x["size"])

            start_idx = target_hole["start"]
            for idx in range(start_idx, start_idx + size): 
                self.responder_fleet_map[idx] = name
                
            nid = len(self.allocated_incidents_mem) + 1
            self.allocated_incidents_mem.append({"id": nid, "name": name, "size": size, "start": start_idx})
            self.mem_log_txt.insert(tk.END, f"[{strategy.upper()}] '{name}' allocated inside blocks {start_idx} to {start_idx+size-1}.\n")
            
            self.sync_mem_table_ui()
            self.repaint_responder_grid()
        except ValueError:
            messagebox.showerror("Error", "Verify entry variables are configured correctly.")

    def randomize_mem_incidents(self):
        names = ["EMS-Squad", "Rescue-4", "K9-Unit", "SWAT-Team", "Hazmat-1", "Patrol-B", "State-Troop", "Coast-Guard"]
        self.responder_fleet_map = ["Free"] * self.TOTAL_RESPONDERS
        self.allocated_incidents_mem.clear()
        self.mem_log_txt.delete("1.0", tk.END)
        self.mem_log_txt.insert(tk.END, f"--- Initializing 4 Randomized Deployments via [{self.mem_fit_var.get()}] ---\n")
        
        current_idx = 0
        for i in range(1, 5):
            name = random.choice(names) + f"-{i}"
            size = random.randint(4, 7)
            if current_idx + size <= self.TOTAL_RESPONDERS:
                for idx in range(current_idx, current_idx + size): self.responder_fleet_map[idx] = name
                self.allocated_incidents_mem.append({"id": i, "name": name, "size": size, "start": current_idx})
                self.mem_log_txt.insert(tk.END, f"[ALLOCATED] '{name}' deployed into blocks {current_idx} to {current_idx+size-1}.\n")
                current_idx += size + random.randint(0, 1)
        self.sync_mem_table_ui()
        self.repaint_responder_grid()

    def terminate_memory_incident(self):
        try:
            tid = int(self.mem_term_ent.get())
            target = next((p for p in self.allocated_incidents_mem if p["id"] == tid), None)
            if target:
                for idx in range(target["start"], target["start"] + target["size"]): self.responder_fleet_map[idx] = "Free"
                self.allocated_incidents_mem.remove(target)
                self.mem_log_txt.insert(tk.END, f"[RELEASED] Deploy ID {tid} recalled. External fragmentation hole opened.\n")
                self.sync_mem_table_ui()
                self.repaint_responder_grid()
            else:
                messagebox.showerror("Error", "Deploy ID entry matching active signatures not discovered.")
        except ValueError:
            messagebox.showerror("Error", "Provide a valid numerical Deploy ID.")

    def execute_fleet_compaction(self):
        self.mem_log_txt.insert(tk.END, "[COMPACTION] Activating memory compaction sequence...\n")
        active_blocks = [unit for unit in self.responder_fleet_map if unit != "Free"]
        self.responder_fleet_map = active_blocks + (["Free"] * (self.TOTAL_RESPONDERS - len(active_blocks)))
        
        self.allocated_incidents_mem.clear()
        seen = {}
        current_id = 1
        for i, val in enumerate(self.responder_fleet_map):
            if val != "Free":
                if val not in seen:
                    seen[val] = {"id": current_id, "name": val, "size": 0, "start": i}
                    current_id += 1
                seen[val]["size"] += 1
        self.allocated_incidents_mem = list(seen.values())
        self.mem_log_txt.insert(tk.END, "[SUCCESS] Dispersed fragmentation holes consolidated at bottom.\n")
        self.sync_mem_table_ui()
        self.repaint_responder_grid()