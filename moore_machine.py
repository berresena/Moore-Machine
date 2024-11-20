#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox

class MooreMachineSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Moore Makinesi Simülatörü")
        self.root.geometry("600x700")
        self.root.configure(bg="#FFB6C1")

        # Başlık
        title_label = tk.Label(root, text="Moore Makinesi Simülatörü", font=("Helvetica", 16, "bold"), bg="#ffe6ee")
        title_label.pack(pady=10)

        # Frame oluşturma
        input_frame = tk.Frame(root, bg="#ffe6ee")
        input_frame.pack(pady=5)

        # Durum bilgileri
        self.add_labeled_entry(input_frame, "Sonlu Durumlar (Q):", "states")
        self.add_labeled_entry(input_frame, "Girdi Alfabesi (S):", "input")
        self.add_labeled_entry(input_frame, "Çıktı Alfabesi (Γ):", "output")

        # Geçiş tablosu
        self.add_labeled_text(root, "Geçiş Tablosu (Format: q0\ta\tq1, q1\tb\tq2):", "transition_text")

        # Çıktı tablosu
        self.add_labeled_text(root, "Çıktı Tablosu (Format: q0\t1, q1\t0):", "output_table_text")

        # Giriş dizisi
        self.add_labeled_entry(root, "Giriş Dizisi:", "input_sequence")

        # Simüle Et butonu (Buton arka plan rengi ve yazı rengi güncellendi)
        button = tk.Button(root, text="Simüle Et", bg="#FFB6C1", fg="white", font=("Helvetica", 12, "bold"))
        button.pack(pady=20)

        # Çıkış alanı
        self.result_label = tk.Label(root, text="Sonuç:", font=("Helvetica", 12, "bold"), bg="#FFE6EE")
        self.result_label.pack(pady=5)
        self.result_text = tk.Text(root, height=5, width=70, state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(pady=5)

        # Stil eklemek için ttk Style
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10), padding=5)

    def add_labeled_entry(self, parent, label_text, attribute_name):
        """Etiketli bir giriş kutusu ekle."""
        frame = tk.Frame(parent, bg="#ffe6ee")
        frame.pack(fill="x", pady=5)
        label = tk.Label(frame, text=label_text, font=("Helvetica", 10), bg="#ffe6ee")
        label.pack(side="left", padx=5)
        entry = ttk.Entry(frame, width=40)
        entry.pack(side="left", padx=5)
        setattr(self, attribute_name + "_entry", entry)

    def add_labeled_text(self, parent, label_text, attribute_name):
        """Etiketli bir metin kutusu ekle."""
        label = tk.Label(parent, text=label_text, font=("Helvetica", 10), bg="#ffe6ee")
        label.pack(pady=5)
        text = tk.Text(parent, height=7, width=70, wrap=tk.WORD)
        text.pack(pady=5)
        setattr(self, attribute_name, text)

    def parse_input(self, entry):
        return entry.strip().split(',')

    def parse_table(self, text):
        table = {}
        for line in text.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) == 3:
                state, input_symbol, next_state = parts
                if state not in table:
                    table[state] = {}
                table[state][input_symbol] = next_state
        return table

    def parse_output(self, text):
        table = {}
        for line in text.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) == 2:
                state, output = parts
                table[state] = output
        return table

    def run_simulation(self):
        # Kullanıcı girdilerini al
        try:
            states = self.parse_input(self.states_entry.get())
            input_alphabet = self.parse_input(self.input_entry.get())
            output_alphabet = self.parse_input(self.output_entry.get())
            transition_table = self.parse_table(self.transition_text.get("1.0", tk.END))
            output_table = self.parse_output(self.output_table_text.get("1.0", tk.END))
            input_sequence = self.input_sequence_entry.get()

            # Simülasyon başlat
            current_state = states[0]
            result = []
            for symbol in input_sequence:
                if symbol not in input_alphabet:
                    raise ValueError(f"Giriş alfabesi geçersiz: {symbol}")
                current_state = transition_table[current_state][symbol]
                result.append(output_table[current_state])

            # Sonuçları göster
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, " ".join(result))
            self.result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Hata", f"Simülasyon sırasında bir hata oluştu:\n{e}")


# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = MooreMachineSimulator(root)
    root.mainloop()
