from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path
import sqlite3
import types as typ

## Databases


class AddressDb:

    def __init__(self):
        self.root = Tk()
        self.root.title("Contacts DataBase")
        self.root.iconbitmap('images/sync.ico')
        self.root.geometry("360x600")

        self.db = Path("address_book.db")
        if not self.db.exists():
            self.open_db()
            self.create_table()
            self.close_db
        self.setup_main_window()

    def mainloop(self):
        self.root.mainloop()

    def open_db(self):
        # Create a database or connect to an existing db
        self.connection = sqlite3.connect(self.db)
        # Create cursor
        self.cursor = self.connection.cursor()

    def close_db(self):
        # Commit Changes
        self.connection.commit()
        # Close Connection
        self.connection.close()

    def create_table(self):
        # Create table
        self.cursor.execute(
            """--begin-sql
            CREATE TABLE addresses (
            first_name text,
            last_name text,
            address text,
            city text,
            state text,
            zipcode integer
            )
            ;"""
        )

    def edit_update_entry(self, edit_window, labels, record_id):
        self.open_db()
        self.cursor.execute(
            """UPDATE addresses SET
                    first_name = :first,
                    last_name = :last,
                    address = :address,
                    city = :city,
                    state = :state,
                    zipcode = :zipcode
                    
                    WHERE oid = :oid""",
            {
                'first': labels.first_name.get(),
                'last': labels.last_name.get(),
                'address': labels.address.get(),
                'city': labels.city.get(),
                'state': labels.state.get(),
                'zipcode': labels.zipcode.get(),
                'oid': record_id,
            },
        )
        self.close_db()
        edit_window.destroy()

    def edit(self):

        def update_entry():
            self.open_db()

        self.open_db()
        record_id = self.delete_box.get()
        self.cursor.execute(f"SELECT oid FROM addresses")
        oids = self.cursor.fetchall()
        print(f"oids = {oids}")
        try:
            rec_int = int(record_id)
        except ValueError:
            rec_int = 0
        if not (rec_int, ) in oids:
            new_label = Label(self.root, text=f"{record_id} is not a valid record ID, cannot edit", foreground="#440044")
            new_label.grid(row=11, column=0, columnspan=2)
            return False

        # Edit function to create a window and edit a given record
        ed = typ.SimpleNamespace()
        ed.win = Tk()
        ed.win.title("Update A Record")
        ed.win.iconbitmap("images/sync.ico")
        ed.win.geometry("320x240")

        ed.labels = self.setup_labels(ed.win)
        # Create Save Button
        ed.save_button = Button(ed.win, text="Save Edited Record", command=lambda: self.edit_update_entry(ed.win, ed.labels, record_id))
        ed.save_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=92)
        # Create Cancel Button
        ed.cancel_button = Button(ed.win, text="Cancel", command=ed.win.destroy)
        ed.cancel_button.grid(row=7, column=0, columnspan=2, pady=(0, 10), padx=10, ipadx=124)

        self.open_db()
        self.cursor.execute(f"SELECT * FROM addresses WHERE oid = {record_id}")
        records = self.cursor.fetchall()
        for record in records:
            ed.labels.first_name.insert(0, record[0])
            ed.labels.last_name.insert(0, record[1])
            ed.labels.address.insert(0, record[2])
            ed.labels.city.insert(0, record[3])
            ed.labels.state.insert(0, record[4])
            ed.labels.zipcode.insert(0, record[5])
        self.close_db()

    def delete(self):
        self.open_db()
        print(f'delete_box entry is: "{self.delete_box.get()}"')
        self.cursor.execute(f"DELETE from addresses WHERE oid = {str(self.delete_box.get())}")
        self.close_db()

    def query(self):
        self.open_db()
        self.cursor.execute("SELECT oid, * FROM addresses")
        records = self.cursor.fetchall()
        print(records)

        records_str = []
        for record in records:
            records_str.append(  #
                f'Entry ID: {record[0]}, Name: {record[1]} {record[2]}\n'
                f'Address: {record[3]}, {record[4]}, {record[5]} {record[6]}'
            )
        print_records = '\n'.join(records_str)

        self.query_label = Label(self.root, text=print_records, justify=LEFT, background="#AAFFFF")
        self.query_label.grid(row=11, column=0, columnspan=2)
        self.close_db()

    def submit(self, labels):
        self.cursor.execute(
            "INSERT INTO addresses VALUES (:first_name, :last_name, :address, :city, :state, :zipcode)",
            {
                "first_name": labels.first_name.get(),
                "last_name": labels.last_name.get(),
                "address": labels.address.get(),
                "city": labels.city.get(),
                "state": labels.state.get(),
                "zipcode": labels.zipcode.get(),
            },
        )

    def submit_new_entry(self):
        # Create Submit function for database
        self.open_db()
        try:
            self.submit(self.root_labels)
        except sqlite3.OperationalError as ex:
            if str(ex) == "no such table: addresses":
                self.create_table()
                self.submit(self.root_labels)
            else:
                raise
        self.close_db()
        self.clear_text_boxes(self.root_labels)

    def clear_text_boxes(self, labels):
        # Clear the text boxes
        labels.first_name.delete(0, END)
        labels.last_name.delete(0, END)
        labels.address.delete(0, END)
        labels.city.delete(0, END)
        labels.state.delete(0, END)
        labels.zipcode.delete(0, END)

    def setup_labels(self, window, rowoff=0, coloff=0):
        labels = typ.SimpleNamespace()
        labels.first_name = Entry(window, width=30)
        labels.first_name.grid(row=rowoff + 0, column=coloff + 1, padx=20, pady=(10, 0))
        labels.last_name = Entry(window, width=30)
        labels.last_name.grid(row=rowoff + 1, column=coloff + 1)
        labels.address = Entry(window, width=30)
        labels.address.grid(row=rowoff + 2, column=coloff + 1)
        labels.city = Entry(window, width=30)
        labels.city.grid(row=rowoff + 3, column=coloff + 1)
        labels.state = Entry(window, width=30)
        labels.state.grid(row=rowoff + 4, column=coloff + 1)
        labels.zipcode = Entry(window, width=30)
        labels.zipcode.grid(row=rowoff + 5, column=coloff + 1)

        # Create Text Box Labels
        labels.first_name_label = Label(window, text="First Name")
        labels.first_name_label.grid(row=rowoff + 0, column=coloff + 0, pady=(10, 0))
        labels.last_name_label = Label(window, text="Last Name")
        labels.last_name_label.grid(row=rowoff + 1, column=coloff + 0)
        labels.address_label = Label(window, text="Address")
        labels.address_label.grid(row=rowoff + 2, column=coloff + 0)
        labels.city_label = Label(window, text="City")
        labels.city_label.grid(row=rowoff + 3, column=coloff + 0)
        labels.state_label = Label(window, text="State")
        labels.state_label.grid(row=rowoff + 4, column=coloff + 0)
        labels.zipcode_label = Label(window, text="Zipcode")
        labels.zipcode_label.grid(row=rowoff + 5, column=coloff + 0)

        return labels

    def setup_main_window(self):
        self.root_labels = self.setup_labels(self.root)

        self.delete_box = Entry(self.root, width=30)
        self.delete_box.grid(row=8, column=1)

        self.delete_box_label = Label(self.root, text="Select ID #")
        self.delete_box_label.grid(row=8, column=0, pady=(10, 0))

        # Create Submit Button
        self.submit_button = Button(self.root, text="Add Record To Database", command=self.submit_new_entry)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Create Query  Button
        self.query_button = Button(self.root, text="Show Records", command=self.query)
        self.query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=128)

        # Create a Delete Button
        self.delete_button = Button(self.root, text="Delete Record", command=self.delete)
        self.delete_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=126)

        # Create and edit Button
        self.edit_button = Button(self.root, text="Edit Record", command=self.edit)
        self.edit_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=132)


def main():
    contacts = AddressDb()
    contacts.mainloop()


if __name__ == "__main__":
    main()
