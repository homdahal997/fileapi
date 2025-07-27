#!/usr/bin/env python
"""
Simple desktop GUI for file conversion using tkinter
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import os
import threading
import time

class FileConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")
        self.root.geometry("600x400")
        self.base_url = "http://127.0.0.1:8000"
        
        self.setup_ui()
        self.load_formats()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="File Converter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        ttk.Label(main_frame, text="Select file:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.file_path_var, width=40).grid(row=1, column=1, padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=1, column=2, pady=5)
        
        # Output format selection
        ttk.Label(main_frame, text="Convert to:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar()
        self.format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, width=37)
        self.format_combo.grid(row=2, column=1, padx=(5, 5), pady=5)
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert File", command=self.convert_file)
        self.convert_btn.grid(row=3, column=1, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=3, pady=5)
        
        # Results area
        ttk.Label(main_frame, text="Results:").grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        self.results_text = tk.Text(main_frame, height=8, width=70)
        self.results_text.grid(row=7, column=0, columnspan=3, pady=5)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=7, column=3, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select file to convert",
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def load_formats(self):
        """Load available output formats"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/conversions/formats/")
            response.raise_for_status()
            data = response.json()
            
            formats = [f['name'].upper() for f in data['results'] if f['is_output_supported']]
            self.format_combo['values'] = formats
            
            if formats:
                self.format_combo.set(formats[0])
                
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load formats: {e}")
    
    def convert_file(self):
        """Start file conversion in background thread"""
        input_file = self.file_path_var.get()
        output_format = self.format_var.get().lower()
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid input file")
            return
        
        if not output_format:
            messagebox.showerror("Error", "Please select an output format")
            return
        
        # Disable UI during conversion
        self.convert_btn.config(state='disabled')
        self.progress.start()
        self.status_var.set("Converting...")
        
        # Start conversion in background
        thread = threading.Thread(target=self._convert_worker, args=(input_file, output_format))
        thread.daemon = True
        thread.start()
    
    def _convert_worker(self, input_file, output_format):
        """Background worker for file conversion"""
        try:
            # Upload and convert
            with open(input_file, 'rb') as f:
                files = {'input_file': f}
                data = {'output_format': output_format}
                
                response = requests.post(
                    f"{self.base_url}/api/v1/conversions/convert/",
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
            
            job_id = result['job_id']
            self.root.after(0, lambda: self.status_var.set(f"Job created: {job_id}"))
            
            # Wait for completion
            while True:
                status_response = requests.get(
                    f"{self.base_url}/api/v1/conversions/jobs/{job_id}/"
                )
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data['status'] == 'completed':
                    # Download result
                    download_response = requests.get(
                        f"{self.base_url}/api/v1/conversions/jobs/{job_id}/download/"
                    )
                    download_response.raise_for_status()
                    
                    # Save file
                    filename = os.path.basename(input_file)
                    name, _ = os.path.splitext(filename)
                    output_path = filedialog.asksaveasfilename(
                        title="Save converted file",
                        defaultextension=f".{output_format}",
                        initialname=f"{name}_converted.{output_format}",
                        filetypes=[(f"{output_format.upper()} files", f"*.{output_format}"), ("All files", "*.*")]
                    )
                    
                    if output_path:
                        with open(output_path, 'wb') as f:
                            f.write(download_response.content)
                        
                        self.root.after(0, lambda: self._conversion_complete(output_path, job_id))
                    else:
                        self.root.after(0, lambda: self._conversion_cancelled())
                    break
                    
                elif status_data['status'] == 'failed':
                    error_msg = status_data.get('error_message', 'Unknown error')
                    self.root.after(0, lambda: self._conversion_failed(error_msg))
                    break
                    
                else:
                    self.root.after(0, lambda: self.status_var.set(f"Status: {status_data['status']}..."))
                    time.sleep(2)
                    
        except requests.RequestException as e:
            self.root.after(0, lambda: self._conversion_failed(str(e)))
    
    def _conversion_complete(self, output_path, job_id):
        """Handle successful conversion"""
        self.progress.stop()
        self.convert_btn.config(state='normal')
        self.status_var.set("Conversion completed!")
        
        result_text = f"✓ Conversion successful!\n"
        result_text += f"Job ID: {job_id}\n"
        result_text += f"Output file: {output_path}\n"
        result_text += f"File size: {os.path.getsize(output_path)} bytes\n"
        result_text += "-" * 50 + "\n"
        
        self.results_text.insert(tk.END, result_text)
        self.results_text.see(tk.END)
        
        messagebox.showinfo("Success", f"File converted successfully!\nSaved to: {output_path}")
    
    def _conversion_failed(self, error_msg):
        """Handle failed conversion"""
        self.progress.stop()
        self.convert_btn.config(state='normal')
        self.status_var.set("Conversion failed!")
        
        result_text = f"✗ Conversion failed: {error_msg}\n"
        result_text += "-" * 50 + "\n"
        
        self.results_text.insert(tk.END, result_text)
        self.results_text.see(tk.END)
        
        messagebox.showerror("Error", f"Conversion failed: {error_msg}")
    
    def _conversion_cancelled(self):
        """Handle cancelled conversion"""
        self.progress.stop()
        self.convert_btn.config(state='normal')
        self.status_var.set("Conversion cancelled")

def main():
    root = tk.Tk()
    app = FileConverterGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
