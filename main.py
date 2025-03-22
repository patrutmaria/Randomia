import requests
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import random

class APIClient:
    def __init__(self):
        self.base_url_posts = "https://jsonplaceholder.typicode.com/posts"
        self.base_url_users = "https://jsonplaceholder.typicode.com/users"
        self.cat_api_url = "https://api.thecatapi.com/v1/images/search"
        self.joke_api_url = "https://v2.jokeapi.dev/joke/Any"

    def fetch_posts(self):
        try:
            response = requests.get(self.base_url_posts)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch posts: {e}")
            return []

    def fetch_users(self):
        try:
            response = requests.get(self.base_url_users)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch users: {e}")
            return []

    def fetch_joke(self):
        try:
            response = requests.get(self.joke_api_url)
            response.raise_for_status()
            data = response.json()
            if "joke" in data:
                return data["joke"]
            else:
                return f"{data['setup']} - {data['delivery']}"
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch joke: {e}")
            return None

    def fetch_cat_image(self):
        try:
            response = requests.get(self.cat_api_url)
            response.raise_for_status()
            return response.json()[0]['url']
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch cat image: {e}")
            return None

    def fetch_random_fact(self):
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
            "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
            "Bananas are berries, but strawberries aren't. According to botanical definitions, bananas qualify as berries, while strawberries do not.",
            "A group of flamingos is called a 'flamboyance'.",
            "Sharks existed before trees. Sharks have been around for more than 400 million years, while the first trees appeared around 350 million years ago."
        ]
        return random.choice(facts)

class APIClientGUI:
    def __init__(self, root):
        self.client = APIClient()
        self.root = root
        self.root.title("API Client GUI")
        self.root.geometry("400x400")  # Set a larger window size
        
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select an action", font=("Arial", 18))  # Increased font size
        self.label.pack(pady=20)  # Added more padding

        self.show_users_btn = tk.Button(self.root, text="Show Users", font=("Arial", 14), command=self.show_users)
        self.show_users_btn.pack(pady=10)

        self.show_posts_btn = tk.Button(self.root, text="Show Posts", font=("Arial", 14), command=self.show_posts)
        self.show_posts_btn.pack(pady=10)
        
        self.fetch_joke_btn = tk.Button(self.root, text="Get a Joke", font=("Arial", 14), command=self.show_joke)
        self.fetch_joke_btn.pack(pady=10)
        
        self.fetch_fact_btn = tk.Button(self.root, text="Get a Random Fact", font=("Arial", 14), command=self.show_random_fact)
        self.fetch_fact_btn.pack(pady=10)
        
        self.show_cat_btn = tk.Button(self.root, text="Show Random Cat", font=("Arial", 14), command=self.show_cat)
        self.show_cat_btn.pack(pady=10)

    def show_joke(self):
        joke = self.client.fetch_joke()
        if joke:
            messagebox.showinfo("Joke", joke)

    def show_random_fact(self):
        fact = self.client.fetch_random_fact()
        messagebox.showinfo("Random Fact", fact)

    def show_users(self):
        users = self.client.fetch_users()
        if not users:
            return

        top = tk.Toplevel(self.root)
        top.title("Users List")
        
        tree = ttk.Treeview(top, columns=("ID", "Name", "Email"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        
        for user in users:
            tree.insert("", tk.END, values=(user["id"], user["name"], user["email"]))
        
        tree.pack()
    
    def show_posts(self):
        posts = self.client.fetch_posts()
        if not posts:
            return

        top = tk.Toplevel(self.root)
        top.title("Posts List")
        
        text = tk.Text(top, wrap="word")
        for post in posts[:10]:
            text.insert(tk.END, f"ID: {post['id']}\nTitle: {post['title']}\nBody: {post['body']}\n\n")
        text.pack()
    
    def show_cat(self):
        url = self.client.fetch_cat_image()
        if url:
            image = Image.open(requests.get(url, stream=True).raw)
            image = image.resize((300, 300))
            img = ImageTk.PhotoImage(image)

            top = tk.Toplevel(self.root)
            top.title("Random Cat")
            tk.Label(top, image=img).pack()
            top.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = APIClientGUI(root)
    root.mainloop()