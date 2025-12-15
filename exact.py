import numpy as np
import itertools
from scipy.sparse import dok_matrix, csr_matrix
from scipy.sparse.linalg import eigsh
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import threading

# --- Çekirdek Fizik Mantığı ---

def generate_basis(n_site, n_max):
    """Hilbert uzayı baz durumlarını oluşturur."""
    return list(itertools.product(range(n_max+1), repeat=n_site))

def construct_hamiltonian(basis_states, t, U, mu, n_site, n_max):
    """Hamiltonyen matrisini oluşturur."""
    dim = len(basis_states)
    H = dok_matrix((dim, dim), dtype=np.float64)
    state_index = {state: idx for idx, state in enumerate(basis_states)}

    for idx, state in enumerate(basis_states):
        # Diagonal terimler: Yerinde etkileşim + kimyasal potansiyel
        diag_energy = sum(U/2 * n_i*(n_i-1) - mu*n_i for n_i in state)
        H[idx, idx] = diag_energy

        # Hopping terimleri (simetrik ekleme)
        for i in range(n_site):
            j = (i + 1) % n_site  # Periyodik sınır koşulları

            # i -> j yönü
            if state[i] > 0 and state[j] < n_max:
                new_state = list(state)
                new_state[i] -= 1
                new_state[j] += 1
                new_state = tuple(new_state)
                new_idx = state_index.get(new_state)
                if new_idx is not None:
                    matrix_element = -t * np.sqrt(state[i] * (state[j] + 1))
                    H[idx, new_idx] += matrix_element

            # j -> i yönü
            if state[j] > 0 and state[i] < n_max:
                new_state = list(state)
                new_state[j] -= 1
                new_state[i] += 1
                new_state = tuple(new_state)
                new_idx = state_index.get(new_state)
                if new_idx is not None:
                    matrix_element = -t * np.sqrt(state[j] * (state[i] + 1))
                    H[idx, new_idx] += matrix_element

    return H.tocsr()

def solve_system(params):
    """
    Sistemi çözer ve sonuçları döndürür.
    params: {t, U, mu, n_site, n_max} sözlüğü
    """
    try:
        t = float(params['t'])
        U = float(params['U'])
        mu = float(params['mu'])
        n_site = int(params['n_site'])
        n_max = int(params['n_max'])
    except ValueError:
        return {"error": "Lütfen tüm parametreleri sayısal olarak giriniz."}

    basis_states = generate_basis(n_site, n_max)
    if not basis_states:
        return {"error": "Baz durumları oluşturulamadı (n_site veya n_max hatalı olabilir)."}

    H = construct_hamiltonian(basis_states, t, U, mu, n_site, n_max)

    if H.shape[0] == 0:
        return {"error": "Hilbert uzayı boş."}

    # eigsh için k < N olmalı
    k = 1
    if H.shape[0] <= 1:
        # Matris çok küçükse sparse solver yerine dense veya direkt değer
        return {"error": f"Hilbert uzayı çok küçük ({H.shape[0]}), n_site veya n_max artırın."}

    try:
        eigenvalues, eigenvectors = eigsh(H, k=k, which='SA')
    except Exception as e:
        return {"error": f"Köşegenleştirme hatası: {str(e)}"}
    
    ground_energy = eigenvalues[0]
    ground_state = eigenvectors[:, 0]
    
    # Yoğunluk hesaplama
    density = np.zeros(n_site)
    for idx, state in enumerate(basis_states):
        prob = np.abs(ground_state[idx])**2
        density += prob * np.array(state)
    
    return {
        "ground_energy": ground_energy,
        "density": density,
        "basis_size": len(basis_states),
        "params": params
    }

# --- GUI ---

class BoseHubbardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bose-Hubbard Simülasyonu")
        self.root.geometry("500x600")

        # Stil
        style = ttk.Style()
        style.theme_use('clam')
        
        # Ana Çerçeve
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Başlık
        ttk.Label(main_frame, text="Parametreler", font=("Helvetica", 12, "bold")).pack(pady=5)

        # Girdiler
        self.entries = {}
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        params = [
            ("Hopping Genliği (t)", "1"),
            ("Kimyasal Potansiyel (mu)", "15"),
            ("Etkileşim (U)", "25"),
            ("Site Sayısı (n_site)", "6"),
            ("Max Bozon/Site (n_max)", "5")
        ]

        for i, (label_text, default_val) in enumerate(params):
            ttk.Label(input_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(input_frame)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky=tk.E, padx=5, pady=2)
            # Parametre anahtarını parantez içinden çıkar (t, U, mu...)
            key = label_text.split("(")[1].split(")")[0]  
            self.entries[key] = entry

        # Butonlar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        self.calc_btn = ttk.Button(btn_frame, text="Hesapla", command=self.start_calculation)
        self.calc_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = ttk.Button(btn_frame, text="Excel'e Kaydet", command=self.export_to_excel, state=tk.DISABLED)
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # Sonuç Alanı
        ttk.Label(main_frame, text="Sonuçlar", font=("Helvetica", 12, "bold")).pack(pady=5)
        self.result_text = tk.Text(main_frame, height=15, width=50)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

        self.last_results = None

    def start_calculation(self):
        """Hesaplamayı ayrı thread'de başlatır UI donmasın diye."""
        self.calc_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.status_var.set("Hesaplanıyor, lütfen bekleyin...")
        self.result_text.delete(1.0, tk.END)
        
        # Parametreleri al
        params = {}
        for key, entry in self.entries.items():
            params[key] = entry.get()
        
        thread = threading.Thread(target=self.run_simulation, args=(params,))
        thread.start()

    def run_simulation(self, params):
        results = solve_system(params)
        self.root.after(0, self.update_ui, results)

    def update_ui(self, results):
        self.calc_btn.config(state=tk.NORMAL)
        self.status_var.set("Tamamlandı")

        if "error" in results:
            messagebox.showerror("Hata", results["error"])
            self.result_text.insert(tk.END, f"Hata: {results['error']}")
            return

        self.last_results = results
        self.export_btn.config(state=tk.NORMAL)

        # Metin çıktısı
        out = f"--- Sonuçlar ---\n"
        out += f"Baz Boyutu: {results['basis_size']}\n"
        out += f"Temel Durum Enerjisi: {results['ground_energy']:.6f}\n\n"
        out += "Yoğunluk Dağılımı:\n"
        for i, val in enumerate(results['density']):
            out += f"Site {i}: {val:.4f}\n"
        out += f"\nOrtalama Yoğunluk: {np.mean(results['density']):.4f}\n"

        self.result_text.insert(tk.END, out)

    def export_to_excel(self):
        if not self.last_results:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if not file_path:
            return

        try:
            # Pandas ile veriyi hazırla
            res = self.last_results
            
            # Parametreler sayfası
            df_params = pd.DataFrame([res['params']])
            
            # Sonuçlar sayfası
            df_density = pd.DataFrame({
                'Site': range(len(res['density'])),
                'Density': res['density']
            })
            
            # Enerji bilgisi
            df_energy = pd.DataFrame({
                'Metric': ['Ground Energy', 'Basis Size', 'Average Density'],
                'Value': [res['ground_energy'], res['basis_size'], np.mean(res['density'])]
            })

            with pd.ExcelWriter(file_path) as writer:
                df_params.to_excel(writer, sheet_name='Parameters', index=False)
                df_density.to_excel(writer, sheet_name='Density', index=False)
                df_energy.to_excel(writer, sheet_name='Summary', index=False)
            
            messagebox.showinfo("Başarılı", f"Dosya kaydedildi:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BoseHubbardApp(root)
    root.mainloop()
