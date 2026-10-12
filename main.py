import tkinter as tk
import time

window = tk.Tk()
window.title("Typing Speed Test")
window.geometry("800x600")
window.configure(bg="light green")

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
    bg='white',
    fg='green',
)
label.pack(pady=(12, 8))

# Sample text
label2 = tk.Label(
    window,
    text=sample_text,
    font=("Arial", 17),
    bg="white",
    fg="green",
    pady=14,
    padx=14,
    wraplength=700,
    justify="left"
)
label2.pack(fill="x", padx=25, pady=8)

# Typing area
typing_box = tk.Text(
    window,
    height=7,
    font=("Arial", 13),
    wrap="word",
    bg="white",
    fg="green",
)
typing_box.pack(fill="both", expand=True, padx=25, pady=8)

# Results
results_label = tk.Label(
    window,
    text="Start typing to begin!",
    font=("Arial", 14),
    bg="white",
    justify="center",
    fg="green"
)
results_label.pack(pady=10)

time_label = tk.Label(
    window,
    text=f"Time left: {TIME_LIMIT} seconds",
    font=("Arial", 15),
    bg="white",
    fg="green"
)
time_label.pack(pady=4)

status_label = tk.Label(
    window,
    text="Ready to start",
    font=("Arial", 15),
    bg="white",
    fg="green"
)
status_label.pack()

# Start the timer when the user types
def start_test(event=None):
    global start_time

    if start_time is None and not test_finished:
        start_time = time.perf_counter()
        status_label.config(text="Test in progress")
        update_timer()


typing_box.bind("<KeyPress>", start_test)


# Update the countdown
def update_timer():
    global timer_job, time_left

    if test_finished or start_time is None:
        return

    elapsed_time = time.perf_counter() - start_time
    time_left = max(0, TIME_LIMIT - int(elapsed_time))

    time_label.config(text=f"Time left: {time_left} seconds")

    if elapsed_time >= TIME_LIMIT:
        finish_test()
    else:
        timer_job = window.after(1000, update_timer)


# Calculate speed and accuracy
def calculate_results():
    typed_text = typing_box.get("1.0", "end-1c")

    typed_words = typed_text.split()
    count_words = len(typed_words)

    elapsed_time = time.perf_counter() - start_time
    elapsed_minutes = max(elapsed_time / 60, 1 / 60)

    wpm = count_words / elapsed_minutes

    # Compare typed characters with the sample text
    correct_chars = sum(
        typed_char == sample_char
        for typed_char, sample_char in zip(typed_text, sample_text)
    )

    # Characters typed beyond the sample are incorrect
    total_typed_chars = len(typed_text)

    accuracy = (
        correct_chars / total_typed_chars * 100
        if total_typed_chars > 0
        else 0
    )

    results_label.config(
        text=(
            f"Accuracy: {accuracy:.1f}%\n"
            f"Speed: {wpm:.1f} WPM\n"
            f"Words typed: {count_words}\n"
            f"Correct characters: {correct_chars}"
        )
    )


# Finish the test
def finish_test():
    global test_finished, timer_job

    if test_finished:
        return

    test_finished = True

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    time_label.config(text="Time left: 0 seconds")
    status_label.config(text="Time Over")

    typing_box.configure(state="disabled")

    calculate_results()


# Reset everything
def reset_timer():
    global timer_job, time_left, test_finished, start_time

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    start_time = None
    time_left = TIME_LIMIT
    test_finished = False

    typing_box.configure(state="normal")
    typing_box.delete("1.0", "end")

    time_label.config(text=f"Time left: {TIME_LIMIT} seconds")
    status_label.config(text="Ready to start")
    results_label.config(text="Start typing to begin!")


reset_button = tk.Button(
    window,
    text="Reset Test",
    font=("Arial", 15),
    command=reset_timer,
    fg="green",
    bg="white",
    justify="center",
)
reset_button.pack(pady=(5, 11))

finish_button = tk.Button(
    window,
    text="Finish",
    font=("Arial", 15),
    command=finish_test,
    fg="#40916C",
    bg="white",
    justify="center",
)

finish_button.pack(pady=(5, 11))

close_button = tk.Button(
    window,
    text="Close",
    font=("Arial", 15),
    command=window.destroy,
    fg="#40916C",
    bg="white",
)

close_button.pack(pady=(5, 11))

window.mainloop()
