import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from tkinter import filedialog
import threading


def on_complete(stream, file_path):
	loading.config(text=f'Download complete.')

def on_progress(stream, chunk, bytes_remaining):
	loading.config(text=f'Download started.....')
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining
	percentage_of_completion = (bytes_downloaded / total_size) * 100
	loading.config(text=f'Download progress: {percentage_of_completion:.2f}%')


firstclick = True
Folder_name = ""


def downloadfile():
	if Folder_name == "":
		error.config(text=f"Select download path")
		return
	order = combobox.current()
	if order is None:
		error.config(text=f"select a resolution")
		return
	#resetting the previous error to none
	error.config(text=f"")

	res = res_list[int(order)]
	task_thread = threading.Thread(target=video_download,args=[res])
	task_thread.start()


def video_download(res):
	"""Download video with the given resolution and save it to the given path"""
	video = yt.streams.get_by_resolution(res)
	video.download(Folder_name)


def OpenLocation():
	global Folder_name
	Folder_name = filedialog.askdirectory()
	if Folder_name != "":
		path_label.config(text=Folder_name, fg='orange')
	else:
		path_label.config(text="Please select a valid directory!", fg='red')


def on_entry_click(event):
	"""function that gets called whenever entry1 is clicked"""
	global firstclick
	if firstclick:   # if this is the first time they clicked it
		firstclick = False
		entry.delete(0, "end")   # delete all the text in the entry


def fetch_info():
	"""gives video link ,duration,thumbnail,video heading"""
	global link
	global yt

	# obtaining video link
	link = entry.get()
	try:
		yt = YouTube(url=link,on_complete_callback=on_complete, on_progress_callback=on_progress)

		# youtube title
		title.config(text=f"Title: {yt.title}")

		# video duration
		duration.config(text=f"Duration: {round((yt.length/60),2)} min")

		# video resolution
		streams = yt.streams.filter(progressive=True)
		global res_list
		res_list = []
		for stream in streams:
			res_list.append(stream.resolution)
		combobox['value'] = res_list
		combobox.current(0)

	except Exception as e:
		title.config(text=f"Invalid link")



def combobox_select(event):
	selected_res = combobox.get()
	file_mb = yt.streams.filter(resolution=selected_res).first().filesize_mb
	file_size.config(text=f"{file_mb}Mb")


def start_fetch_info():
    # Run fetch_info in a separate thread
    task_thread = threading.Thread(target=fetch_info)
    task_thread.start()

def on_combobox_select(event):
	thread_main = threading.Thread(target=combobox_select,args=[event])
	thread_main.start()






master = tk.Tk()

# window title
master.title("YouTube Converter")

# breadth and width of the master window
master.geometry('600x450')

# setting background color
master['background'] = '#474166'

# setting favicon
# master.wm_iconbitmap("images\icon_i.ico")

# frame1 with label Youtube converter
frame1 = tk.Frame(master, height=50)
frame1.pack()
l1 = tk.Label(frame1, pady=20, text='Youtube Converter', fg='white', bg='#474166', font=('calibre',20))
l1.pack()

# frame2 with label URL and
frame2 = tk.Frame(master)
frame2.pack()


# entry box

entry = tk.Entry(frame2)
entry.grid(row=0, column=0, ipadx=150, ipady=5, padx=2, pady=2)
entry.insert(0, 'Paste your video link here.')      # temp text in entry box
entry.bind('<FocusIn>', on_entry_click)         # removes the temp text when clicked

# convert button
b1 = tk.Button(frame2, text='Convert', bg='#f59300', fg='white', command=start_fetch_info)
b1.grid(row=0, column=1, ipady=1, padx=1, pady=2)

# frame3
frame3 = tk.Frame(master,bg='#474166')
frame3.pack()

details = tk.Label(frame3, text='Video Info',fg='white',bg='#474166',pady=10, font=('calibre',10,'bold'))
details.grid(row=0)

title = tk.Label(frame3, text='title',fg='white',bg='#474166')
title.grid(row=1)

duration = tk.Label(frame3, text="Duration:", fg='white',bg='#474166')
duration.grid(row=2)

Download_options = tk.Label(frame3, text='Download Options',fg='white',bg='#474166',pady=10, font=('calibre',10,'bold'))
Download_options.grid(row=3)

path_button = tk.Button(frame3, text='Select file path',command=OpenLocation)
path_button.grid(row=4)

path_label = tk.Label(frame3, text='Please select a file path', fg='green',bg='#474166')
path_label.grid(row=5)

v_quality = tk.Label(frame3, text='Select video quality', fg='white', bg='#474166',font=('calibre', 8, 'bold'),pady=5)
v_quality.grid(row=6)

global combobox

combobox = ttk.Combobox(frame3, width=5)
combobox.grid(row=7)
# Bind the <<ComboboxSelected>> event to the combobox
combobox.bind("<<ComboboxSelected>>", on_combobox_select)


file_size = tk.Label(frame3, text="filesize:",fg='white',bg='#474166',pady=5)
file_size.grid(row=8)

Download_button = tk.Button(frame3, text='Download file',padx=5,pady=4,command=downloadfile)
Download_button.grid(pady=5)

loading = tk.Label(frame3, fg='white',bg='#474166',font=('calibre',10,'bold'))
loading.grid(row=10)

error = tk.Label(frame3, fg='red',bg='#474166',font=('calibre',10,'bold'))
error.grid(row=11)


master.mainloop()
