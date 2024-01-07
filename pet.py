from tkinter import HIDDEN, NORMAL, Tk, Canvas, Toplevel, Label, Button, Listbox, Scrollbar, END, SINGLE, filedialog, ttk, PhotoImage
import webbrowser
import subprocess
from pygame import mixer
import pyjokes
import os
from PIL import Image, ImageTk

def toggle_eyes():
    current_color = c.itemcget(eye_left, 'fill')
    new_color = c.body_color if current_color == 'white' else 'white'
    current_state = c.itemcget(pupil_left, 'state')
    new_state = NORMAL if current_state == HIDDEN else HIDDEN
    c.itemconfigure(pupil_left, state=new_state)
    c.itemconfigure(pupil_right, state=new_state)
    c.itemconfigure(eye_left, fill=new_color)
    c.itemconfigure(eye_right, fill=new_color)

def blink():
    toggle_eyes()
    root.after(250, toggle_eyes)
    root.after(3000, blink)
    
def open_second_window():
    second_window = Toplevel(root)
    second_window.title("Let's talk!")

    label = Label(second_window, text="Choose a message from the list:")
    label.pack()

    # list of messages
    messages = [
        "Hello!", "What's up?", "Good morning!", "Goodbye!",
        "Thank you!", "What are you up to?", "What time is it?",
        "Do you know how to dance?", "Who is the president?", "What kind of movies do you like?", "Can you sing?"
    ]

    # listbox to display the messages
    listbox = Listbox(second_window, selectmode=SINGLE)
    for message in messages:
        listbox.insert(END, message)
    listbox.config(width=50, height=10, justify="center")
    listbox.pack()

    # add a scrollbar to the listbox
    scrollbar = Scrollbar(second_window, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # button to choose a message
    button_choose = ttk.Button(second_window, text="Choose", command=lambda: choose_message(listbox))
    button_choose.pack()

def choose_message(listbox):
    # get the selected message
    selected_index = listbox.curselection()
    
    if selected_index:
        selected_message = listbox.get(selected_index)
        response = get_custom_response(selected_message)
    else:
        response = "No message chosen."

    # print the response in the console
    print(response)

    # show the response in a new window
    show_response_window(response)

food_item = None

def create_food():
    global food_item
    food_item = c.create_oval(190, 330, 210, 350, outline='green', fill='green')

def move_food():
    if food_item:
        c.move(food_item, 0, -7)
        c.itemconfigure(tongue_tip, state=NORMAL)
        c.itemconfigure(tongue_main, state=NORMAL)
        c.tongue_out = True
        root.after(1100, retract_tongue)  # schedule the tongue to retract after a short delay

def retract_tongue():
    if c.tongue_out:
        c.itemconfigure(tongue_tip, state=HIDDEN)
        c.itemconfigure(tongue_main, state=HIDDEN)
        c.tongue_out = False

def feed_pet():
    global food_item
    # hide the tongue and increase happiness level
    c.itemconfigure(tongue_main, state=HIDDEN)
    c.itemconfigure(tongue_tip, state=HIDDEN)
    if c.happy_level <= 8:
        c.happy_level += 2
        update_happiness_label()
    
    # show the feeding animation
    create_food()
    for _ in range(10):
        move_food()
        root.update()
        root.after(100)
    c.delete(food_item)
    food_item = None

def get_custom_response(selected_message):
    # define a dictionary of custom responses
    responses = {
        "Hello!": "Hey!",
        "What's up?": "I wanna play!",
        "Good morning!": "Mornin'!",
        "Goodbye!": "Bye, see you later!",
        "Thank you!": "You're welcome!",
        "What are you up to?": "I'm currently learning Spanish",
        "What time is it?": "I don't know, I don't have a watch!",
        "Do you know how to dance?": "No, but I'd love to learn!",
        "Who is the president?": "I don't know, I'm just a Desktop Pet.",
        "What kind of movies do you like?": "I like comedies and action movies.",
        "Can you sing?": "No, but I can dance!"
        # add more custom responses if needed
    }

    # return the custom response if it exists, otherwise return the selected message
    return responses.get(selected_message, selected_message)

# other functions

def music():
    # create a new Toplevel window for music player buttons
    music_player_window = Toplevel(root)
    music_player_window.title("Music Player")

    # instantiate the MusicPlayer class in the new window
    player = MusicPlayer(music_player_window)

    # add player buttons to the new window
    player.Load.pack()
    player.Play.pack()
    player.Pause.pack()
    player.Stop.pack()

def jokes():
    # get a random joke
    if c.happy_level <= 9:
        c.happy_level += 1
    joke = pyjokes.get_joke(language="en", category="all")
    show_response_window(joke)

def show_response_window(response):
    # create a new Toplevel window for the response
    response_window = Toplevel(root)
    response_window.title("Answer")

    bubble_label = Label(response_window, text=response, bg='white', padx=10, pady=10, relief='solid', borderwidth=1)
    bubble_label.configure(font=('Arial', 10), justify='center', width=50, height=5, wraplength=200)
    bubble_label.pack()

    response_window.geometry(f"{len(response) * 8}x100+400+300")

def toggle_pupils():
    if not c.eyes_crossed:
        c.move(pupil_left, 10, -5)
        c.move(pupil_right, -10, -5)
        c.eyes_crossed = True
    else:
        c.move(pupil_left, -10, 5)
        c.move(pupil_right, 10, 5)
        c.eyes_crossed = False

def toggle_tongue():
    if c.eyes_crossed:  # check if the eyes are crossed
        if not c.tongue_out:
            c.itemconfigure(tongue_tip, state=NORMAL)
            c.itemconfigure(tongue_main, state=NORMAL)
            c.tongue_out = True
        else:
            c.itemconfigure(tongue_tip, state=HIDDEN)
            c.itemconfigure(tongue_main, state=HIDDEN)
            c.tongue_out = False

def cheeky(event):
    if not c.cheeky_disabled:
        toggle_tongue()
        toggle_pupils()
        hide_happy(event)
        root.after(1000, toggle_tongue)
        root.after(1000, toggle_pupils)
        c.cheeky_disabled = True  # deactivates the cheeky function for a short period of time
    return

def show_happy(event):
    if (20 <= event.x and event.x <= 350) and (20 <= event.y and event.y <= 350):
        c.itemconfigure(cheek_left, state=NORMAL)
        c.itemconfigure(cheek_right, state=NORMAL)
        c.itemconfigure(mouth_happy, state=NORMAL)
        c.itemconfigure(mouth_normal, state=HIDDEN)
        c.itemconfigure(mouth_sad, state=HIDDEN)
        c.happy_level = 10
        update_happiness_label()
    return

def hide_happy(event):
    c.itemconfigure(cheek_left, state=HIDDEN)
    c.itemconfigure(cheek_right, state=HIDDEN)
    c.itemconfigure(mouth_happy, state=HIDDEN)
    c.itemconfigure(mouth_normal, state=NORMAL)
    c.itemconfigure(mouth_sad, state=HIDDEN)
    update_happiness_label()
    return

def sad():
    if c.happy_level == 0:
        c.itemconfigure(mouth_happy, state=HIDDEN)
        c.itemconfigure(mouth_normal, state=HIDDEN)
        c.itemconfigure(mouth_sad, state=NORMAL)
    else:
        c.happy_level -= 1
        update_happiness_label()
    root.after(5000, sad)

def update_happiness_label():
    happiness_label.config(text="Happiness Level: {}".format(c.happy_level))

def toggle_cheek_color(event):
    cheek = cheek_left if (20 <= event.x <= 170) and (180 <= event.y <= 230) else cheek_right if (280 <= event.x <= 330) and (180 <= event.y <= 230) else None
    if cheek:
        current_color = c.itemcget(cheek, 'fill')
        new_color = 'red' if current_color == cheek_color else cheek_color
        c.itemconfigure(cheek, fill=new_color)
        root.after(3000, lambda: restore_cheek(cheek))

def restore_cheek(cheek):
    c.itemconfigure(cheek, fill=cheek_color)
    c.cheeky_disabled = False  # allows the cheeky function to be used again

def open_pet_screen():
    # open the pet.py file in Visual Studio Code
    subprocess.Popen(["code ./pet.py"], shell=True)

def run_pet_desktop():
    # run the pet.py file
    subprocess.Popen(["python3 ./pet.py"], shell=True)

game_windows = []
flappy_bird_process = None
dino_process = None
snake_process = None

def run_flappy_bird():
    global flappy_bird_process
    
    flappy_bird_process = subprocess.Popen(["python3 ./flappybird.py"], shell=True)
    def update_happiness():
        global flappy_bird_process
        if c.happy_level <= 9:
            c.happy_level += 1
            update_happiness_label()
        if flappy_bird_process.poll() is None:
            root.after(3000, update_happiness)
        else:
            flappy_bird_process = None
    root.after(3000, update_happiness)


def run_dino():
    global dino_process
    
    dino_process = subprocess.Popen(["python3 ./dino.py"], shell=True)
    def update_happiness():
        global dino_process
        if c.happy_level <= 9:
            c.happy_level += 1
            update_happiness_label()
        if dino_process.poll() is None:
            root.after(3000, update_happiness)
        else:
            dino_process = None
    root.after(3000, update_happiness)


def run_snake():
    global snake_process
    
    snake_process = subprocess.Popen(["python3 ./snake.py"], shell=True)
    def update_happiness():
        global snake_process
        if c.happy_level <= 9:
            c.happy_level += 1
            update_happiness_label()
        if snake_process.poll() is None:
            root.after(3000, update_happiness)
        else:
            snake_process = None
    root.after(3000, update_happiness)
def run_breakout():
    global breakout_process

    breakout_process = subprocess.Popen(["python3 ./breakout.py"], shell=True)
    def update_happiness():
        global breakout_process
        if c.happy_level <= 9:
            c.happy_level += 1
            update_happiness_label()
        if breakout_process.poll() is None:
            root.after(3000, update_happiness)
        else:
            breakout_process = None
    root.after(3000, update_happiness)


class MusicPlayer:
    def __init__(self, window):
        self.window = window
        self.Load = Button(window, text='Load', width=10, font=('Times', 10), command=self.load)
        self.Play = Button(window, text='Play', width=10, font=('Times', 10), command=self.play)
        self.Pause = Button(window, text='Pause', width=10, font=('Times', 10), command=self.pause)
        self.Stop = Button(window, text='Stop', width=10, font=('Times', 10), command=self.stop)

        self.music_file = False
        self.playing_state = False

    def load(self):
        self.music_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])

    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            if c.happy_level <= 9:
                c.happy_level += 1
                update_happiness_label()

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
        else:
            mixer.music.unpause()
            self.playing_state = False

    def stop(self):
        mixer.music.stop()

