from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
import traceback
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from demo_01_histogram import run as run_histogram
from demo_02_equalization import run as run_equalization
from demo_03_matching import run as run_matching
from demo_04_adaptive_clahe import run as run_clahe
from demo_05_bbhe import run as run_bbhe
from demo_06_information_theory import run as run_information
from run_all import main as _unused_run_all_main  # import check only
from histogram_ops import (
    ambe,
    bbhe,
    clahe_equalization,
    global_equalization,
    histogram_match,
    image_mean,
    image_std,
    kl_to_uniform,
    load_gray,
    load_gray_or_synthetic,
    mutual_information,
    roll_horizontal,
    save_pgm,
    shannon_entropy,
    shuffled_same_histogram,
    synthetic_reference,
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
GUI_DIR = OUTPUTS_DIR / "gui_preview"

OPERATIONS = [
    "1. Histogram",
    "2. Global Histogram Equalization",
    "3. Histogram Matching",
    "4. CLAHE",
    "5. BBHE",
    "6. Information Theory",
]


def _open_folder(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def _format_metrics(name: str, image, original=None) -> str:
    lines = [
        f"{name}",
        f"  Mean              : {image_mean(image):.4f}",
        f"  Std. deviation    : {image_std(image):.4f}",
        f"  Shannon entropy   : {shannon_entropy(image):.6f} bits",
        f"  KL to uniform     : {kl_to_uniform(image):.6f} bits",
    ]
    if original is not None:
        lines.append(f"  AMBE vs. input    : {ambe(original, image):.4f}")
    return "\n".join(lines)


def _run_all_demos(input_path: str | None, reference_path: str | None) -> None:
    run_histogram(input_path, str(OUTPUTS_DIR / "01_histogram"))
    run_equalization(input_path, str(OUTPUTS_DIR / "02_global_equalization"))
    run_matching(input_path, reference_path, str(OUTPUTS_DIR / "03_histogram_matching"))
    run_clahe(input_path, str(OUTPUTS_DIR / "04_clahe"))
    run_bbhe(input_path, str(OUTPUTS_DIR / "05_bbhe"))
    run_information(input_path, str(OUTPUTS_DIR / "06_information_theory"))

    img = load_gray_or_synthetic(input_path)
    he, _ = global_equalization(img)
    cl = clahe_equalization(img)
    bh, _ = bbhe(img)
    rows = [("input", img), ("global_he", he), ("clahe", cl), ("bbhe", bh)]
    lines = ["method,mean,std,entropy_bits,kl_to_uniform_bits,ambe_vs_input"]
    for name, arr in rows:
        lines.append(
            f"{name},{image_mean(arr):.6f},{image_std(arr):.6f},"
            f"{shannon_entropy(arr):.6f},{kl_to_uniform(arr):.6f},{ambe(img,arr):.6f}"
        )
    (OUTPUTS_DIR / "summary_metrics.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


class HistogramGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Histogram Equalization Lecture - Offline GUI")
        self.geometry("1180x760")
        self.minsize(980, 680)

        self.input_path: str | None = None
        self.reference_path: str | None = None
        self.operation_var = tk.StringVar(value=OPERATIONS[1])
        self.input_label_var = tk.StringVar(value="Synthetic educational image (offline default)")
        self.reference_label_var = tk.StringVar(value="Synthetic reference (default)")
        self.status_var = tk.StringVar(value="Ready - no pip / no PyPI / no third-party packages")
        self.events: queue.Queue = queue.Queue()
        self._input_photo = None
        self._result_photo = None

        self._build_ui()
        self.after(100, self._drain_events)
        self.after(150, self._show_initial_preview)

    def _build_ui(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("vista" if os.name == "nt" else "clam")
        except tk.TclError:
            pass

        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        title = ttk.Label(
            outer,
            text="Histogram Equalization Lecture - Offline GUI",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w")
        ttk.Label(
            outer,
            text="Python 3.12 standard library only | No pip | No PyPI | No NumPy/OpenCV/Matplotlib",
        ).pack(anchor="w", pady=(2, 10))

        controls = ttk.LabelFrame(outer, text="Controls", padding=10)
        controls.pack(fill="x")
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Input image:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Label(controls, textvariable=self.input_label_var).grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(controls, text="Choose image", command=self._choose_input).grid(row=0, column=2, padx=4)
        ttk.Button(controls, text="Use synthetic", command=self._use_synthetic).grid(row=0, column=3, padx=4)

        ttk.Label(controls, text="Reference:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Label(controls, textvariable=self.reference_label_var).grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(controls, text="Choose reference", command=self._choose_reference).grid(row=1, column=2, padx=4)
        ttk.Button(controls, text="Synthetic reference", command=self._use_synthetic_reference).grid(row=1, column=3, padx=4)

        ttk.Label(controls, text="Operation:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=8)
        combo = ttk.Combobox(controls, textvariable=self.operation_var, values=OPERATIONS, state="readonly")
        combo.grid(row=2, column=1, sticky="ew", pady=8)

        self.run_button = ttk.Button(controls, text="Run selected", command=self._run_selected)
        self.run_button.grid(row=2, column=2, padx=4)
        self.run_all_button = ttk.Button(controls, text="Run ALL demos", command=self._run_all)
        self.run_all_button.grid(row=2, column=3, padx=4)

        ttk.Button(controls, text="Open outputs folder", command=lambda: _open_folder(OUTPUTS_DIR)).grid(
            row=3, column=2, padx=4, pady=(4, 0)
        )
        ttk.Button(controls, text="Open GUI output", command=lambda: _open_folder(GUI_DIR)).grid(
            row=3, column=3, padx=4, pady=(4, 0)
        )
        ttk.Label(
            controls,
            text="Dependency-free input: PGM/BMP. PNG/JPEG also works only if Pillow is already installed.",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True, pady=(12, 0))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = ttk.LabelFrame(body, text="Input preview", padding=8)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        right = ttk.LabelFrame(body, text="Result preview", padding=8)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        self.input_preview = ttk.Label(left, text="Loading preview...", anchor="center")
        self.input_preview.pack(fill="both", expand=True)
        self.result_preview = ttk.Label(right, text="Run an operation to see the result", anchor="center")
        self.result_preview.pack(fill="both", expand=True)

        lower = ttk.Panedwindow(outer, orient="horizontal")
        lower.pack(fill="both", expand=False, pady=(10, 0))
        metrics_frame = ttk.LabelFrame(lower, text="Metrics / information", padding=6)
        log_frame = ttk.LabelFrame(lower, text="Log", padding=6)
        lower.add(metrics_frame, weight=1)
        lower.add(log_frame, weight=1)

        self.metrics = tk.Text(metrics_frame, height=10, wrap="word", font=("Consolas", 10))
        self.metrics.pack(fill="both", expand=True)
        self.metrics.insert("1.0", "Select an operation and click Run selected.\n")
        self.metrics.configure(state="disabled")

        self.log = tk.Text(log_frame, height=10, wrap="word", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True)
        self._append_log("GUI started in fully offline mode.")

        status = ttk.Frame(outer)
        status.pack(fill="x", pady=(8, 0))
        self.progress = ttk.Progressbar(status, mode="indeterminate", length=180)
        self.progress.pack(side="left", padx=(0, 10))
        ttk.Label(status, textvariable=self.status_var).pack(side="left", fill="x", expand=True)

    def _set_busy(self, busy: bool, message: str) -> None:
        state = "disabled" if busy else "normal"
        self.run_button.configure(state=state)
        self.run_all_button.configure(state=state)
        self.status_var.set(message)
        if busy:
            self.progress.start(10)
        else:
            self.progress.stop()

    def _append_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text.rstrip() + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_metrics(self, text: str) -> None:
        self.metrics.configure(state="normal")
        self.metrics.delete("1.0", "end")
        self.metrics.insert("1.0", text)
        self.metrics.configure(state="disabled")

    def _choose_input(self) -> None:
        path = filedialog.askopenfilename(
            title="Choose grayscale input image",
            filetypes=[
                ("Offline supported", "*.pgm *.pnm *.bmp"),
                ("Images", "*.png *.jpg *.jpeg *.pgm *.pnm *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if path:
            try:
                img = load_gray(path)
                self.input_path = path
                self.input_label_var.set(path)
                self._show_image(self.input_preview, img, "input")
                self._set_metrics(_format_metrics("INPUT", img))
                self._append_log(f"Input selected: {path}")
            except Exception as exc:
                messagebox.showerror("Input error", str(exc))

    def _use_synthetic(self) -> None:
        self.input_path = None
        self.input_label_var.set("Synthetic educational image (offline default)")
        self._show_initial_preview()
        self._append_log("Using synthetic educational input.")

    def _choose_reference(self) -> None:
        path = filedialog.askopenfilename(
            title="Choose reference image for histogram matching",
            filetypes=[
                ("Offline supported", "*.pgm *.pnm *.bmp"),
                ("Images", "*.png *.jpg *.jpeg *.pgm *.pnm *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if path:
            try:
                _ = load_gray(path)
                self.reference_path = path
                self.reference_label_var.set(path)
                self._append_log(f"Reference selected: {path}")
            except Exception as exc:
                messagebox.showerror("Reference error", str(exc))

    def _use_synthetic_reference(self) -> None:
        self.reference_path = None
        self.reference_label_var.set("Synthetic reference (default)")
        self._append_log("Using synthetic histogram-matching reference.")

    def _show_initial_preview(self) -> None:
        try:
            img = load_gray_or_synthetic(self.input_path)
            self._show_image(self.input_preview, img, "input")
            self._set_metrics(_format_metrics("INPUT", img))
        except Exception as exc:
            self._append_log(f"Preview error: {exc}")

    def _show_image(self, widget: ttk.Label, image, stem: str) -> None:
        GUI_DIR.mkdir(parents=True, exist_ok=True)
        path = GUI_DIR / f"{stem}_preview.pgm"
        save_pgm(path, image)
        photo = tk.PhotoImage(file=str(path))
        w, h = photo.width(), photo.height()
        factor = max(1, (max(w, h) + 379) // 380)
        if factor > 1:
            photo = photo.subsample(factor, factor)
        widget.configure(image=photo, text="")
        if widget is self.input_preview:
            self._input_photo = photo
        else:
            self._result_photo = photo

    def _run_selected(self) -> None:
        op = self.operation_var.get()
        self._set_busy(True, f"Running {op} ...")
        self._append_log(f"Running selected operation: {op}")
        threading.Thread(target=self._selected_worker, args=(op,), daemon=True).start()

    def _run_all(self) -> None:
        self._set_busy(True, "Running all six demos ...")
        self._append_log("Running ALL demos...")
        threading.Thread(target=self._all_worker, daemon=True).start()

    def _selected_worker(self, op: str) -> None:
        try:
            img = load_gray_or_synthetic(self.input_path)
            result = img
            extra = ""

            if op.startswith("1."):
                run_histogram(self.input_path, str(OUTPUTS_DIR / "01_histogram"))
                result = img
                extra = "Histogram files written to outputs/01_histogram."
            elif op.startswith("2."):
                run_equalization(self.input_path, str(OUTPUTS_DIR / "02_global_equalization"))
                result, _ = global_equalization(img)
            elif op.startswith("3."):
                run_matching(self.input_path, self.reference_path, str(OUTPUTS_DIR / "03_histogram_matching"))
                ref = load_gray(self.reference_path) if self.reference_path else synthetic_reference(len(img), len(img[0]))
                result, _ = histogram_match(img, ref)
                extra = "REFERENCE\n" + _format_metrics("Reference", ref)
            elif op.startswith("4."):
                run_clahe(self.input_path, str(OUTPUTS_DIR / "04_clahe"))
                result = clahe_equalization(img, clip_limit=2.0, tile_grid=(8, 8))
            elif op.startswith("5."):
                run_bbhe(self.input_path, str(OUTPUTS_DIR / "05_bbhe"))
                result, _ = bbhe(img)
            elif op.startswith("6."):
                run_information(self.input_path, str(OUTPUTS_DIR / "06_information_theory"))
                result, _ = global_equalization(img)
                shifted = roll_horizontal(img, 12)
                shuffled = shuffled_same_histogram(img, 11)
                extra = (
                    "INFORMATION-THEORETIC COMPARISON\n"
                    f"  MI(input,input)     : {mutual_information(img, img):.6f} bits\n"
                    f"  MI(input,shifted)   : {mutual_information(img, shifted):.6f} bits\n"
                    f"  MI(input,shuffled)  : {mutual_information(img, shuffled):.6f} bits\n"
                    "  Note: shuffled image preserves the marginal histogram but destroys spatial organization."
                )
            else:
                raise ValueError(f"Unknown operation: {op}")

            metrics = _format_metrics("INPUT", img) + "\n\n" + _format_metrics("RESULT", result, img)
            if extra:
                metrics += "\n\n" + extra
            self.events.put(("selected_ok", op, img, result, metrics))
        except Exception:
            self.events.put(("error", traceback.format_exc()))

    def _all_worker(self) -> None:
        try:
            _run_all_demos(self.input_path, self.reference_path)
            img = load_gray_or_synthetic(self.input_path)
            result, _ = global_equalization(img)
            metrics_path = OUTPUTS_DIR / "summary_metrics.csv"
            metrics = "ALL DEMOS COMPLETED\n\n"
            if metrics_path.exists():
                metrics += metrics_path.read_text(encoding="utf-8")
            self.events.put(("all_ok", img, result, metrics))
        except Exception:
            self.events.put(("error", traceback.format_exc()))

    def _drain_events(self) -> None:
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                if kind == "selected_ok":
                    _, op, img, result, metrics = event
                    self._show_image(self.input_preview, img, "input")
                    self._show_image(self.result_preview, result, "result")
                    self._set_metrics(metrics)
                    self._set_busy(False, f"Finished: {op}")
                    self._append_log(f"Finished successfully: {op}")
                elif kind == "all_ok":
                    _, img, result, metrics = event
                    self._show_image(self.input_preview, img, "input")
                    self._show_image(self.result_preview, result, "result")
                    self._set_metrics(metrics)
                    self._set_busy(False, "All demos finished successfully.")
                    self._append_log("All demos finished successfully. Results are in outputs.")
                elif kind == "error":
                    _, tb = event
                    self._set_busy(False, "Execution failed - see log.")
                    self._append_log(tb)
                    last = tb.strip().splitlines()[-1] if tb.strip() else "Unknown error"
                    messagebox.showerror("Execution error", last)
        except queue.Empty:
            pass
        self.after(100, self._drain_events)


def self_test() -> int:
    """Headless smoke test: exercises the processing core without opening Tk."""
    try:
        OUTPUTS_DIR.mkdir(exist_ok=True)
        _run_all_demos(None, None)
        img = load_gray_or_synthetic(None)
        _ = global_equalization(img)
        _ = clahe_equalization(img)
        _ = bbhe(img)
        print("GUI/core self-test: OK")
        return 0
    except Exception:
        traceback.print_exc()
        return 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    app = HistogramGUI()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
