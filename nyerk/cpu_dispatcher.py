import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f171e")
        self.cpu_incidents = []  
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.LabelFrame(self, text=" LOG NEW 911 INCIDENT ", bg="#0f171e", fg="#ffcc00", font=("Courier", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Desc:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_desc_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=15)
        self.cpu_desc_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_desc_ent.insert(0, "Assault")

        tk.Label(form_frame, text="Arrival:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_arr_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.cpu_arr_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_arr_ent.insert(0, "0")

        tk.Label(form_frame, text="Burst:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_burst_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.cpu_burst_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_burst_ent.insert(0, "10")

        tk.Label(form_frame, text="Priority (1=High):", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_prio_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.cpu_prio_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_prio_ent.insert(0, "1")

        tk.Button(form_frame, text="Add", bg="#1c2d3d", fg="white", font=("Courier", 9, "bold"), command=self.add_incident_to_table, width=8).pack(side=tk.LEFT, padx=10)
        tk.Button(form_frame, text="🎲 Randomize 4", bg="#1c2d3d", fg="white", font=("Courier", 9, "bold"), command=self.randomize_cpu_incidents).pack(side=tk.LEFT, padx=2)

        table_frame = tk.Frame(self, bg="#0f171e")
        table_frame.pack(fill=tk.X, pady=5)
        
        self.cpu_tree = ttk.Treeview(table_frame, columns=("ID", "Description", "Arrival Time", "Burst Time", "Priority"), show='headings', height=5)
        self.cpu_tree.heading("ID", text="ID")
        self.cpu_tree.heading("Description", text="Description")
        self.cpu_tree.heading("Arrival Time", text="Arrival Time")
        self.cpu_tree.heading("Burst Time", text="Burst Time")
        self.cpu_tree.heading("Priority", text="Priority")
        self.cpu_tree.pack(fill=tk.X, expand=True)

        bottom_workspace = tk.Frame(self, bg="#0f171e")
        bottom_workspace.pack(fill=tk.BOTH, expand=True, pady=5)
        
        left_ctrls = tk.Frame(bottom_workspace, bg="#0f171e")
        left_ctrls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        algo_row = tk.Frame(left_ctrls, bg="#0f171e")
        algo_row.pack(fill=tk.X, anchor="w", pady=2)
        
        tk.Label(algo_row, text="Algorithm:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=2)
        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_box = ttk.Combobox(algo_row, textvariable=self.algo_var, values=["FCFS", "SJF (Non-Preemptive)", "SRTF (SJF Preemptive)", "Priority (Non-Preemptive)", "Priority (Preemptive)"], width=22)
        self.algo_box.pack(side=tk.LEFT, padx=5)
        
        tk.Button(algo_row, text="Run Dispatch", bg="#229954", fg="white", font=("Courier", 9, "bold"), command=self.execute_cpu_dispatcher).pack(side=tk.LEFT, padx=5)
        tk.Button(algo_row, text="Clear Queue", bg="#d35400", fg="white", font=("Courier", 9, "bold"), command=self.clear_cpu_queue).pack(side=tk.LEFT, padx=2)

        tk.Label(left_ctrls, text="System Execution Log", bg="#0f171e", fg="#52be80", font=("Courier", 10, "bold")).pack(anchor="w", pady=(8,2))
        self.cpu_log_txt = tk.Text(left_ctrls, bg="#111111", fg="#ffffff", font=("Courier", 10), height=15, width=45)
        self.cpu_log_txt.pack(fill=tk.BOTH, expand=True)

        right_graph = tk.Frame(bottom_workspace, bg="#16222f", relief="solid", bd=1)
        right_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.cpu_fig = Figure(figsize=(6, 4), dpi=95, facecolor='#16222f')
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=right_graph)
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sync_cpu_table_ui()
        self.render_empty_gantt()

    def add_incident_to_table(self):
        try:
            desc = self.cpu_desc_ent.get().strip()
            arr = int(self.cpu_arr_ent.get())
            burst = int(self.cpu_burst_ent.get())
            prio = int(self.cpu_prio_ent.get())
            if arr < 0 or burst <= 0 or prio <= 0 or not desc: raise ValueError
            
            nid = len(self.cpu_incidents) + 1
            self.cpu_incidents.append({"id": nid, "desc": desc, "arrival": arr, "burst": burst, "priority": prio})
            self.sync_cpu_table_ui()
        except ValueError:
            messagebox.showerror("Error", "Verify item metrics are valid positive numbers.")

    def randomize_cpu_incidents(self):
        sample_pool = ["Traffic Stop", "Assault", "Heart Attack", "Structure Fire", "Robbery", "MVA Accident", "Noise Complaint", "Burglary"]
        self.cpu_incidents.clear()
        for i in range(1, 5):
            desc = random.choice(sample_pool)
            arr = random.randint(0, 15)
            burst = random.randint(3, 20)
            prio = random.randint(1, 4)
            self.cpu_incidents.append({"id": i, "desc": f"{desc} (p{i})", "arrival": arr, "burst": burst, "priority": prio})
        self.sync_cpu_table_ui()

    def clear_cpu_queue(self):
        self.cpu_incidents.clear()
        self.sync_cpu_table_ui()
        self.cpu_log_txt.delete("1.0", tk.END)
        self.render_empty_gantt()

    def sync_cpu_table_ui(self):
        for item in self.cpu_tree.get_children(): self.cpu_tree.delete(item)
        for i in self.cpu_incidents:
            self.cpu_tree.insert("", tk.END, values=(i["id"], i["desc"], i["arrival"], i["burst"], i["priority"]))

    def render_empty_gantt(self):
        self.cpu_ax.clear()
        self.cpu_ax.set_facecolor('#0f171e')
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=11, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.set_xlabel("Time Units", fontsize=10, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.tick_params(colors='white')
        self.cpu_canvas.draw()

    def execute_cpu_dispatcher(self):
        if not self.cpu_incidents:
            messagebox.showwarning("Warning", "Add some dispatch vectors into the simulation registry first.")
            return
        
        algo = self.algo_var.get()
        self.cpu_log_txt.delete("1.0", tk.END)
        self.cpu_log_txt.insert(tk.END, f"--- Running {algo} ---\n")
        
        processes = [dict(p) for p in self.cpu_incidents]
        gantt_chart = [] 
        current_time = 0
        completed = 0
        n = len(processes)
        
        for p in processes: p["remaining"] = p["burst"]
        last_pid = None
        block_start = 0

        if algo in ["FCFS", "SJF (Non-Preemptive)", "Priority (Non-Preemptive)"]:
            while completed < n:
                ready_pool = [p for p in processes if p["arrival"] <= current_time and p["remaining"] > 0]
                if not ready_pool:
                    current_time = min([p["arrival"] for p in processes if p["remaining"] > 0])
                    continue
                
                if algo == "FCFS": target = min(ready_pool, key=lambda x: x["arrival"])
                elif algo == "SJF (Non-Preemptive)": target = min(ready_pool, key=lambda x: (x["burst"], x["arrival"]))
                elif algo == "Priority (Non-Preemptive)": target = min(ready_pool, key=lambda x: (x["priority"], x["arrival"]))
                
                self.cpu_log_txt.insert(tk.END, f"Time {current_time}: Dispatching to {target['desc']}\n")
                gantt_chart.append({"id": target["id"], "desc": target["desc"], "start": current_time, "duration": target["burst"]})
                current_time += target["burst"]
                target["remaining"] = 0
                completed += 1
        else:
            timeline_history = []
            while completed < n and current_time < 1000:
                ready_pool = [p for p in processes if p["arrival"] <= current_time and p["remaining"] > 0]
                if not ready_pool:
                    timeline_history.append(None)
                    current_time += 1
                    continue
                
                if algo == "SRTF (SJF Preemptive)": target = min(ready_pool, key=lambda x: (x["remaining"], x["arrival"]))
                elif algo == "Priority (Preemptive)": target = min(ready_pool, key=lambda x: (x["priority"], x["arrival"]))
                
                timeline_history.append(target)
                target["remaining"] -= 1
                if target["remaining"] == 0: completed += 1
                current_time += 1

            if timeline_history:
                for t_idx, current_proc in enumerate(timeline_history):
                    if t_idx == 0:
                        last_pid = current_proc["id"] if current_proc else None
                        block_start = 0
                    else:
                        this_id = current_proc["id"] if current_proc else None
                        if this_id != last_pid:
                            if last_pid is not None:
                                matched_desc = next(p["desc"] for p in self.cpu_incidents if p["id"] == last_pid)
                                gantt_chart.append({"id": last_pid, "desc": matched_desc, "start": block_start, "duration": t_idx - block_start})
                            block_start = t_idx
                            last_pid = this_id
                if last_pid is not None:
                    matched_desc = next(p["desc"] for p in self.cpu_incidents if p["id"] == last_pid)
                    gantt_chart.append({"id": last_pid, "desc": matched_desc, "start": block_start, "duration": len(timeline_history) - block_start})
                
                for block in gantt_chart:
                    self.cpu_log_txt.insert(tk.END, f"Time {block['start']}: Dispatching to {block['desc']}\n")

        self.cpu_ax.clear()
        self.cpu_ax.set_facecolor('#0f171e')
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=11, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.set_xlabel("Time Units", fontsize=10, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.tick_params(colors='white')
        
        all_unique_descriptions = list(dict.fromkeys([p["desc"] for p in sorted(self.cpu_incidents, key=lambda x: x["arrival"])]))
        self.cpu_ax.set_yticks(range(len(all_unique_descriptions)))
        self.cpu_ax.set_yticklabels(all_unique_descriptions, fontname="Courier", color="white")
        
        x_ticks_positions = [0]
        for block in gantt_chart:
            y_position_index = all_unique_descriptions.index(block["desc"])
            self.cpu_ax.barh(y=y_position_index, width=block["duration"], left=block["start"], height=0.6, color="#4aa3df", edgecolor="#ffffff", align="center")
            self.cpu_ax.text(block["start"] + block["duration"]/2, y_position_index, f"ID:{block['id']}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
            end_time = block["start"] + block["duration"]
            if end_time not in x_ticks_positions: x_ticks_positions.append(end_time)
                
        x_ticks_positions.sort()
        self.cpu_ax.set_xticks(x_ticks_positions)
        self.cpu_ax.xaxis.grid(True, linestyle="--", alpha=0.3, color="#ffffff")
        self.cpu_ax.set_axisbelow(True)
        self.cpu_canvas.draw()