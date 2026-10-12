import tkinter as tk
import time

window = tk.Tk()
window.title("Typing Speed Test")
window.geometry("800x600")
window.configure(bg="#17212B")

sample_text = (
    "Python is a powerful programming language. "
    "Practice every day to improve your typing speed "
    "and accuracy. Small improvements lead to great results."
)

TIME_LIMIT = 60

start_time = None
time_left = TIME_LIMIT
timer_job = None
test_finished = False

# Heading
label = tk.Label(
    window,
    text="Typing Speed Test",
    font=("Arial", 17, "bold"),
    bg="black",
    fg="cyan"
)
label.pack(pady=(12, 8))

# Sample text
label2 = tk.Label(
    window,
    text=sample_text,
    font=("Arial", 17),
    bg="black",
    pady=14,
    padx=14,
    wraplength=700,
    justify="left",
    fg="cyan"
)
label2.pack(fill="x", padx=25, pady=8)

# Typing area
typing_box = tk.Text(
    window,
    height=7,
    font=("Arial", 17),
    wrap="word",
    bg="cyan",
    fg="#243746",
    undo=True,
)
typing_box.pack(fill="both", expand=True, padx=25, pady=8)

# Results
results_label = tk.Label(
    window,
    text="Start typing to begin!",
    font=("Arial", 14),
    bg="black",
    justify="center",
    fg="cyan",
)
results_label.pack(pady=10)

time_label = tk.Label(
    window,
    text=f"Time left: {TIME_LIMIT} seconds",
    font=("Arial", 15),
    bg="cyan",
    fg="black",
)
time_label.pack(pady=4)

status_label = tk.Label(
    window,
    text="Ready to start",
    font=("Arial", 15),
    bg="cyan",
    fg="black",
)
status_label.pack()

def start_test(event=None):
    global start_time

    if start_time is None and not test_finished:
        start_time = time.perf_counter()
        time_label.configure(text="Time in Progress")
        update_timer()

typing_box.bind("<KeyPress>", start_test)

def update_timer():
    global test_finished , timer_job , time_left

    if test_finished or start_time is None:
        return

    elapsed_time = time.perf_counter() - start_time
    time_left = TIME_LIMIT - int(elapsed_time)

    time_label.configure(text=f"Time left: {time_left} seconds")

    if elapsed_time >= TIME_LIMIT:
        finished_test()

    else:
        timer_job = window.after(1000, update_timer)


def calculated_result():

    typed_text = typing_box.get("1.0", "end-1c")
    typed_text = typed_text.split()
    count_text = len(typed_text)

    elapsed_time = time.perf_counter() - start_time
    elapsed_mins = max(elapsed_time/60 , 1/60)

    wpm = count_text / elapsed_mins

    correct_chars = sum(
        text_char == sample_char
        for text_char , sample_char in zip(typed_text, sample_text)
    )

    total_chars = len(typed_text)

    accuracy = (
        correct_chars / total_chars * 100
        if total_chars > 0 else 0
    )

    results_label.config(
        text=f"Speed {wpm:.1f} WPM\n"
             f"Accuracy: {accuracy:.1f}%\n"
             f"Correct Chars: {correct_chars}\n"
             f"Total Chars: {total_chars}"
    )


def finished_test():

    global test_finished , timer_job

    if test_finished:
        return

    test_finished = True

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    time_label.config(text="Time Left: 0 Seconds")
    status_label.configure(text="Time Over !!")

    typing_box.configure(state="disabled")

    calculated_result()



def reset_everything():

    global test_finished , timer_job , start_time , time_left

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    start_time = None
    time_left = TIME_LIMIT
    test_finished = False

    typing_box.configure(state="normal")
    typing_box.delete("1.0", "end")

    status_label.configure(text="Ready to start!")
    results_label.configure(text="Start typing to begin!")


finished_btn = tk.Button(
    window,
    text="Finishing Test",
    command=finished_test,
    bg="black",
    fg="cyan",
)
finished_btn.pack(padx=1, pady=1)

reset_btn = tk.Button(
    window,
    text="Reset Button",
    command=reset_everything,
    bg="black",
    fg="cyan",
)

reset_btn.pack(padx=1, pady=1)

close_btn = tk.Button(
    window,
    text="Close Button",
    command=window.destroy,
    bg="black",
    fg="cyan",
)
close_btn.pack(padx=1, pady=1)

window.mainloop()