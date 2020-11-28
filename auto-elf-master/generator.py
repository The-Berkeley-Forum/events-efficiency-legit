"""Generates an optimal event logistics form."""

from state import mem_time_code, single_speaker_schedule, multi_speaker_schedule, single_transform, single_inverse, multiple_transform, multiple_inverse
from schedule import Schedule
from load import loadMeta, loadPersons
from random import randint
from os import path, mkdir
from copy import deepcopy
import statistics as stat
import sys
from tempfile import NamedTemporaryFile
import shutil
import csv
from tkinter import *
from PIL import ImageTk, Image # Used for resizing the image
import argparse
from tkinter import messagebox

def main():
    def close(frame):
        window.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing
    
    # Adding a blank div
    def add_div(row_num, col_num=0):
        Label (window, text="___", bg="#1e374a", fg="#1e374a", font="Arial 3", justify=LEFT).grid(row=row_num, column=col_num, sticky=SW)

    # Adding a text entry box
    # def add_entry(row_num, col_num=1):
    # textentry = Entry(window, width=25, bg='white', font="Arial 6")
    # textentry.grid(row=row_num, column=col_num, padx=10)

    # Window setup
    window = Tk()
    window.title("Events Logistics Generator")
    window.configure(bg='#1e374a')
    window.geometry("800x740")
    window.tk.call('tk', 'scaling', 3)
    window.bind('<Escape>', close)
    # window.wm_attributes('-transparentcolor', 'grey') #window['bg'] #Transparent background...

    # ESC to Quit label
    Label (window, text="Press ESC to quit", bg="#1e374a", fg="white", font="Helvetica 10", justify=RIGHT).grid(row=0, column=4, pady=10, sticky=NE)

    # Title
    Label (window, text="Events Logistics Generator", bg="#1e374a", fg="white", font="Arial 14", justify=RIGHT).grid(row=0, column=1)


    # TBF Logo
    logoimg = Image.open('img/Berkeley_Forum_logo.png')
    logoimg = logoimg.resize((200, 200), Image.ANTIALIAS)
    logophoto = ImageTk.PhotoImage(logoimg)

    Label (window, image=logophoto, bg='#1e374a') .grid(row=0, column=0, sticky=W)

    # Adding text
    # Title
    Label (window, text="What is the title of the event? [REQUIRED]", bg="#1e374a", fg="white", font="Arial 12", justify=LEFT).grid(row=1, column=0, padx=10, sticky=SW)
    #add_entry(1)
    e = Entry(window, width=25, bg='white', font="Arial 12")
    e.grid(row = 1, column = 1, padx = 10)

    text = Label (window, text="format: Alan Turing at the Berkeley Forum", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=2, column=0, padx=10, sticky=NW)

    
    add_div(3)

    # Type
    Label (window, text="What type of event is it? [REQUIRED]", bg = "#1e374a", fg="white", font="Arial 12", justify=LEFT) .grid(row=4, column=0, padx=10, sticky=SW)
    t = Entry(window, width=25, bg='white', font="Arial 12")
    t.grid(row = 4, column = 1, padx = 10)

    text = Label (window, text="format: single, multi", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=5, column=0, padx=10, sticky=NW)

    add_div(6)

    # Day
    Label (window, text="What is the day of the event? [REQUIRED]", bg = "#1e374a", fg="white", font="Arial 12", justify=LEFT) .grid(row=7, column=0, padx=10, sticky=SW)
    d = Entry(window, width=25, bg='white', font="Arial 12")
    d.grid(row = 7, column = 1, padx = 10)
    #add_entry(7)

    text = Label (window, text="format: Monday, Tuesday, etc.", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=8, column=0, padx=10, sticky=NW)

    add_div(9)

    # Time
    Label (window, text="What is the time of the event? [REQUIRED]", bg = "#1e374a", fg="white", font="Arial 12", justify=LEFT) .grid(row=10, column=0, padx=10, sticky=SW)
    ti = Entry(window, width=25, bg='white', font="Arial 12")
    ti.grid(row = 10, column = 1, padx = 10)
    #add_entry(10)

    text = Label (window, text="format: 5:00 PM, 6:30 PM, etc.", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=11, column=0, padx=10, sticky=NW)

    add_div(12)
    
    # Member Exlusions
    Label (window, text="Are there any member exclusions?", bg = "#1e374a", fg="white", font="Arial 12", justify=LEFT) .grid(row=13, column=0, padx=10, sticky=SW)
    mem = Entry(window, width=25, bg='white', font="Arial 12")
    mem.grid(row = 13, column = 1, padx = 10)
    #add_entry(13)

    text = Label (window, text="format: Alan Turing, Grace Hopper, etc.", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=14, column=0, padx=10, sticky=NW)

    add_div(15)

    # Job Exlusions
    Label (window, text="Are there any job exclusions?", bg = "#1e374a", fg="white", font="Arial 12", justify=LEFT) .grid(row=16, column=0, padx=10, sticky=SW)
    job = Entry(window, width=25, bg='white', font="Arial 12")
    job.grid(row = 16, column = 1, padx = 10)

    text = Label (window, text="format: Tech Oversight/Set Up, Photographer, etc.", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=17, column=0, padx=10, sticky=NW)

    add_div(18)

    # Number of Schedules to be generated
    Label (window, text="Number of sample schedules created? [REQUIRED]", bg = "#1e374a", fg="white", font="Arial 12", justify=LEFT) .grid(row=19, column=0, padx=10, sticky=SW)
    sched = Entry(window, width=25, bg='white', font="Arial 12")
    sched.grid(row = 19, column = 1, padx = 10)

    text = Label (window, text="recommended: 10000", bg="#1e374a", fg="white", font = "Arial 10 italic", justify=LEFT)
    text.grid(row=20, column=0, padx=10, sticky=NW)

    add_div(21,2)

    def save():
        event = e.get()
        eventType = t.get()
        day = d.get()
        time = ti.get()
        memExc = mem.get()
        jobExc = job.get()
        schedExc = sched.get()
        global params
        params = [event, eventType, day, time, memExc, jobExc, schedExc]

    def saveAndGenerate():
        save()
        generate()

    # submit button
    Button(window, text="GENERATE!", width=10, padx=10, font="Arial 12", command=saveAndGenerate) .grid(row=22, column=4, sticky=E)

    # run the main loop
    window.mainloop()

