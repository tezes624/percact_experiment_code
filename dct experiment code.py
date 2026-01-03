#EV
#setup, imports
import time
import random
from psychopy import core, visual, event, gui, data, sound
import csv

#screens to show
    #welcome, requirements
welcome_screen = '''
Welcome to the experiment!

To participate you must meet the following requirements:
18 years of age or older
Normal or corrected vision 
Normal hearing

Press 'SPACE' to confirm fulfiling the above.
'''
    #consent
consent_screen = '''
The data collected in this experiment are anonymous and the participation is completly voluntary. 
The experiment will take about 10 minutes to complete. After, you have the option to debrief with the experimenter.
You can withdraw your consent to participate at any time prior to or during the experiment pressing 'ESCAPE'.

If you have any questions, feel free to ask the experimenter.

If you understand these conditions and consent to participating, press 'SPACE' to continue to the instructions. 
'''
    #instructions
instructions_screen = '''
The experiment consists of 60 trials.
In each trial you will be presented with a short sound. 
Your task is to indicate either "THIS" or "THAT" by clicking on one of the options displayed.
Your response should be based on what word you most associate with the sound.
You can click the buttons once the sound has been played.

If you have any questions, feel free to ask the experimenter.

You can start the experiment by pressing 'SPACE'
'''
    #thank you
thankyou_screen = '''
Thank you for your participation. 

You now have the option to debrief with the experimenter if you wish to.

Press 'SPACE' to exit.
'''

#collect participant information
dialog = gui.Dlg(title="Please fill in your information")
dialog.addField("ID", label="Participant ID:")
dialog.addField("age", label="Age:")
dialog.addField("gender", label="Gender:", choices=['Female', 'Male', 'Other'])
dialog.addField("nationality", label = "Nationality:")
dialog.show()

#save data
if dialog.OK:
    ID = dialog.data["ID"]
    age = dialog.data["age"]
    gender = dialog.data ["gender"]
    nationality = dialog.data["nationality"]
else:
    core.quit()

#load in soundfiles
sound_files = {
    '0078': '0078.mp3',
    '0133': '0133.mp3',
    '0249': '0249.mp3',
    '0288': '0288.mp3',
    '0359': '0359.mp3',
    '0478': '0478.mp3',
    '0511': '0511.mp3',
    '0585': '0585.mp3',
    '0614': '0614.mp3',
    '0681': '0681.mp3',
    '0688': '0688.mp3',
    '0848': '0848.mp3',
    '0902': '0902.mp3',
    '1259': '1259.mp3',
    '1313': '1313.mp3',
    '1343': '1343.mp3',
    '1356': '1356.mp3',
    '1622': '1622.mp3',
    '1806': '1806.mp3',
    '2002': '2002.mp3',
}

#create stimulus set
stimuli1 = list(sound_files.items()) 
random.shuffle(stimuli1)
stimuli2 = list(sound_files.items()) 
random.shuffle(stimuli2)
stimuli3 = list(sound_files.items()) 
random.shuffle(stimuli3)

stimuli = stimuli1 + stimuli2 + stimuli3

#set trial count to 0
trial_count = 0

#total trials
n_trials = 60

#create trial log
trial_log = []

#define window
win = visual.Window(
    size=[1800, 1000], 
    color=['gray'],
    units='pix')

#visuals setup
mouse = event.Mouse(visible=True, win=win)
    #demonstratives background
rectangle_size = [200, 150]
left_rectangle = visual.Rect(win, width=rectangle_size[0], height=rectangle_size[1], fillColor='black', pos=(-250, 0))
right_rectangle = visual.Rect(win, width=rectangle_size[0], height=rectangle_size[1], fillColor='black', pos=(250, 0))
    #fixation cross
fixation = visual.TextStim(win, text='+', color='black', height=40)

#TS
#define experiment function
def experiment():
    global trial_count, stimuli
    while True:
        #increase trial_count if relevant
        if trial_count < n_trials:
            trial_count += 1
        else:
            break
        #pick a stimulus by random and remove it from the stimulus set
        stim_id, stim_file = stimuli.pop(random.randrange(len(stimuli)))
        #demonstratives
        demonstratives = ("THIS", "THAT")
        left_dem = random.choice(demonstratives)
        if left_dem == "THIS":
            right_dem = "THAT"
        else:
            right_dem = "THIS"
        demonstrative_left = visual.TextStim(win, text=left_dem, color='white', pos=(-250, 0))
        demonstrative_right = visual.TextStim(win, text= right_dem, color='white', pos=(250, 0))
        #present trial visuals
        left_rectangle.draw()
        right_rectangle.draw()
        demonstrative_left.draw()
        demonstrative_right.draw()
        win.flip()
        #play sound
        stimulus = sound.Sound(stim_file, stereo=True)
        stimulus.play()
        core.wait(stimulus.getDuration())
        #wait for demonstrative choice
        clicked = False
        while not clicked:
            buttons, times = mouse.getPressed(getTime=True)
            if buttons[0]:
                mouse_pos = mouse.getPos()
                if left_rectangle.contains(mouse_pos):
                    clicked = True
                    if left_dem == "THIS":
                        choice = 1
                    else:
                        choice = 0
                elif right_rectangle.contains(mouse_pos):
                    clicked = True
                    if right_dem == "THIS":
                        choice = 1
                    else:
                        choice = 0
            if 'escape' in event.getKeys():
                core.quit()
        #draw fixation cross
        fixation.draw()
        win.flip()
        core.wait(1)
        #save data
        trial_log.append({
            "trial": trial_count,
            "stimulus": stim_id,
            "demonstrative": choice
        })

#display welcome screen
welcome_vis_screen = visual.TextStim(win, text=welcome_screen, color="white")
welcome_vis_screen.draw()
win.flip()
#wait for keypress
keys = event.waitKeys(keyList=["space", "escape"])
if "escape" in keys:
    win.close()
    core.quit()

#display consent screen
consent_vis_screen = visual.TextStim(win, text=consent_screen, color="white")
consent_vis_screen.draw()
win.flip()
#wait for consent
keys = event.waitKeys(keyList=["space", "escape"])
if "escape" in keys:
    win.close()
    core.quit()

#display instructions screen
instructions_vis_screen = visual.TextStim(win, text=instructions_screen, color="white")
instructions_vis_screen.draw()
win.flip()
#wait for keypress
keys = event.waitKeys(keyList=["space", "escape"])
if "escape" in keys:
    win.close()
    core.quit()

#call experiment function
experiment()

#EV
#saving data
fieldnames = [
    "participant_id",
    "age",
    "gender",
    "nationality",
    "trial",
    "stimulus",
    "demonstrative"
]
#write file
with open(f"{ID}_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for row in trial_log:
        row_to_write = {
            "participant_id": ID,
            "age": age,
            "gender": gender,
            "nationality": nationality,
            "trial": row["trial"],
            "stimulus": row["stimulus"],
            "demonstrative": row["demonstrative"]
        }
        writer.writerow(row_to_write)

#TS
#display thank you screen
thankyou_vis_screen = visual.TextStim(win, text=thankyou_screen, color="white")
thankyou_vis_screen.draw()
win.flip()
#wait for keypress
keys = event.waitKeys(keyList=["space", "escape"])

#press space to close the experiment
win.close()
core.quit()
