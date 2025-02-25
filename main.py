from js import document, window
from pyodide.ffi import create_proxy

# App state
is_playing = False
count = 0
countdown = 4
total_time = 0
sound_enabled = False
time_limit = None
session_complete = False

# Get DOM elements
start_button = document.getElementById("start-button")
reset_button = document.getElementById("reset-button")
sound_toggle = document.getElementById("sound-toggle")
time_limit_input = document.getElementById("time-limit")
instruction_div = document.getElementById("instruction")
countdown_div = document.getElementById("countdown")
timer_div = document.getElementById("timer")
controls_div = document.getElementById("controls")

# Helper functions
def get_instruction(count):
    if count == 0:
        return "Inhale"
    elif count == 1:
        return "Hold"
    elif count == 2:
        return "Exhale"
    elif count == 3:
        return "Wait"
    return ""

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def play_tone():
    if sound_enabled:
        try:
            audio_context = new window.AudioContext()
            oscillator = audio_context.createOscillator()
            oscillator.type = "sine"
            oscillator.frequency.setValueAtTime(440, audio_context.currentTime)
            oscillator.connect(audio_context.destination)
            oscillator.start()
            oscillator.stop(audio_context.currentTime + 0.1)
        except Exception as e:
            print(f"Error playing sound: {e}")

# Timer function
def update_timer():
    global is_playing, count, countdown, total_time, session_complete
    
    if not is_playing or session_complete:
        return
    
    countdown = countdown - 1
    
    if countdown <= 0:
        count = (count + 1) % 4
        play_tone()
        countdown = 4
        total_time += 1
    
    # Check time limit
    if time_limit:
        time_limit_seconds = int(time_limit) * 60
        if total_time >= time_limit_seconds:
            if count == 2 and countdown == 1:
                end_session()
        elif total_time >= time_limit_seconds - 12:
            end_session()
    
    # Update UI
    countdown_div.innerText = str(countdown)
    instruction_div.innerText = get_instruction(count)
    timer_div.innerText = f"Total Time: {format_time(total_time)}"
    
    # Schedule next update
    if is_playing:
        window.setTimeout(create_proxy(update_timer), 1000)

def toggle_play(event):
    global is_playing, total_time, countdown, count, session_complete
    
    is_playing = not is_playing
    
    if is_playing:
        # Starting
        start_button.innerText = "Pause"
        total_time = 0
        countdown = 4
        count = 0
        session_complete = False
        controls_div.style.display = "none"
        countdown_div.style.display = "block"
        instruction_div.innerText = get_instruction(count)
        timer_div.innerText = f"Total Time: {format_time(total_time)}"
        window.setTimeout(create_proxy(update_timer), 1000)
    else:
        # Pausing
        start_button.innerText = "Start"

def end_session():
    global is_playing, session_complete
    
    is_playing = False
    session_complete = True
    instruction_div.innerText = "Complete!"
    countdown_div.style.display = "none"
    start_button.style.display = "none"
    reset_button.style.display = "block"

def reset_to_start(event):
    global is_playing, total_time, countdown, count, session_complete, time_limit
    
    # Reset UI
    is_playing = False
    total_time = 0
    countdown = 4
    count = 0
    session_complete = False
    time_limit = None
    time_limit_input.value = ""
    instruction_div.innerText = "Press start to begin"
    countdown_div.style.display = "none"
    timer_div.innerText = ""
    start_button.innerText = "Start"
    start_button.style.display = "block"
    reset_button.style.display = "none"
    controls_div.style.display = "block"

def update_sound_enabled(event):
    global sound_enabled
    sound_enabled = sound_toggle.checked

def update_time_limit(event):
    global time_limit
    
    # Remove non-numeric characters
    time_limit_input.value = ''.join(c for c in time_limit_input.value if c.isdigit())
    time_limit = time_limit_input.value

# Set up event listeners
start_button.addEventListener("click", create_proxy(toggle_play))
reset_button.addEventListener("click", create_proxy(reset_to_start))
sound_toggle.addEventListener("change", create_proxy(update_sound_enabled))
time_limit_input.addEventListener("input", create_proxy(update_time_limit))