root = Tk()
root.title("Desktop Pet")

script_directory = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_directory, 'gallery/imgs/icon.png')
if os.path.exists(icon_path):
    icon_image_pil = Image.open(icon_path)
    icon_image = ImageTk.PhotoImage(icon_image_pil)
    root.iconphoto(True, icon_image)  

root.resizable(False, False)
root.configure(bg='#AFBFC0')


# Desktop Pet design and functionality

c = Canvas(root, width=400, height=400)
c.configure(bg='dark blue', highlightthickness=0)
c.body_color = 'SkyBlue1'

# body components
body = c.create_oval(35, 20, 365, 350, outline=c.body_color, fill=c.body_color)

tail = c.create_line(300, 200, 400, 300, width=10, fill=c.body_color)
ear_left = c.create_polygon(75, 80, 75, 10, 165, 70, outline=c.body_color, fill=c.body_color)
ear_right = c.create_polygon(255, 45, 325, 10, 320, 70, outline=c.body_color, fill=c.body_color)
foot_left = c.create_oval(65, 320, 145, 360, outline=c.body_color, fill=c.body_color)
foot_right = c.create_oval(250, 320, 330, 360, outline=c.body_color, fill=c.body_color)

eye_left = c.create_oval(130, 110, 160, 170, outline='black', fill='white')
pupil_left = c.create_oval(140, 145, 150, 155, outline='black', fill='black')
eye_right = c.create_oval(230, 110, 260, 170, outline='black', fill='white')
pupil_right = c.create_oval(240, 145, 250, 155, outline='black', fill='black')


