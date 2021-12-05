from tkinter import LabelFrame, ttk
import tkinter as tk
import sqlite3


class Window:
  """Represents the window of the application where users can register, edit and delete products."""

 # Path to the database file
  DATABASE_PATH = "database.db"

  def __init__(self, window):
    """Creates the main window and its widgets."""
    self.window = window
    self.window.title("Products App")

    # Creating the Registry frame container
    frame_registry = LabelFrame(self.window, text = "Register a new product")
    frame_registry.grid(row = 0, column = 0, columnspan = 3, pady = 20)

    # Creating the name input
    label_name = tk.Label(frame_registry, text = "Name: ")
    label_name.grid(row = 1, column = 0)
    self.name = tk.Entry(frame_registry)
    self.name.focus()
    self.name.grid(row = 1, column = 1)

    # Creating the price input
    label_price = tk.Label(frame_registry, text = "Price: ")
    label_price.grid(row = 2, column = 0)
    self.price = tk.Entry(frame_registry)
    self.price.grid(row = 2, column = 1)

    # Button for ADDING a product
    button_add = ttk.Button(frame_registry, text = "Add product", command = self.add_product)
    button_add.grid(row = 3, columnspan = 2, sticky = tk.W + tk.E)

    # Message for notification about an operation
    self.message = tk.Label(text = "")
    self.message.grid(row = 3, column = 0, columnspan = 2, sticky = tk.W + tk.E)

    # List of products
    self.treeview_list = ttk.Treeview(height = 10, column = 2)
    self.treeview_list.grid(row = 4, column = 0, columnspan = 2)
    self.treeview_list.heading("#0", text = "Name", anchor = tk.CENTER)
    self.treeview_list.heading("#1", text = "Price", anchor = tk.CENTER)

    # Buttons for DELETING and EDITING a product

    # Delete
    button_delete = ttk.Button(text = "Delete", command = self.delete_product)
    button_delete.grid(row = 5, column = 0, sticky = tk.W + tk.E)
    # Edit
    button_edit = ttk.Button(text = "Edit", command = self.edit_product)
    button_edit.grid(row = 5, column = 1, sticky = tk.W + tk.E)

    # Calling the query to get all the products
    self.get_all_products()

  def run_query(self, query, params = ()):
    """Makes a connection to the database and executes the query, along with its parameters if given."""
    with sqlite3.connect(self.DATABASE_PATH) as conn:
      cursor = conn.cursor()
      result = cursor.execute(query, params)
      conn.commit()
    return result

  def get_all_products(self):
    """Executes the query to retrieve all products from the database."""

    # Check if treeview_list is empty
    if self.treeview_list.get_children():
      records = self.treeview_list.get_children()
      # Cleaning the treeview_list
      for record in records:
        self.treeview_list.delete(record)

    # Executing the query to get all products
    query = "SELECT * FROM PRODUCTS ORDER BY NAME DESC"
    db_rows = self.run_query(query)
    for row in db_rows:
      print(row)
      self.treeview_list.insert("", 0, text = row[1].title(), values = row[2])

  def validate_inputs(self):
    """Validates if the name and price input are not empty."""
    return len(self.name.get()) > 0 and len(self.price.get()) > 0

  def add_product(self):
    """Executes the query to add a new product with the name and price given by the user."""
    self.message["text"] = ""
    if self.validate_inputs():
      query = "INSERT INTO PRODUCTS VALUES(NULL, ?, ?)"
      params = (self.name.get().lower(), self.price.get())
      self.run_query(query, params)
      self.message["text"] = "New {} was saved!".format(self.name.get())
      self.message["fg"] = "green"
      self.name.delete(0, tk.END)
      self.price.delete(0, tk.END)
    else:
      self.message["text"] = "Name and price are requiered."
      self.message["fg"] = "red"
    self.get_all_products()

  def delete_product(self):
    """Executes the query to delete a product"""
    self.message["text"] = ""
    try:
      self.treeview_list.item(self.treeview_list.selection())["text"][0]
    except IndexError:
      self.message["text"] = "Please select a product"
      self.message["fg"] = "red"
      return
    else:
      product_name = self.treeview_list.item(self.treeview_list.selection())["text"]
      query = "DELETE FROM PRODUCTS WHERE NAME = ?"
      self.run_query(query, (product_name.lower(), ))
      self.message["text"] = "Product {} was deleted succesfully".format(product_name.title())
      self.message["fg"] = "green"
      self.get_all_products()

  def edit_product(self):
    """Validates if user has selected a product to edit. If so, opens a new window to edit that product"""
    self.message["text"] = ""
    try:
      self.treeview_list.item(self.treeview_list.selection())["text"][0]
    except IndexError:
      self.message["text"] = "Please select a product"
      self.message["fg"] = "red"
      return
    else:
      old_name = self.treeview_list.item(self.treeview_list.selection())["text"]
      old_price = self.treeview_list.item(self.treeview_list.selection())["values"][0]
      self.editing_window = tk.Toplevel()
      self.editing_window.title("Edit product")

      # --- New window for editing ---

      # - Old name -
      # Label
      label_old_name = tk.Label(self.editing_window, text="Old name: ")
      label_old_name.grid(row = 0, column = 1)
      # Entry
      entry_old_name = tk.Entry(self.editing_window, textvariable = tk.StringVar(self.editing_window, value = old_name), state = "readonly")
      entry_old_name.grid(row = 0, column = 2)

      # - New name -
      # Label
      label_new_name = tk.Label(self.editing_window, text = "New name: ")
      label_new_name.grid(row = 1, column = 1)
      # Entry
      entry_new_name = tk.Entry(self.editing_window)
      entry_new_name.grid(row = 1, column = 2)

      # - Old price -
      # Label
      label_old_price = tk.Label(self.editing_window, text = "Old price: ")
      label_old_price.grid(row = 2, column = 1)
      # Entry
      entry_old_price = tk.Entry(self.editing_window, textvariable = tk.StringVar(self.editing_window, value = old_price), state = "readonly")
      entry_old_price.grid(row = 2, column = 2)

      # - New price -
      # Label
      label_new_price = tk.Label(self.editing_window, text = "New price: ")
      label_new_price.grid(row = 3, column = 1)
      # Entry
      entry_new_price = tk.Entry(self.editing_window)
      entry_new_price.grid(row = 3, column = 2)
      
      # - Button to update -
      button_update = ttk.Button(self.editing_window, text = "Update", command = lambda: self.update_record(old_name.lower(), 
      entry_new_name.get().lower(), old_price, entry_new_price.get()))
      button_update.grid(row = 4, column = 2, sticky = tk.W)

  def update_record(self, old_name, new_name, old_price, new_price):
    """Executes the query to update the product with the new name and price"""
    query = "UPDATE PRODUCTS SET NAME = ?, PRICE = ? WHERE NAME = ? AND PRICE = ?"
    params = (new_name, new_price, old_name, old_price)
    self.run_query(query, params)
    self.editing_window.destroy()
    self.message["text"] = "Product {} updated succesfully".format(old_name)
    self.message["fg"] = "green"
    self.get_all_products()


"""Executes the application"""
if __name__ == "__main__":
  window = tk.Tk()
  application = Window(window)
  window.mainloop()