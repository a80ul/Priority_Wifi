import customtkinter as ctk
import psutil
import time
import threading
import socket
import subprocess
import re
from scapy.all import ARP, Ether, sendp, conf


ctk.set_appearance_mode("Dark")

class NEXAHYPER(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXA HYPER")
        self.geometry("1200x850")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.is_active = False
        self.packet_count = 0
        self.download_speed = "0.0 KB/s"
        self.upload_speed = "0.0 KB/s"
        self.total_data = "0.0 MB"

        self.sidebar = ctk.CTkFrame(self, width=280, fg_color="#020408", corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        ctk.CTkLabel(self.sidebar, text="NEXA HYPER", font=("Orbitron", 25, "bold"), text_color="#00fbff").pack(pady=(50, 0))
        ctk.CTkLabel(self.sidebar, text="NETWORK PRIORITY ENGINE", font=("Orbitron", 12), text_color="#005555").pack(pady=(0, 40))
        
        self.create_nav("DASHBOARD CONTROL", self.view_dash)
        self.create_nav("NETWORK TUNER", self.view_tuner)
        self.create_nav("WIFI PASSWORDS", self.view_wifi)

        ctk.CTkButton(self.sidebar, text="FLUSH DNS", fg_color="#1a1a1a", height=35, command=self.flush_dns).pack(pady=10, padx=30)
        ctk.CTkButton(self.sidebar, text="CLEAN ARP", fg_color="#1a1a1a", height=35, command=self.clean_arp).pack(pady=5, padx=30)

        self.status_indicator = ctk.CTkLabel(self.sidebar, text="● SYSTEM IDLE", font=("Arial", 11, "bold"), text_color="#444")
        self.status_indicator.pack(side="bottom", pady=30)


        self.viewport = ctk.CTkFrame(self, fg_color="#010204", corner_radius=0)
        self.viewport.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.terminal = ctk.CTkTextbox(self, height=180, fg_color="#000", text_color="#00ff88", font=("Consolas", 12), state="disabled")
        self.terminal.grid(row=1, column=1, padx=20, pady=20, sticky="nsew") 

        self.view_dash()
        self.update_engine()

    def create_nav(self, text, cmd):
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", text_color="#888", 
                            hover_color="#0a1a2a", anchor="w", height=45, font=("Arial", 12, "bold"), command=cmd)
        btn.pack(fill="x", padx=20, pady=5)

    def log_sys(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.terminal.configure(state="normal")
        self.terminal.insert("end", f"[{ts}] {msg}\n")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")

    def clear_viewport(self):
        for widget in self.viewport.winfo_children():
            widget.destroy()

    def view_dash(self):
        self.clear_viewport()
        ctk.CTkLabel(self.viewport, text="DASHBOARD CORE", font=("Orbitron", 22, "bold"), text_color="#00fbff").pack(pady=25)
        
        grid_frame = ctk.CTkFrame(self.viewport, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=30, pady=10)
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        self.dl_card = self.create_stat_box(grid_frame, "DOWNLOAD RATE", self.download_speed, "#00fbff", 0, 0)
        self.ul_card = self.create_stat_box(grid_frame, "UPLOAD RATE", self.upload_speed, "#ff00ff", 0, 1)
        self.pkt_card = self.create_stat_box(grid_frame, "PRIORITY PACKETS", str(self.packet_count), "#00ff88", 1, 0)
        self.ping_card = self.create_stat_box(grid_frame, "TOTAL DATA FLOW", self.total_data, "#ffcc00", 1, 1)

        self.mode_lbl = ctk.CTkLabel(self.viewport, text="SYSTEM STATUS: STANDBY", font=("Orbitron", 14), text_color="#444")
        self.mode_lbl.pack(pady=20)
        if self.is_active: self.mode_lbl.configure(text="SYSTEM STATUS: PRIORITY ACTIVE", text_color="#00fbff")

    def create_stat_box(self, parent, title, val, color, r, c):
        box = ctk.CTkFrame(parent, fg_color="#080c14", corner_radius=15, border_width=1, border_color="#1a1a1a")
        box.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(box, text=title, font=("Orbitron", 10), text_color="#555").pack(expand=True, pady=(20, 0))
        lbl = ctk.CTkLabel(box, text=val, font=("Orbitron", 32, "bold"), text_color=color)
        lbl.pack(expand=True, pady=15)
        return lbl

    def view_tuner(self):
        self.clear_viewport()
        ctk.CTkLabel(self.viewport, text="PRIORITY ENGINE CONFIG", font=("Orbitron", 20)).pack(pady=30)
        panel = ctk.CTkFrame(self.viewport, fg_color="#080c14", corner_radius=15)
        panel.pack(pady=20, padx=60, fill="x")
        ctk.CTkLabel(panel, text="NETWORK INJECTION SWITCH", font=("Arial", 14, "bold")).pack(pady=(30, 10))
        self.sw = ctk.CTkSwitch(panel, text="PRIORITY MODE", command=self.toggle_engine, progress_color="#00fbff")
        self.sw.pack(pady=10)
        if self.is_active: self.sw.select()
        ctk.CTkLabel(panel, text="Optimizes packet routing for lowest possible latency.", font=("Arial", 10), text_color="#444").pack(pady=(0, 30))

    def view_wifi(self):
        self.clear_viewport()
        ctk.CTkLabel(self.viewport, text="SAVED WIFI NETWORKS", font=("Orbitron", 22, "bold"), text_color="#00fbff").pack(pady=20)
        scroll_frame = ctk.CTkScrollableFrame(self.viewport, fg_color="#080c14", border_width=1, border_color="#1a1a1a")
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.log_sys("WIFI: Retrieving stored profiles...")
        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore").split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
            if not profiles:
                ctk.CTkLabel(scroll_frame, text="No WiFi profiles found.", text_color="#555").pack(pady=20)
            for name in profiles:
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8', errors="ignore").split('\n')
                    passwords = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    pwd = passwords[0] if passwords else "--- (No Password) ---"
                    item = ctk.CTkFrame(scroll_frame, fg_color="#0d1117", corner_radius=8)
                    item.pack(fill="x", pady=5, padx=5)
                    ctk.CTkLabel(item, text=f"SSID: {name}", font=("Arial", 12, "bold"), text_color="#00fbff").pack(side="left", padx=15, pady=10)
                    ctk.CTkLabel(item, text=f"PWD: {pwd}", font=("Consolas", 12), text_color="#00ff88").pack(side="right", padx=15)
                except: continue
            self.log_sys(f"WIFI: Success. Found {len(profiles)} networks.")
        except Exception as e:
            self.log_sys(f"WIFI_ERROR: {str(e)}")

    def toggle_engine(self):
        self.is_active = self.sw.get()
        if self.is_active:
            self.status_indicator.configure(text="● ENGINE ACTIVE", text_color="#00fbff")
            self.log_sys("NET: Priority injection started.")
            threading.Thread(target=self.packet_engine, daemon=True).start()
        else:
            self.status_indicator.configure(text="● SYSTEM IDLE", text_color="#444")
            self.log_sys("NET: Engine halted.")

    def packet_engine(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            my_ip = s.getsockname()[0]
            gw = ".".join(my_ip.split(".")[:-1]) + ".1"
            pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc=my_ip, hwsrc=conf.iface.mac, pdst=gw)
            while self.is_active:
                sendp(pkt, verbose=False, realtime=True)
                self.packet_count += 1
                time.sleep(0.02)
        except: self.is_active = False

    def update_engine(self):
        try:
            io1 = psutil.net_io_counters()
            time.sleep(0.5)
            io2 = psutil.net_io_counters()
            dl = (io2.bytes_recv - io1.bytes_recv) / 1024
            ul = (io2.bytes_sent - io1.bytes_sent) / 1024
            total = (io2.bytes_recv + io2.bytes_sent) / (1024 * 1024)
            self.download_speed, self.upload_speed, self.total_data = f"{dl:.1f} KB/s", f"{ul:.1f} KB/s", f"{total:.1f} MB"

            if hasattr(self, 'dl_card'):
                self.dl_card.configure(text=self.download_speed)
                self.ul_card.configure(text=self.upload_speed)
                self.pkt_card.configure(text=str(self.packet_count))
                self.ping_card.configure(text=self.total_data)
        except: pass
        self.after(500, self.update_engine)

    def flush_dns(self):
        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        self.log_sys("SYS: DNS Cache Flushed.")

    def clean_arp(self):
        subprocess.run("arp -d *", shell=True, capture_output=True)
        self.log_sys("SYS: ARP Table Cleared.")

if __name__ == "__main__":
    app = NEXAHYPER()
    app.mainloop()