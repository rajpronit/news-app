import io
import webbrowser
from dotenv import dotenv_values
import requests
import pyttsx3
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image

class NewsApp:
    config = dotenv_values(".env")

    def load_gui(self):
        self.root = Tk()
        self.root.geometry("425x600")
        self.root.resizable(0, 0)
        self.root.title('News App')
        self.root.configure(background='black')

        self.show_categories()  # Show the categories on startup

        self.root.mainloop()

    def __init__(self):
        self.load_gui()  # Initialize and show the GUI

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def read_news(self, headline):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')      
        engine.setProperty('voice', voices[0].id) 
        engine.say(headline)
        engine.runAndWait()

    def show_categories(self):
        # Create category buttons
        self.clear()  # Clear any existing content

        self.newsCatButton = []
        self.newsCat = ["general", "entertainment", "business", "sports", "technology", "health","Music"]
        bg_color = "#404040"
        basic_font_color = "#ccc4c4"

        self.F1 = LabelFrame(self.root, text="Category", font=("times new roman", 20, "bold"), bg=bg_color, fg=basic_font_color, bd=10, relief=GROOVE)
        self.F1.place(x=0, y=0, width=500, relheight=1)

        for i in range(len(self.newsCat)):
            b = Button(self.F1, text=self.newsCat[i].upper(), width=30, bd=9, font="arial 15 bold",
                       command=lambda cat=self.newsCat[i]: self.load_news(cat))
            b.grid(row=i, column=0, padx=10, pady=5)
            self.newsCatButton.append(b)

    def load_news(self, category):
        # Clear the screen and hide the category frame
        self.F1.place_forget()

        # Fetch news data based on the selected category
        try:
            data = requests.get(f'https://newsapi.org/v2/everything?q={category+"+india"}&apiKey={self.config.get("API_KEY")}').json()
            newdata = data['articles']
            filtered_articles = [
                article for article in newdata
                if article.get('author') is not None 
                and article.get('author') != '[Removed]'
                and article.get('title') is not None and article.get('title') != '[Removed]'
                and article.get('description') is not None and article.get('description') != '[Removed]'
            ]

            self.data = filtered_articles

            if self.data:
                self.load_news_item(0)
            else:
                self.display_message("No articles with images available for this category.")

        except Exception as e:
            self.display_message(f"Error fetching news: {e}")

    def display_message(self, message):
        self.clear()
        msg_label = Label(self.root, text=message, bg='black', fg='white', wraplength=350, justify='center')
        msg_label.pack(pady=(200, 20))
        msg_label.config(font=('arial black', 15))

        # Add a back button to return to category selection
        back_btn = Button(self.root, text='Back to Categories', width=16, height=3, command=self.show_categories)
        back_btn.pack(pady=20)

    def load_news_item(self, index):
        self.clear()

        try:
            img_url = self.data[index]['urlToImage']
            raw = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw)).resize((424, 250))
            photo = ImageTk.PhotoImage(im)
           

        except Exception as e:
            raw = urlopen("https://dzinejs.lv/wp-content/plugins/lightbox/images/No-image-found.jpg").read()
            im = Image.open(io.BytesIO(raw)).resize((424, 250))
            photo = ImageTk.PhotoImage(im)
           
       
        # Back button at the top left corner
        back_frame = Frame(self.root, bg='black')
        back_frame.pack(anchor='nw', pady=5, padx=3)
        back_btn = Button(back_frame, text='Back', command=self.show_categories)
        back_btn.pack(side=LEFT) 
       
        back_btn = Button(back_frame, text='Read', command=lambda: self.read_news(self.data[index]['title']))
        back_btn.pack(side=RIGHT, padx=8)

        label = Label(self.root, image=photo)
        label.pack(pady=(0, 10))

        heading = Label(self.root, text=self.data[index]['title'][:83], bg='black', fg='white', wraplength=380, justify='center')
        heading.pack(pady=(8, 18))
        heading.config(font=('arial black', 15))

        details = Label(self.root, text=self.data[index]['description'][:150], bg='black', fg='white', wraplength=380, justify='center',)
        details.pack(pady=(20, 20) )
        details.config(font=('arial black', 10))

        frame = Frame(self.root, bg='black')
        frame.pack(expand=TRUE, fill=BOTH)

        if index != 0:
            prev = Button(frame, text='Prev', width=19, height=3, command=lambda: self.load_news_item(index - 1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=19, height=3, command=lambda: self.open_link(self.data[index]['url']))
        read.pack(side=LEFT)
        

        if index != len(self.data) - 1:
            next = Button(frame, text='Next', width=19, height=3, command=lambda: self.load_news_item(index + 1))
            next.pack(side=LEFT)

        # Keep a reference to the image to avoid garbage collection
        label.image = photo

    def open_link(self, url):
        webbrowser.open(url)


# Instantiate the NewsApp class
obj = NewsApp()
