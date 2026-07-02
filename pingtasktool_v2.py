import customtkinter as ctk
import threading
import datetime
from icmplib import multiping

# ================= THEME =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONSOLE_BG   = "#0D1117"
CONSOLE_FG   = "#C9D1D9"
COLOR_UP     = "#3FB950"
COLOR_DOWN   = "#F85149"
COLOR_HEADER = "#58A6FF"
COLOR_DIM    = "#6E7681"
FONT_MONO    = ("Consolas", 11)
FONT_LABEL   = ("Segoe UI", 11)
FONT_TITLE   = ("Segoe UI", 13, "bold")
FONT_BTN     = ("Segoe UI", 12, "bold")
FONT_CFG_LBL = ("Segoe UI", 10)
FONT_CFG_VAL = ("Consolas", 13, "bold")

INTERVAL     = 0.2
COLOR_CANCEL = "#E3B341"   # amber for cancel button

class PingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ICMP Ping Tool")
        self.geometry("880x580")
        self.minsize(700, 460)
        self.resizable(True, True)
        self._cancelled = False   # cancel flag
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -------- LEFT PANEL --------
        left = ctk.CTkFrame(self, width=230, corner_radius=10)
        left.grid(row=0, column=0, padx=(12,6), pady=12, sticky="nsew")
        left.grid_propagate(False)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="IP Address List",
                     font=FONT_TITLE).grid(row=0, column=0,
                                           padx=12, pady=(12,4), sticky="w")

        self.ip_box = ctk.CTkTextbox(left, font=FONT_MONO,
                                     fg_color="#161B22",
                                     border_color="#30363D",
                                     border_width=1,
                                     wrap="none")
        self.ip_box.grid(row=1, column=0, padx=10, pady=(0,8), sticky="nsew")
        self.ip_box.insert("end", "# one IP per line\n")

        # ── PING SETTINGS CARD ──
        cfg_card = ctk.CTkFrame(left, fg_color="#161B22",
                                corner_radius=8, border_width=1,
                                border_color="#30363D")
        cfg_card.grid(row=2, column=0, padx=10, pady=(0,8), sticky="ew")
        cfg_card.grid_columnconfigure((0,1), weight=1)

        ctk.CTkLabel(cfg_card, text="PING SETTINGS",
                     font=("Segoe UI", 9, "bold"),
                     text_color=COLOR_DIM).grid(row=0, column=0, columnspan=2,
                                                padx=10, pady=(8,6), sticky="w")

        # Count box
        count_frame = ctk.CTkFrame(cfg_card, fg_color="#0D1117",
                                   corner_radius=6, border_width=1,
                                   border_color="#30363D")
        count_frame.grid(row=1, column=0, padx=(8,4), pady=(0,10), sticky="ew")
        count_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(count_frame,
                     text="Ping Packet Count",
                     font=FONT_CFG_LBL,
                     text_color="#FFFFFF").grid(row=0, column=0,
                                                padx=8, pady=(6,0), sticky="w")
        self.count_var = ctk.StringVar(value="2")
        ctk.CTkEntry(count_frame,
                     textvariable=self.count_var,
                     font=FONT_CFG_VAL,
                     text_color="#FFFFFF",
                     justify="center",
                     height=36,
                     fg_color="transparent",
                     border_width=0).grid(row=1, column=0,
                                          padx=8, pady=(0,6), sticky="ew")

        # Timeout box
        timeout_frame = ctk.CTkFrame(cfg_card, fg_color="#0D1117",
                                     corner_radius=6, border_width=1,
                                     border_color="#30363D")
        timeout_frame.grid(row=1, column=1, padx=(4,8), pady=(0,10), sticky="ew")
        timeout_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(timeout_frame,
                     text="Timeout (s)",
                     font=FONT_CFG_LBL,
                     text_color="#FFFFFF").grid(row=0, column=0,
                                                padx=8, pady=(6,0), sticky="w")
        self.timeout_var = ctk.StringVar(value="1")
        ctk.CTkEntry(timeout_frame,
                     textvariable=self.timeout_var,
                     font=FONT_CFG_VAL,
                     text_color="#FFFFFF",
                     justify="center",
                     height=36,
                     fg_color="transparent",
                     border_width=0).grid(row=1, column=0,
                                          padx=8, pady=(0,6), sticky="ew")

        # Run button
        self.btn = ctk.CTkButton(left, text="▶  Run Ping",
                                 font=FONT_BTN,
                                 height=40,
                                 corner_radius=8,
                                 command=self._start_ping)
        self.btn.grid(row=3, column=0, padx=10, pady=(0,4), sticky="ew")

        # Cancel button
        self.cancel_btn = ctk.CTkButton(left, text="✕  Cancel",
                                        font=FONT_BTN,
                                        height=36,
                                        corner_radius=8,
                                        fg_color="#3A2000",
                                        hover_color="#5A3200",
                                        text_color=COLOR_CANCEL,
                                        border_width=1,
                                        border_color=COLOR_CANCEL,
                                        state="disabled",
                                        command=self._cancel_ping)
        self.cancel_btn.grid(row=4, column=0, padx=10, pady=(0,6), sticky="ew")

        # Clear button
        ctk.CTkButton(left, text="Clear Results",
                      font=FONT_LABEL,
                      height=28,
                      fg_color="transparent",
                      border_width=1,
                      border_color="#30363D",
                      hover_color="#21262D",
                      corner_radius=6,
                      command=self._clear).grid(row=5, column=0,
                                                padx=10, pady=(0,12), sticky="ew")

        # -------- RIGHT PANEL --------
        right = ctk.CTkFrame(self, corner_radius=10)
        right.grid(row=0, column=1, padx=(6,12), pady=12, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        top_bar = ctk.CTkFrame(right, fg_color="#161B22",
                               corner_radius=8, height=36)
        top_bar.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top_bar, text="● PING RESULTS",
                     font=("Consolas", 11, "bold"),
                     text_color=COLOR_HEADER).grid(row=0, column=0,
                                                    padx=10, sticky="w")

        self.status_lbl = ctk.CTkLabel(top_bar, text="idle",
                                       font=("Consolas", 10),
                                       text_color=COLOR_DIM)
        self.status_lbl.grid(row=0, column=1, padx=10, sticky="e")

        self.console = ctk.CTkTextbox(right,
                                      font=FONT_MONO,
                                      fg_color=CONSOLE_BG,
                                      text_color=CONSOLE_FG,
                                      border_color="#30363D",
                                      border_width=1,
                                      wrap="none",
                                      state="disabled")
        self.console.grid(row=1, column=0, padx=10, pady=(6,10), sticky="nsew")

        self.console.tag_config("up",     foreground=COLOR_UP)
        self.console.tag_config("down",   foreground=COLOR_DOWN)
        self.console.tag_config("header", foreground=COLOR_HEADER)
        self.console.tag_config("dim",    foreground=COLOR_DIM)
        self.console.tag_config("warn",   foreground="#E3B341")

        self._print("Ready. Enter IPs on the left and press Run Ping.\n", "dim")

    # -------- HELPERS --------
    def _print(self, text, tag=None):
        self.console.configure(state="normal")
        if tag:
            self.console.insert("end", text, tag)
        else:
            self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")

    def _clear(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self.status_lbl.configure(text="idle", text_color=COLOR_DIM)

    def _set_btn(self, enabled):
        if enabled:
            self.btn.configure(state="normal", text="▶  Run Ping")
            self.cancel_btn.configure(state="disabled")
            self._cancelled = False
        else:
            self.btn.configure(state="disabled", text="Running...")
            self.cancel_btn.configure(state="normal")

    def _set_status(self, text, color=COLOR_DIM):
        self.status_lbl.configure(text=text, text_color=color)

    def _cancel_ping(self):
        self._cancelled = True
        self._set_status("cancelling...", COLOR_CANCEL)

    # -------- PING --------
    def _start_ping(self):
        raw = self.ip_box.get("1.0", "end").strip().splitlines()
        ips = [l.strip() for l in raw
               if l.strip() and not l.strip().startswith("#")]

        if not ips:
            self._print("⚠  No IPs found. Add IPs to the input box.\n", "warn")
            return

        try:
            count   = int(self.count_var.get())
            timeout = int(self.timeout_var.get())
        except ValueError:
            self._print("⚠  Ping Packet Count and Timeout must be integers.\n", "warn")
            return

        self._cancelled = False
        self._set_btn(False)
        self._set_status("pinging...", COLOR_HEADER)

        threading.Thread(target=self._run_ping,
                         args=(ips, count, timeout),
                         daemon=True).start()

    def _run_ping(self, ips, count, timeout):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.after(0, self._print, f"\n{'─'*60}\n", "dim")
        self.after(0, self._print, f"  Ping started : {ts}\n", "dim")
        self.after(0, self._print, f"  Targets      : {len(ips)} IPs  |  Packets: {count}  |  Timeout: {timeout}s\n", "dim")
        self.after(0, self._print, f"{'─'*60}\n", "dim")
        self.after(0, self._print, f"\n{'IP':<20} {'STATUS':<7} {'AVG RTT (ms)':<14} {'LOSS %'}\n", "header")
        self.after(0, self._print, f"{'─'*55}\n", "dim")

        try:
            hosts = multiping(
                ips,
                count=count,
                interval=INTERVAL,
                timeout=timeout,
                concurrent_tasks=50,
                privileged=False
            )

            up_count   = 0
            down_count = 0

            for host in hosts:
                if self._cancelled:
                    def _cancelled_msg():
                        self._print(f"\n⚠  Cancelled by user.\n", "warn")
                        self._set_status("cancelled", COLOR_CANCEL)
                        self._set_btn(True)
                    self.after(0, _cancelled_msg)
                    return

                is_up   = host.is_alive
                status  = "UP" if is_up else "DOWN"
                avg_rtt = f"{host.avg_rtt:.2f}" if is_up and host.avg_rtt is not None else "-"
                loss    = f"{host.packet_loss * 100:.0f}%"
                tag     = "up" if is_up else "down"
                line    = f"{host.address:<20} {status:<7} {avg_rtt:<14} {loss}\n"
                self.after(0, self._print, line, tag)

                if is_up:
                    up_count += 1
                else:
                    down_count += 1

            def _finish():
                self._print(f"\n{'─'*55}\n", "dim")
                self._print(f"  Total: {len(hosts)}   ", "dim")
                self._print(f"UP: {up_count}  ", "up")
                self._print(f"DOWN: {down_count}\n\n", "down")
                self._set_status(f"done — {up_count} up / {down_count} down",
                                 COLOR_UP if down_count == 0 else COLOR_DOWN)
                self._set_btn(True)

            self.after(0, _finish)

        except Exception as e:
            def _err():
                self._print(f"\n⚠  Error: {e}\n", "warn")
                self._set_status("error", COLOR_DOWN)
                self._set_btn(True)
            self.after(0, _err)


if __name__ == "__main__":
    app = PingApp()
    app.mainloop()