def generate():
	unusable_chars = ["#", "%", "&", "{", "}", "\\", "<", ">",
					  "*", "?", "/", "$", "!", "'", "\"", ":",
					  "@", "+", "`", "|", "="]

	#title = input("\nWhat is the title of the event? (format: Alan Turing at the Berkeley Forum)\n>>> ")
	title = params[0]

	def charCheck(new_title):
		for character in unusable_chars:
			if character in new_title:
				return False
		return True

	while not charCheck(title):
		print("\nPlease enter a title without the following characters: " + ", ".join(unusable_chars) + ".\n")
		#title = input("What is the title of the event? (format: Alan Turing at the Berkeley Forum)\n>>> " )
		title = params[0]

	event_type = params[1]

	while event_type not in ["single", "multi"]:
		print("\nPlease enter a valid event type.\n")
		event_type = params[1]

	default_schedule = (single_transform if event_type == "single" else multiple_transform)

	day = params[2]
	valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

	while day not in valid_days:
		print("\nPlease enter a valid day.\n")
		day = params[2]

	hour = 0
	minute = 0
	meridian = "XM"

	while minute not in [0, 30] or meridian not in ["AM", "PM"] or (hour < 1 or hour > 12):
		time = params[3]
		meridian_split = time.split(" ")
		if len(meridian_split) != 2:
			print("\nPlease enter a valid time in 12 hour notation that is a multiple of 30 minutes.")
			hour = 0
			continue
		meridian = meridian_split[1]
		if meridian not in ["AM", "PM"]:
			print("\nPlease enter a valid time in 12 hour notation that is a multiple of 30 minutes.")
			hour = 0
			continue
		time_check = meridian_split[0].split(":")
		if len(time_check) != 2:
			print("\nPlease enter a valid time in 12 hour notation that is a multiple of 30 minutes.")
			hour = 0
			continue
		hour = int(time_check[0])
		minute = int(time_check[1])

	"""The adjusted time code is calculated to properly index into member availabilities."""
	time_code = ((0 if hour == 12 else hour) \
			  + (12 if meridian == "PM" else 0)) * 2 \
			  + (1 if minute == 30 else 0) \
			  - mem_time_code \
			  - 3

	elf = Schedule(title, time_code, event_type)
	new_schedule = elf.getWrittenSchedule()

	meta_information = loadMeta()
	people = loadPersons(meta_information)

	excluded = []

	excluded_prompt = params[4]

	if excluded_prompt != "":
		excluded_names = excluded_prompt.split(",")
		for name in excluded_names:
			excluded.append(name.strip())

	excluded_jobs = []

	excluded_jobs_prompt = params[5]

	if excluded_jobs_prompt != "":
		excluded_jobs = excluded_jobs_prompt.split(",")
		for i in range(len(excluded_jobs)):
			excluded_jobs[i] = excluded_jobs[i].strip()

	text_out = ["# Query Information\n\n", "## Event Information\n\n", "Title: " + title + "\n", "Event Type: " + event_type + "\n", "Day: " + day + "\n", "Time: " + time + "\n", \
				"Members Excluded: " + (", ".join(excluded) if len(excluded) != 0 else "None"), "\nJobs Excluded: " + ", ".join(excluded_jobs)  + "\n\n"]

	def createELF():
		from schedule import Schedule
		new_elf = Schedule(title, time_code, event_type)
		created_schedule = deepcopy(default_schedule)
		slots_completed = []
		people_assigned = []
		slot = randint(0, len(created_schedule)-1)
		while len(created_schedule) != len(slots_completed):
			while (slot in slots_completed):
				slot = randint(0, len(created_schedule)-1)
			if created_schedule[slot][0] in excluded_jobs or len(list(filter(lambda s: s != "BLANK", created_schedule[slot][1]))) == 0:
				slots_completed.append(slot)
				continue
			slots_completed.append(slot)
			shifts = created_schedule[slot][1]
			index = 0
			while shifts[index] == "BLANK":
				index += 1
			while index != len(shifts) and shifts[index] == "FILL_IN":
				if time_code + index < 0 or time_code + index > 23:
					created_schedule[slot][1][index] = "NONE_AVAILABLE"
					index += 1
					continue
				if index != 0 and shifts[index-1] != "BLANK" and shifts[index-1] != "NONE_AVAILABLE":
					prev = list(filter(lambda person: person.getName() == shifts[index-1], people[:]))
					if prev[0].getSchedule()[day][time_code + index] and len(list(filter(lambda person: prev[0].getName() == person, created_schedule[slot][1]))) < 2:
						created_schedule[slot][1][index] = prev[0].getName()
						index += 1
						continue
				available_people = list(filter(lambda person: person.getSchedule()[day][time_code + index] \
											   and person.getName() not in people_assigned \
											   and person.getName() not in excluded, people[:]))
				if len(available_people) == 0:
					created_schedule[slot][1][index] = "NONE_AVAILABLE"
					index += 1
					continue
				min_events_attended = min([person.getEventsAttended() for person in available_people])
				available_people = list(filter(lambda person: person.getEventsAttended() == min_events_attended, available_people))
				chosen_one = available_people[randint(0, len(available_people)-1)]
				created_schedule[slot][1][index] = chosen_one.getName()
				people_assigned.append(chosen_one.getName())
				index += 1
		new_elf.setWrittenSchedule(created_schedule)
		return new_elf

	def AC3():
		from schedule import Schedule
		new_elf = Schedule(title, time_code, event_type)
		created_schedule = deepcopy(default_schedule)
		people_assigned = []
		for slot in created_schedule:
			if len(list(filter(lambda s: s != "BLANK", created_schedule[slot][1]))) == 0:
				continue
			index = 0
			while shifts[index] == "BLANK":
				index += 1
			while index != len(shifts) and shifts[index] == "FILL_IN":
				if time_code + index < 0 or time_code + index > 23:
					return "AC3 terminated without finding a valid schedule."
				available_people = list(filter(lambda person: person.getSchedule()[day][time_code + index] \
												   and person.getName() not in people_assigned \
												   and person.getName() not in excluded, people[:]))
				if len(available_people) == 0:
					return "AC3 terminated without finding a valid schedule."
				chosen_one = available_people[randint(0, len(available_people)-1)]
				people_assigned.append(chosen_one.getName())
				index += 1
		new_elf.setWrittenSchedule(created_schedule)
		return new_elf

	def findOptimalELF(iterations=10000):
		nonlocal text_out
		sample_elfs = {}
		excluded_sample_elfs = {}
		excluded_sample_count = 0
		print()
		curr_progress = 0
		sys.stdout.write("Generating " + str(iterations) + " sample schedules: [{0}{1}] 0.0%\r".format("#" * 0, " " * 9))
		sys.stdout.flush()
		for i in range(iterations):
			if curr_progress != int(i / (iterations / 1000)):
				sys.stdout.write("Generating " + str(iterations) + " sample schedules: [{0}{1}] {2}\r".format("#" * int(i / (iterations / 10)), " " * (10 - int(i / (iterations / 10))), str(100 * i/iterations) + "%"))
				sys.stdout.flush()
				curr_progress = int(i / (iterations / 1000))
			if i == iterations-1:
				sys.stdout.write("Generating " + str(iterations) + " sample schedules: [{0}{1}] {2}\r".format("##########", "", "100.0%"))
				sys.stdout.flush()
			sample_elf = createELF()
			sample_people = set([])
			num_unoccupied_shifts = 0
			for slot in sample_elf.getWrittenSchedule():
				for name in slot[1]:
					if name == "NONE_AVAILABLE":
						num_unoccupied_shifts += 1
					if name != "BLANK" and name != "NONE_AVAILABLE":
						sample_people.add(name)
			if num_unoccupied_shifts > 0:
				excluded_sample_count += 1
				if num_unoccupied_shifts not in excluded_sample_elfs.keys():
					excluded_sample_elfs[num_unoccupied_shifts] = [sample_elf.getWrittenSchedule()]
				else:
					excluded_sample_elfs[num_unoccupied_shifts].append(sample_elf.getWrittenSchedule())
			else:
				if len(sample_people) not in sample_elfs.keys():
					sample_elfs[len(sample_people)] = [sample_elf.getWrittenSchedule()]
				else:
					sample_elfs[len(sample_people)].append(sample_elf.getWrittenSchedule())
		key_list = []
		for key in sample_elfs.keys():
			for values in sample_elfs[key]:
				key_list.append(key)
		excluded_key_list = []
		for key in excluded_sample_elfs.keys():
			for values in excluded_sample_elfs[key]:
				excluded_key_list.append(key)
		print("\n\n" + str(excluded_sample_count) + " samples had inoccupiable shifts and were excluded.")
		text_out.append("\n" + str(excluded_sample_count) + " samples had inoccupiable shifts and were excluded.\n")
		if len(sample_elfs.keys()) != 0:
			print("\nStatistics for number of members in " + str(iterations - excluded_sample_count) + " non-excluded sample ELFs:\n")
			print("* Minimum: " + str(min(key_list)))
			print("* Maximum: " + str(max(key_list)))
			print("* Median: " + str(stat.median(key_list)))
			print("* Mean: " + str(stat.mean(key_list)))
			print("* Mode: " + str(stat.mode(key_list)))
			text_out.append("\nStatistics for number of members in " + str(iterations - excluded_sample_count) + " non-excluded sample ELFs:\n\n")
			text_out += ["Minimum: " + str(min(key_list)) + "\n", "Maximum: " + str(max(key_list)) + "\n", "Median: " + str(stat.median(key_list)) + "\n", \
						 "Mean: " + str(stat.mean(key_list)) + "\n", "Mode: " + str(stat.mode(key_list)) + "\n"]
			if len(sample_elfs.keys()) > 1:
				print("* Standard Deviation: " + str(stat.stdev(key_list)))
				print("* Variance: " + str(stat.variance(key_list)) + "\n")
				text_out += ["Standard Deviation: " + str(stat.stdev(key_list)) + "\n", "Variance: " + str(stat.variance(key_list)) + "\n\n"]
			else:
				print()
				text_out.append("\n\n")
			for key in sorted(sample_elfs.keys()):
				stars = int(len(list(filter(lambda k: k == key, key_list))) / (iterations / 100))
				print(str(key) + " = |" + stars * "*")
				text_out.append(str(key) + " = |" + stars * "*" + "\n")
		else:
			print("\nStatistics for number of unoccupied shifts in " + str(excluded_sample_count) + " excluded sample ELFs:\n")
			print("* Minimum: " + str(min(excluded_key_list)))
			print("* Maximum: " + str(max(excluded_key_list)))
			print("* Median: " + str(stat.median(excluded_key_list)))
			print("* Mean: " + str(stat.mean(excluded_key_list)))
			print("* Mode: " + str(stat.mode(excluded_key_list)))
			text_out.append("\nStatistics for number of unoccupied shifts in " + str(excluded_sample_count) + " excluded sample ELFs:\n\n")
			text_out += ["Minimum: " + str(min(excluded_key_list)) + "\n", "Maximum: " + str(max(excluded_key_list)) + "\n", "Median: " + str(stat.median(excluded_key_list)) + "\n", \
						 "Mean: " + str(stat.mean(excluded_key_list)) + "\n", "Mode: " + str(stat.mode(excluded_key_list)) + "\n"]
			if len(excluded_sample_elfs.keys()) > 1:
				print("* Standard Deviation: " + str(stat.stdev(excluded_key_list)))
				print("* Variance: " + str(stat.variance(excluded_key_list)) + "\n")
				text_out += ["Standard Deviation: " + str(stat.stdev(excluded_key_list)) + "\n", "Variance: " + str(stat.variance(excluded_key_list)) + "\n\n"]
			else:
				print()
				text_out.append("\n\n")
			for key in sorted(excluded_sample_elfs.keys()):
				stars = int(len(list(filter(lambda k: k == key, excluded_key_list))) / (iterations / 10))
				print(str(key) + " = |" + stars * "*")
				text_out.append(str(key) + " = |" + stars * "*" + "\n")
		if len(sample_elfs.keys()) != 0:
			if int(stat.median(sample_elfs.keys())) in sample_elfs.keys() and int(stat.median(sample_elfs.keys())) == stat.median(sample_elfs.keys()):
				med_elfs = sample_elfs[int(stat.median(sample_elfs.keys()))]
				elf.setWrittenSchedule(med_elfs[randint(0,len(med_elfs)-1)])
				return elf
			else:
				median = stat.median(sample_elfs.keys())
				median_chosen = 0
				if abs(stat.median(sample_elfs.keys()) - stat.median_low(sample_elfs.keys())) < abs(stat.median(sample_elfs.keys()) - stat.median_high(sample_elfs.keys())):
					median_chosen = stat.median_low(sample_elfs.keys())
				else:
					median_chosen = stat.median_high(sample_elfs.keys())
				med_elfs = sample_elfs[median_chosen]
				elf.setWrittenSchedule(med_elfs[randint(0,len(med_elfs)-1)])
				return elf
		else:
			lowest_unoccupied = min(excluded_sample_elfs.keys())
			low_elfs = excluded_sample_elfs[lowest_unoccupied]
			elf.setWrittenSchedule(low_elfs[randint(0,len(low_elfs)-1)])
			return elf

	def update_csv(elf):
		names = {}
		for row in [x[1] for x in elf.getWrittenSchedule()]:
			for item in row:
				if item != "BLANK":
					if item in names:
						names[item] += 1
					else:
						names[item] = 1

		filename = 'schedules/info.csv'
		tempfile = NamedTemporaryFile(mode='w', delete=False)

		fields = ['Name', 'Email', 'Num_Hours']

		with open(filename, 'r') as csvfile, tempfile:
		    reader = csv.DictReader(csvfile, fieldnames=fields)
		    writer = csv.DictWriter(tempfile, fieldnames=fields)
		    for row in reader:
		        if row['Name'] in names:
		            row['Num_Hours'] = float(row['Num_Hours']) + (0.5 * names[row['Name']])
		        row = {'Name': row['Name'], 'Email': row['Email'], 'Num_Hours': row['Num_Hours']}
		        writer.writerow(row)

		shutil.move(tempfile.name, filename)

	iter_input = params[6]

	text_out.append("## Sampling Information\n\n")
	text_out.append("Schedule Sample Size: " + str(iter_input) + "\n")

	def numCheck(inp):
		try:
			int(inp)
			return True
		except ValueError:
			return False

	while int(iter_input) < 1 and not numCheck(iter_input):
		print("\nPlease enter a nonzero number.\n")
		iter_input = params[6]

	elf = findOptimalELF(int(iter_input))
	update_csv(elf)

	if event_type == "single":
		elf.setWrittenSchedule(single_inverse(elf.getWrittenSchedule()))

	if event_type == "multi":
		elf.setWrittenSchedule(multiple_inverse(elf.getWrittenSchedule()))

	def writeFile():
		"""Creates the heading times for the schedule."""
		local_time = ((0 if hour == 12 else hour) \
			  + (12 if meridian == "PM" else 0)) * 2 \
			  + (1 if minute == 30 else 0) \
			  - 3
		local_times = []
		local_times.append("")
		for i in range(7):
			local_times.append(("12" if (int((local_time + i) / 2) % 12 == 0) else str(int((local_time + i) / 2) % 12)) + ":" \
							 + ("00" if ((local_time + i) % 2 == 0) else "30") \
							 + (" AM" if (local_time + i) < 24 else " PM"))
		"""Creates the directory for the ELF files."""
		dir_name = title
		if path.exists("./ELFs/" + dir_name):
			i = 1
			title_copy = dir_name
			while path.exists("./ELFs/" + dir_name):
				dir_name = title_copy + " (" + str(i) + ")"
				i += 1
		mkdir("./ELFs/" + dir_name)
		"""Creates the CSV file that holds the generated schedule."""
		schedule_file = open("./ELFs/" + dir_name + "/ELF.csv", "w")
		schedule_file.write(",".join(local_times))
		schedule_file.write("\n")
		for slot in elf.getWrittenSchedule():
			schedule_file.write(",".join([slot[0]] + slot[1]))
			schedule_file.write("\n")
		schedule_file.close()
		return dir_name
		
	def writeTable(dir_name):
		nonlocal text_out
		names_found = {}
		name_to_position = {}
		for slot in elf.getWrittenSchedule():
			shifts = slot[1]
			index = 0
			name_found = "BLANK"
			for shift in shifts:
				if shift not in ["BLANK", "NONE_AVAILABLE", "FILL_IN"]:
					name_found = shift
					if name_found not in name_to_position.keys():
						name_to_position[name_found] = [slot[0]]
					else:
						name_to_position[name_found] += [slot[0]]
					if name_found not in names_found.keys():
						names_found[name_found] = [index]
					else:
						names_found[name_found].append(index)
				index += 1
		name_keys = sorted(names_found.keys())
		table = []
		for name in name_keys:
			positions_temp = []
			for p in name_to_position[name]:
				if p not in positions_temp:
					positions_temp.append(p)
			position_name = " + ".join(positions_temp)
			start_time = names_found[name][0] + time_code + mem_time_code
			start_shift = ("12" if (int((start_time) / 2) % 12 == 0) else str(int((start_time) / 2) % 12)) + ":" \
						+ ("00" if ((start_time) % 2 == 0) else "30") \
						+ (" AM" if (start_time) < 24 else " PM")
			end_time = names_found[name][len(names_found[name])-1] + time_code + mem_time_code + 1
			end_shift = ("12" if (int((end_time) / 2) % 12 == 0) else str(int((end_time) / 2) % 12)) + ":" \
						+ ("00" if ((end_time) % 2 == 0) else "30") \
						+ (" AM" if (end_time) < 24 else " PM")
			email = list(filter(lambda person: person.getName() == name, people))[0].getEmail()
			entry = [name, position_name, start_shift, end_shift, email]
			table.append(entry)
		table_file = open("./ELFs/" + dir_name + "/table.csv", "w")
		table_file.write(",".join(["Name", "Position", "Shift Start Time", "Shift End Time", "Email"]))
		table_file.write("\n")
		for entry in table:
			table_file.write(",".join(entry))
			table_file.write("\n")
		table_file.close()
		"""Prints the table into the terminal."""
		print("\nAssignments:\n")
		text_out.append("\n## Assignments\n\n")
		for entry in table:
			print(" -- " + entry[0] + " for " + entry[1] + " at " + entry[2] + " - " + entry[3] + ".")
			text_out.append(" -- " + entry[0] + " for " + entry[1] + " at " + entry[2] + " - " + entry[3] + ".\n")
		print("\nSchedule generated successfully. The ELF's location is `ELFs/" + dir_name + "/ELF.csv`.\n")
		text_out.append("\nSchedule generated successfully. The ELF's location is `ELFs/" + dir_name + "/ELF.csv`.\n")

	def writeQueryInfo():
		query_file = open("./ELFs/" + dir_name + "/query.txt", "w")
		for line in text_out:
			query_file.write(line)
		query_file.close()

	dir_name = writeFile()
	writeTable(dir_name)
	writeQueryInfo()

if __name__ == "__main__":
    main()