mouth_normal = c.create_line(170, 250, 200, 272, 230, 250, smooth=1, width=2, state=NORMAL)
mouth_happy = c.create_line(170, 250, 200, 282, 230, 250, smooth=1, width=2, state=HIDDEN)
mouth_sad = c.create_line(170, 250, 200, 232, 230, 250, smooth=1, width=2, state=HIDDEN)
tongue_main = c.create_rectangle(170, 250, 230, 290, outline='red', fill='red', state=HIDDEN)
tongue_tip = c.create_oval(170, 285, 230, 300, outline='red', fill='red', state=HIDDEN)

cheek_color = 'pink'
cheek_left = c.create_oval(70, 180, 120, 230, outline='pink', fill='pink', state=HIDDEN)
cheek_right = c.create_oval(280, 180, 330, 230, outline='pink', fill='pink', state=HIDDEN)

whisker1 = c.create_line(80, 180, 10, 160, width=2, fill='black')
whisker2 = c.create_line(80, 200, 10, 200, width=2, fill='black')
whisker3 = c.create_line(80, 220, 10, 240, width=2, fill='black')

whisker4 = c.create_line(320, 180, 390, 160, width=2, fill='black')
whisker5 = c.create_line(320, 200, 390, 200, width=2, fill='black')
whisker6 = c.create_line(320, 220, 390, 240, width=2, fill='black')

