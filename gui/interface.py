import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from models.medicine_list import MedicineList
from models.medicine import Medicine
from tkinter import messagebox
import tkinter as tk
import json
import os

class PharmacyAppInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Облік ліків")

        # Розміри головного вікна та його позиція
        window_width = 900
        window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Встановлюємо тему для всього додатку
        self.root.style = ttk.Style("cosmo")
        self.root.configure(bg="#4B0082")  # Фон

        self.medicine_list = MedicineList()
        self.load_medicines_from_file()
        self.init_main_menu()

    def load_medicines_from_file(self):
        # Завантажуємо дані про ліки з файлу, якщо він існує
        if os.path.exists("medicines.json"):
            with open("medicines.json", "r", encoding="utf-8") as f:
                medicines_data = json.load(f)
            self.medicine_list.medicines = [
                Medicine(
                    name=med["name"],
                    quantity=med["quantity"],
                    price=med["price"],
                    description=med.get("description", "Опис відсутній")
                ) for med in medicines_data
            ]
        else:
            self.medicine_list.medicines = []

    def save_medicines_to_file(self):
        # Зберігаємо дані про ліки у файл
        medicines_data = [
            {
                "name": med.name,
                "quantity": med.quantity,
                "price": med.price,
                "description": med.description
            } for med in self.medicine_list.get_medicines()
        ]
        with open("medicines.json", "w", encoding="utf-8") as f:
            json.dump(medicines_data, f, indent=4, ensure_ascii=False)

    def init_main_menu(self):
        # Ініціалізація головного меню
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = ttk.Label(self.root, text="Облік ліків", font=("Calibri", 30, "bold"), foreground="white", background="#4B0082")
        title_label.pack(pady=20)

        style = ttk.Style()
        style.configure('Custom.TButton', font=('Calibri', 16, 'bold'))
        style.configure('Exit.TButton', font=('Calibri', 16, 'bold'), background='red')

        buttons_info = [
            ("Склад", self.open_stock_page, PRIMARY),
            ("Замовлення", self.open_order_page, PRIMARY),
            ("Вийти", self.root.quit, DANGER)
        ]

        for text, command, bootstyle in buttons_info:
            style_name = 'Exit.TButton' if text == "Вийти" else 'Custom.TButton'
            button = ttk.Button(self.root, text=text, command=command, bootstyle=bootstyle, style=style_name)
            button.pack(pady=10, ipadx=20, ipady=15)

    def open_stock_page(self):
        # Відкриваємо сторінку "Склад"
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = ttk.Label(self.root, text="Склад", font=("Arial", 18, "bold"), foreground="white", background="#4B0082")
        title_label.pack(pady=10)

        search_frame = ttk.Frame(self.root, style="TFrame")
        search_frame.pack(fill="x", padx=10, pady=5)
        
        search_entry = ttk.Entry(search_frame, foreground="gray")
        search_entry.insert(0, "Пошук")
        search_entry.pack(side="left", fill="x", expand=True)

        # Обробники для пошуку
        def on_focus_in(event):
            if search_entry.get() == "Пошук":
                search_entry.delete(0, "end")
                search_entry.config(foreground="black")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Пошук")
                search_entry.config(foreground="gray")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        search_entry.bind("<KeyRelease>", lambda event: self.search_medicine(search_entry.get()))

        table_frame = ttk.Frame(self.root, style="TFrame")
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.stock_table = ttk.Treeview(table_frame, columns=("name", "quantity", "price", "description"), show="headings", bootstyle=INFO)
        self.stock_table.heading("name", text="Назва")
        self.stock_table.heading("quantity", text="Кількість (шт)")
        self.stock_table.heading("price", text="Ціна (грн)")
        self.stock_table.heading("description", text="Опис")

        self.stock_table.column("name", width=200, anchor="center")
        self.stock_table.column("quantity", width=100, anchor="center")
        self.stock_table.column("price", width=100, anchor="center")
        self.stock_table.column("description", width=600, anchor="w")

        self.stock_table.pack(fill="both", expand=True)
        
        self.stock_table.bind("<Double-1>", self.edit_item)

        self.load_medicines_to_table()

        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.pack(side="bottom", fill="x", pady=(0, 10))

        add_button = ttk.Button(button_frame, text="Додати", bootstyle=(SUCCESS, OUTLINE), command=self.add_medicine_row)
        add_button.pack(side="left", padx=10)

        delete_button = ttk.Button(button_frame, text="Видалити", bootstyle=(DANGER, OUTLINE), command=self.delete_selected_rows)
        delete_button.pack(side="left", padx=10)

        replenish_button = ttk.Button(button_frame, text="Замовлення приїхало", bootstyle=(PRIMARY, OUTLINE), command=self.replenish_stock_from_order)
        replenish_button.pack(side="left", padx=10)

        back_button = ttk.Button(button_frame, text="Назад", bootstyle=(PRIMARY, OUTLINE), command=self.init_main_menu)
        back_button.pack(side="right", padx=10)

    def load_medicines_to_table(self):
        # Завантажуємо ліки в таблицю
        self.stock_table.delete(*self.stock_table.get_children())
        for medicine in self.medicine_list.get_medicines():
            self.stock_table.insert("", "end", values=(medicine.name, medicine.quantity, medicine.price, medicine.description))

    def search_medicine(self, query):
        # Пошук ліків за запитом
        filtered_medicines = [med for med in self.medicine_list.get_medicines() if query.lower() in med.name.lower()]
        self.stock_table.delete(*self.stock_table.get_children())
        for medicine in filtered_medicines:
            self.stock_table.insert("", "end", values=(medicine.name, medicine.quantity, medicine.price, medicine.description))

    def add_medicine_row(self):
        # Вікно для додавання нового запису ліків
        new_medicine_window = ttk.Toplevel(self.root)
        new_medicine_window.title("Додати ліки")
        new_medicine_window.configure(bg="#4B0082")
        new_medicine_window.geometry("500x200")
        
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        new_medicine_window.geometry(f"+{x}+{y}")

        new_medicine_window.grab_set()
        new_medicine_window.focus_set()

        ttk.Label(new_medicine_window, text="Назва:", background="#4B0082", foreground="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = ttk.Entry(new_medicine_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(new_medicine_window, text="Кількість (шт):", background="#4B0082", foreground="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        quantity_entry = ttk.Entry(new_medicine_window)
        quantity_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(new_medicine_window, text="Ціна:", background="#4B0082", foreground="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        price_entry = ttk.Entry(new_medicine_window)
        price_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(new_medicine_window, text="Опис:", background="#4B0082", foreground="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        description_entry = tk.Text(new_medicine_window, height=4, width=40)
        description_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Збереження нового запису ліків
        def save_medicine():
            name = name_entry.get()
            quantity = quantity_entry.get()
            price = price_entry.get()
            description = description_entry.get("1.0", "end").strip()
            if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
                self.medicine_list.add_medicine(name, int(quantity), float(price), description)
                self.save_medicines_to_file()
                self.load_medicines_to_table()
                new_medicine_window.destroy()
            else:
                messagebox.showerror("Помилка", "Будь ласка, корректно заповніть усі поля!", parent=new_medicine_window)

        save_button = ttk.Button(new_medicine_window, text="Зберегти", bootstyle=SUCCESS, command=save_medicine)
        save_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

    def add_medicine_to_order(self):
        add_order_window = ttk.Toplevel(self.root)
        add_order_window.title("Додати товар в замовлення")
        add_order_window.geometry("400x250")
        add_order_window.configure(bg="#4B0082")

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        add_order_window.geometry(f"+{x}+{y}")

        add_order_window.grab_set()
        add_order_window.focus_set()

        ttk.Label(add_order_window, text="Оберіть товар:", background="#4B0082", foreground="white").pack(pady=10)
        selected_medicine = tk.StringVar(add_order_window)
        available_medicines = [med for med in self.medicine_list.get_medicines()]
        if not available_medicines:
            messagebox.showerror("Помилка", "Немає товарів для додавання в замовлення.")
            add_order_window.destroy()
            return

        medicine_menu = ttk.OptionMenu(add_order_window, selected_medicine, available_medicines[0].name, *[med.name for med in available_medicines])
        medicine_menu.pack(pady=5)

        ttk.Label(add_order_window, text="Кількість (шт)", background="#4B0082", foreground="white").pack(pady=10)
        quantity_entry = ttk.Entry(add_order_window)
        quantity_entry.pack(pady=5)

        def confirm_addition():
            name = selected_medicine.get()
            quantity = quantity_entry.get()
            if quantity.isdigit():
                quantity = int(quantity)
                current_qty = next((med.quantity for med in available_medicines if med.name == name), "Не визначено")
                self.order_table.insert("", "end", values=(name, current_qty, quantity))
                add_order_window.destroy()
            else:
                messagebox.showerror("Помилка", "Введіть коректну кількість.")

        confirm_button = ttk.Button(add_order_window, text="Додати", command=confirm_addition, bootstyle=SUCCESS)
        confirm_button.pack(pady=10)

    def edit_item(self, event):
        selected_item = event.widget.selection()
        if not selected_item:
            return

        item = event.widget.item(selected_item)
        values = item["values"]

        if hasattr(self, 'stock_table') and event.widget == self.stock_table:
            self.open_full_edit_window(values)  # Відкриває інтерфейс для повної зміни
        elif hasattr(self, 'order_table') and event.widget == self.order_table:
            self.open_quantity_edit_window(values)  # Відкиває інтерфейс для зміни кількості

    def open_full_edit_window(self, values):
        name, quantity, price, description = values

        edit_window = ttk.Toplevel(self.root)
        edit_window.title("Редагувати ліки (Повне)")
        edit_window.geometry("370x250")
        edit_window.configure(bg="#4B0082")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        edit_window.geometry(f"+{x}+{y}")

        edit_window.grab_set()
        edit_window.focus_set()

        ttk.Label(edit_window, text="Назва:", background="#4B0082", foreground="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(edit_window, text="Кількість (шт)", background="#4B0082", foreground="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        quantity_entry = ttk.Entry(edit_window)
        quantity_entry.insert(0, quantity)
        quantity_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(edit_window, text="Ціна:", background="#4B0082", foreground="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        price_entry = ttk.Entry(edit_window)
        price_entry.insert(0, price)
        price_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(edit_window, text="Опис:", background="#4B0082", foreground="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        description_entry = tk.Text(edit_window, height=4, width=40)
        description_entry.insert("1.0", description)
        description_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def save_full_changes():
            new_name = name_entry.get()
            new_quantity = quantity_entry.get()
            new_price = price_entry.get()
            new_description = description_entry.get("1.0", "end").strip()

            if new_quantity.isdigit() and new_price.replace('.', '', 1).isdigit():
                new_quantity = int(new_quantity)
                new_price = float(new_price)
                for medicine in self.medicine_list.get_medicines():
                    if medicine.name == name:
                        medicine.name = new_name
                        medicine.quantity = new_quantity
                        medicine.price = new_price
                        medicine.description = new_description
                        break
                self.save_medicines_to_file()
                self.load_medicines_to_table()
                edit_window.destroy()
            else:
                messagebox.showerror("Помилка", "Будь ласка, введіть коректні значення.")

        save_button = ttk.Button(edit_window, text="Зберегти", bootstyle=SUCCESS, command=save_full_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

    def open_quantity_edit_window(self, values):
        name, current_qty, order_qty = values

        edit_window = ttk.Toplevel(self.root)
        edit_window.title("Редагувати кількість для замовлення (шт)")
        edit_window.geometry("344x170")
        edit_window.configure(bg="#4B0082")

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
        edit_window.geometry(f"+{x}+{y}")

        edit_window.grab_set()
        edit_window.focus_set()

        ttk.Label(edit_window, text="Назва:", background="#4B0082", foreground="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(edit_window, text=name, background="#4B0082", foreground="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(edit_window, text="Кількість для замовлення (шт):", background="#4B0082", foreground="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        quantity_entry = ttk.Entry(edit_window)
        quantity_entry.insert(0, order_qty)
        quantity_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        def save_quantity_changes(selected_item):
            new_order_qty = quantity_entry.get()
            if new_order_qty.isdigit():
                new_order_qty = int(new_order_qty)
                self.order_table.item(selected_item, values=(name, current_qty, new_order_qty))
                edit_window.destroy()
            else:
                messagebox.showerror("Помилка", "Введіть корректну кількість!", parent=edit_window)

        save_button = ttk.Button(edit_window, text="Зберегти", bootstyle=SUCCESS, command=lambda: save_quantity_changes(self.order_table.selection()))
        save_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        def delete_item():
            selected_item = self.order_table.selection()
            if selected_item:
                self.order_table.delete(selected_item)
                edit_window.destroy()

        delete_button = ttk.Button(edit_window, text="Видалити", bootstyle=DANGER, command=delete_item)
        delete_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

    def delete_selected_rows(self):
        selected_items = self.stock_table.selection()
        if not selected_items:
            messagebox.showwarning("Попередження", "Виберіть рядок для видалення")
        else:
            for item in selected_items:
                item_values = self.stock_table.item(item, "values")
                item_name = item_values[0]
                for idx, medicine in enumerate(self.medicine_list.get_medicines()):
                    if medicine.name == item_name:
                        self.medicine_list.remove_medicine(idx)
                        break
                self.stock_table.delete(item)
            self.save_medicines_to_file()

    def open_order_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = ttk.Label(self.root, text="Замовлення", font=("Arial", 18, "bold"), foreground="white", background="#4B0082")
        title_label.pack(pady=10)

        order_table_frame = ttk.Frame(self.root, style="TFrame")
        order_table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.order_table = ttk.Treeview(order_table_frame, columns=("name", "current_qty", "order_qty"), show="headings", bootstyle=INFO)
        self.order_table.heading("name", text="Назва")
        self.order_table.heading("current_qty", text="Кількість на складі")
        self.order_table.heading("order_qty", text="Кількість для замовлення")

        self.order_table.column("name", width=200, anchor="center")
        self.order_table.column("current_qty", width=150, anchor="center")
        self.order_table.column("order_qty", width=150, anchor="center")

        self.order_table.pack(fill="both", expand=True)
        self.load_order_table()

        confirm_order_button = ttk.Button(self.root, text="Підтвердити замовлення", bootstyle=SUCCESS, command=self.confirm_order)
        confirm_order_button.pack(pady=5)

        add_to_order_button = ttk.Button(self.root, text="Додати товар в замовлення", bootstyle=PRIMARY, command=self.add_medicine_to_order)
        add_to_order_button.pack(pady=5)

        back_button = ttk.Button(self.root, text="Назад", bootstyle=PRIMARY, command=self.init_main_menu)
        back_button.pack(pady=5)

        self.order_table.bind("<Double-1>", self.edit_item)

    def load_order_table(self):
        self.order_table.delete(*self.order_table.get_children())
        for medicine in self.medicine_list.get_medicines():
            if medicine.quantity < 15:
                self.order_table.insert("", "end", values=(medicine.name, medicine.quantity, 15 - medicine.quantity))

    def confirm_order(self):
        items = self.order_table.get_children()
        orders = []
        for item in items:
            name, current_qty, order_qty = self.order_table.item(item, "values")
            order_qty = int(order_qty) if str(order_qty).isdigit() else 0
            if order_qty > 0:
                orders.append({"name": name, "current_qty": current_qty, "order_qty": order_qty})

        if orders:
            with open("orders.json", "w", encoding="utf-8") as f:
                json.dump(orders, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Замовлення підтверджено", "Замовлення успішно збережено.")
        else:
            messagebox.showwarning("Попередження", "Будь ласка, введіть кількість для замовлення.")

    def replenish_stock_from_order(self):
        if not os.path.exists("orders.json"):
            messagebox.showinfo("Інформація", "Немає доступних замовлень для поповнення.")
            return

        with open("orders.json", "r", encoding="utf-8") as file:
            orders = json.load(file)

        for order in orders:
            name = order["name"]
            order_qty = int(order["order_qty"])

            for medicine in self.medicine_list.get_medicines():
                if medicine.name == name:
                    medicine.quantity += order_qty
                    break
            else:
                self.medicine_list.add_medicine(name, order_qty, 0)

        self.save_medicines_to_file()
        self.load_medicines_to_table()
        os.remove("orders.json")
        messagebox.showinfo("Інформація", "Склад успішно поповнено згідно з замовленням.")

        if __name__ == "__main__":
            root = tk.Tk()
            app = PharmacyAppInterface(root)
            root.mainloop()