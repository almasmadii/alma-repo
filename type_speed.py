import tkinter as tk
import time
import random
timer_id=None

root=tk.Tk()
root.config(bg="pink",width=20,height=15,padx=10,pady=10)
root.title("TypeRace")

window_width=800
window_height=600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

possibleTexts=["list tuple dictionary string variable function module python",
            "the quick brown fox jumps over the lazy dog",
            "to be or not to be that is the question",
            "A bird in the hand is worth two in the bush."
            "Never underestimate the power of a good book." ]
text = random.choice(possibleTexts)
timer_started=False
start_time = None
timer_var = tk.StringVar(value="60")

timer_label = tk.Label(root, textvariable=timer_var)
timer_label.pack()

text_label=tk.Label(root,text=text)
text_label.pack()
text_label.config()
time_left = 60
result_label=tk.Label(root,text="")
result_label.pack()

def countdown():
    global time_left,timer_id

    if time_left > 0:
        timer_var.set(str(time_left))
        time_left-=1
        timer_id=root.after(1000,countdown)

def calc_wpm():
    global start_time
    if start_time is None:
        return
    typed=text_box.get("1.0","end-1c")
    word_count=len(typed.split())
    end_time = time.time()
    elapsed_minutes = (end_time - start_time) / 60
    if elapsed_minutes == 0 :
        return
    wpm=word_count/elapsed_minutes
    result_label.config(text=f"WPM: {round(wpm)}!")

def start_timer(event):
    global timer_started,start_time
    if not timer_started:
        timer_started=True
        start_time=time.time()
        countdown()

def check_complete(event):
    typed=text_box.get("1.0","end-1c")
    if typed.strip()==text.strip():
        root.after_cancel(timer_id)
        text_box.config(state="disabled")
        calc_wpm()


text_box = tk.Text(root, height=10, width=40)
text_box.config(padx=20,pady=10)
text_box.bind("<Key>",start_timer)
text_box.bind("<KeyRelease>",check_complete)
text_box.pack()


root.mainloop()


