# bind the Desktop Pet to the mouse
c.pack()
c.bind('<Motion>', show_happy)
c.bind('<Leave>', hide_happy)
c.bind('<Double-1>', cheeky)
c.bind('<Button-1>', toggle_cheek_color)

c.happy_level = 10
c.eyes_crossed = False
c.tongue_out = False
c.cheeky_disabled = False

# creating the buttons for the Desktop Pet

happiness_label = ttk.Label(root, text="Happiness Level: 10", font=('Arial', 12))
happiness_label.pack(pady=5)

button_open_second_window = ttk.Button(root, text="Let's talk", command=open_second_window)
button_open_second_window.pack(pady=5)

button_feed_pet = ttk.Button(root, text="Feed me", command=feed_pet)
button_feed_pet.pack(pady=5)

button_custom_function_1 = ttk.Button(root, text="Let's listen to music", command=music)
button_custom_function_1.pack(pady=5)

button_custom_function_2 = ttk.Button(root, text="Tell me a joke", command=jokes)
button_custom_function_2.pack(pady=5)

button_open_website = ttk.Button(root, text="Open Visual Studio Code", command=open_pet_screen)
button_open_website.pack(pady=5)

button_open_website = ttk.Button(root, text="Run the code", command=run_pet_desktop)
button_open_website.pack(pady=5)

button_flappy_bird = ttk.Button(root, text="Let's play Flappy Bird", command=run_flappy_bird)
button_flappy_bird.pack(pady=5)

button_dino = ttk.Button(root, text="Let's play Dino Runner", command=run_dino)
button_dino.pack(pady=5)

button_snake = ttk.Button(root, text="Let's play Snake", command=run_snake)
button_snake.pack(pady=5)

button_breakout = ttk.Button(root, text="Let's play Breakout", command=run_breakout)
button_breakout.pack(pady=5)

root.after(1000, blink)
root.after(5000, sad)

root.mainloop()