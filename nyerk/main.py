import tkinter as tk
from tkinter import ttk

# Import the standalone module sub-frames
from cpu_dispatcher import CPUModule
from memory_mvt import MemoryModule
from virtual_memory import VirtualMemoryModule
from disk_router import DiskRouterModule

class ComprehensiveOSCADApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRISIS-LINK // Unified 4-in-1 OS Capstone Dashboard")
        self.root.geometry("1350x800")
        self.root.state('zoomed')  
        self.root.configure(bg="#0f171e")
        
        self.setup_styles()
        self.build_navigation_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#0f171e", foreground="#ffffff", fieldbackground="#16222f")
        style.configure("Treeview", background="#16222f", foreground="#ffffff", rowheight=24, fieldbackground="#16222f")
        style.map("Treeview", background=[('selected', '#1f5370')], foreground=[('selected', '#ffffff')])

    def build_navigation_layout(self):
        top_banner = tk.Label(self.root, text="🚨 SYSTEM INTERNALS CORE DASHBOARD // 911 COMPUTER AIDED DISPATCH TERMINAL 🚨",
                              bg="#16222f", fg="#ff4a4a", font=("Courier", 12, "bold"), pady=8, relief="raised", bd=1)
        top_banner.pack(fill=tk.X, side=tk.TOP)

        base_frame = tk.Frame(self.root, bg="#0f171e")
        base_frame.pack(fill=tk.BOTH, expand=True)

        # ---------------- SIDEBAR NAVIGATION MENU ----------------
        sidebar = tk.Frame(base_frame, bg="#111c24", width=240, relief="solid", bd=1)
        sidebar.pack_propagate(False)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        menu_title = tk.Label(sidebar, text="OS CAD ENGINE DIRECTORY", bg="#111c24", fg="#5dade2", font=("Courier", 10, "bold"), pady=15)
        menu_title.pack()

        modules = [
            ("1. CPU Dispatcher", self.show_cpu_module),
            ("2. Active Memory (MVT)", self.show_memory_module),
            ("3. Virtual Memory Unit", self.show_vm_module),
            ("4. Multi-Disk Router", self.show_storage_module)
        ]
        
        for name, callback in modules:
            btn = tk.Button(sidebar, text=name, bg="#1c2d3d", fg="#ffffff", activebackground="#293f54",
                            activeforeground="#ffffff", font=("Courier", 10), anchor="w", padx=15, pady=10,
                            bd=0, command=callback)
            btn.pack(fill=tk.X, pady=2, padx=5)

        # ---------------- SUB-PANEL CONTAINER CARD ----------------
        self.container_panel = tk.Frame(base_frame, bg="#0f171e")
        self.container_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Default initialization frame module on screen load
        self.show_cpu_module()

    def clear_container(self):
        for widget in self.container_panel.winfo_children():
            widget.destroy()

    def show_cpu_module(self):
        self.clear_container()
        frame = CPUModule(self.container_panel)
        frame.pack(fill=tk.BOTH, expand=True)

    def show_memory_module(self):
        self.clear_container()
        frame = MemoryModule(self.container_panel)
        frame.pack(fill=tk.BOTH, expand=True)

    def show_vm_module(self):
        self.clear_container()
        frame = VirtualMemoryModule(self.container_panel)
        frame.pack(fill=tk.BOTH, expand=True)

    def show_storage_module(self):
        self.clear_container()
        frame = DiskRouterModule(self.container_panel)
        frame.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = ComprehensiveOSCADApp(root)
    root.mainloop()