import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
from huffman import *
import json
import shutil

class HuffmanApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.huffman_coder = HuffmanCoding()

        self.title("Huffman Coding App")

        # Установка начального размера окна
        self.geometry("600x600")

        self.create_widgets()

        self.huffman_coder = HuffmanCoding()

        self.bind("<Escape>", lambda event: self.quit())
        
        self.canvas_top = tk.Canvas(self, bg="white", height=200)
        self.canvas_top.pack(fill="x", expand=True)

        # Добавляем синюю полоску по середине
        self.canvas_middle = tk.Canvas(self, bg="blue", height=200)
        self.canvas_middle.pack(fill="x", expand=True)

        # Добавляем красную полоску снизу
        self.canvas_bottom = tk.Canvas(self, bg="red", height=200)
        self.canvas_bottom.pack(fill="x", expand=True)

    def create_widgets(self):
        self.menu = tk.Menu(self)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.config(menu=self.menu)

        # Основной фрейм
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        # Фрейм для кнопки "Encode Huffman"
        encode_frame = tk.Frame(self.main_frame)
        encode_frame.grid(row=0, column=0, padx=10, pady=10)
        encode_button = tk.Button(encode_frame, text="Encode Huffman", command=lambda: self.on_choice("Encode Huffman"))
        encode_button.pack()

        # Фрейм для кнопки "Decode Huffman"
        decode_frame = tk.Frame(self.main_frame)
        decode_frame.grid(row=0, column=1, padx=10, pady=10)
        decode_button = tk.Button(decode_frame, text="Decode Huffman", command=lambda: self.on_choice("Decode Huffman"))
        decode_button.pack()

        # Фрейм для кнопки "File Info"
        file_info_frame = tk.Frame(self.main_frame)
        file_info_frame.grid(row=0, column=2, padx=10, pady=10)
        file_info_button = tk.Button(file_info_frame, text="File Info", command=lambda: self.on_choice("File Info"))
        file_info_button.pack()

        # Фрейм для кнопки "Delete File"
        delete_frame = tk.Frame(self.main_frame)
        delete_frame.grid(row=0, column=3, padx=10, pady=10)
        delete_button = tk.Button(delete_frame, text="Delete File", command=lambda: self.on_choice("Delete File"))
        delete_button.pack()

        # Фрейм для кнопки "Quit"
        quit_frame = tk.Frame(self.main_frame)
        quit_frame.grid(row=0, column=4, padx=10, pady=10)
        quit_button = tk.Button(quit_frame, text="Quit", command=lambda: self.on_choice("Quit"))
        quit_button.pack()

    def on_choice(self, choice):
        if choice == "Encode Huffman":
            input_file_name = fd.askopenfilename(title="Choose a file to encode")
            if input_file_name:
                with open(input_file_name, "r", encoding="utf-8") as file:
                    text_data = file.read()

                self.huffman_coder.generate_huffman_code(text_data)
                self.huffman_coder.save_huffman_code_to_json()
                mb.showinfo("Success", "Huffman encoding completed.")

        elif choice == "Decode Huffman":
            json_file_path = fd.askopenfilename(title="Choose a JSON file with Huffman code")
            if json_file_path:
                with open(json_file_path, "r", encoding="utf-8") as json_file:
                    huffman_code_json = json_file.read()
                    self.huffman_coder.huffman_code = json.loads(huffman_code_json)

                encoded_file_path = fd.askopenfilename(title="Choose a file with encoded text")
                if encoded_file_path:
                    try:
                        with open(encoded_file_path, "r", encoding="utf-8") as encoded_file:
                            encoded_text = encoded_file.read()

                        decoded_text = self.huffman_coder.decode_huffman(encoded_text)

                        # Вывод декодированного текста
                        mb.showinfo("Decoded Text", decoded_text)

                        save_choice = mb.askyesno("Save File", "Do you want to save the decoded text?")
                        if save_choice:
                            output_file_path = fd.asksaveasfilename(title="Save Decoded Text", defaultextension=".txt")
                            if output_file_path:
                                with open(output_file_path, "w", encoding="utf-8") as output_file:
                                    output_file.write(decoded_text)
                                mb.showinfo("Success", "Decoded text saved to file.")
                    except Exception as e:
                        mb.showerror("Error", f"An error occurred: {str(e)}")


        elif choice == "File Info":
            input_file_path = fd.askopenfilename(title="Choose the original file")
            if input_file_path:
                compressed_file_path = fd.askopenfilename(title="Choose the compressed file")

                original_size = os.path.getsize(input_file_path)
                compressed_size = os.path.getsize(compressed_file_path)
                entropy = calculate_entropy(input_file_path)
                avg_bits_per_symbol = compressed_size * 8 / original_size
                compression_ratio = compressed_size / original_size

                info_str = f"Original Size: {original_size} bytes\n" \
                        f"Compressed Size: {compressed_size} bytes\n" \
                        f"Entropy: {entropy}\n" \
                        f"Avg Bits per Symbol: {avg_bits_per_symbol:.2f} bits\n" \
                        f"Compression Ratio: {compression_ratio:.2%}"

                mb.showinfo("File Info", info_str)

        elif choice == "Delete File":
            folder_to_delete = fd.askdirectory(title="Choose a folder to delete")
            if folder_to_delete:
                try:
                    shutil.rmtree(folder_to_delete)
                    mb.showinfo("Success", "Folder and its contents successfully deleted.")
                except FileNotFoundError:
                    mb.showerror("Error", "Folder not found or unable to delete.")

        elif choice == "Quit":
            self.quit()


if __name__ == "__main__":
    app = HuffmanApp()
    app.mainloop()
