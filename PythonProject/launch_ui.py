import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def launch_ui(best_state):
    window = tk.Tk()
    window.title("🚚 Vehicle Routing Solution")
    window.geometry("1000x900")
    window.configure(bg="#f5f5f5")

    # ===== Frame for Table =====
    frame_top = tk.Frame(window, bg="#f5f5f5")
    frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=10)

    label = tk.Label(frame_top, text="📦 Package Assignments", font=("Segoe UI", 14, "bold"), bg="#f5f5f5")
    label.pack(pady=(0, 10))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    tree = ttk.Treeview(frame_top, columns=("Vehicle ID", "Packages", "Route", "Total Weight"), show="headings", height=6)
    tree.heading("Vehicle ID", text="Vehicle ID")
    tree.heading("Packages", text="Package IDs")
    tree.heading("Route", text="Route [x,y]")
    tree.heading("Total Weight", text="Total Weight (kg)")

    tree.column("Vehicle ID", width=80, anchor="center")
    tree.column("Packages", width=200)
    tree.column("Route", width=400)
    tree.column("Total Weight", width=120, anchor="center")

    for vehicle in best_state:
        vehicle_id = vehicle["vehicle_id"]
        packages = [pkg["package_id"] for pkg in vehicle["packages"]]
        route = vehicle["route"]
        total_weight = sum(pkg["weight"] for pkg in vehicle["packages"])
        tree.insert("", tk.END, values=(vehicle_id, str(packages), str(route), f"{total_weight} kg"))

    tree.pack(fill=tk.BOTH, expand=False)

    # ===== Frame for Plot =====
    frame_bottom = tk.Frame(window, bg="#ffffff", relief=tk.GROOVE, borderwidth=2)
    frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig, ax = plt.subplots(figsize=(10, 6))
    shop = (0, 0)

    colors = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd']

    for i, vehicle in enumerate(best_state):
        color = colors[i % len(colors)]
        route = [shop] + vehicle["route"] + [shop]
        x, y = zip(*route)
        ax.plot(x, y, marker='o', markersize=8, linewidth=2, label=f"Vehicle {vehicle['vehicle_id']}", color=color)

        for pkg in vehicle["packages"]:
            px, py = pkg["location"]
            ax.text(px + 1, py + 1, str(pkg["package_id"]), fontsize=10, color=color, weight="bold")

    ax.plot(0, 0, 'ks', label='🏠 Shop (0,0)', markersize=10)
    ax.set_xlabel("X Position (km)", fontsize=12)
    ax.set_ylabel("Y Position (km)", fontsize=12)
    ax.set_title("🗺️ Vehicle Delivery Routes", fontsize=15, fontweight='bold')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_facecolor('#f0f8ff')

    canvas = FigureCanvasTkAgg(fig, master=frame_bottom)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    window.mainloop()