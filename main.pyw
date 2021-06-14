import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from tkinter import filedialog

firstclick = True
Folder_name = ""


def download():
	order = combobox.current()
	choice = res_list[order]
	if choice == 'Audio':
		audio_download()
	else:
		video_download(choice)


def audio_download():
	"""Download audio file to the and save to given path"""
	global file_size
	youtube = YouTube(url=link)
	audio = youtube.streams.get_audio_only()
	audio.download(output_path=Folder_name)


def video_download(res):
	"""Download video with the given resolution and save it to the given path"""
	global file_size
	youtube = YouTube(url=link)
	video = youtube.streams.get_by_resolution(res)
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

	# obtaining video link
	link = entry.get()
	print(link)
	yt = YouTube(url=link)

	# youtube title
	title.config(text=f"Title: {yt.title}")

	# video duration
	duration.config(text=f"Duration: {(yt.length/60)} min")

	# video resolution
	global high_res, low_res, res_start, res_end, res_list
	res_list = ["720p", "480p", "360p", "240p", "144p"]
	high = str(yt.streams.get_highest_resolution())
	low = str(yt.streams.get_lowest_resolution())
	l_start = str(low).find('res=')
	h_start = str(high).find('res=')

	if h_start != -1:
		high_res = str(high[h_start + 5:h_start + 9])
	if l_start != -1:
		low_res = str(low[l_start + 5:h_start + 9])

	for i in range(len(res_list)):
		if high_res == res_list[i]:
			res_start = i
		if low_res == res_list[i]:
			res_end = i
	res_list = res_list[res_start:res_end + 1]
	res_list.append('Audio')

	# combobox
	global combobox
	combobox = ttk.Combobox(frame3, width=5)
	combobox['value'] = res_list
	combobox.current(0)
	combobox.grid(row=7)



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
b1 = tk.Button(frame2, text='Convert', bg='#f59300', fg='white', command=fetch_info)
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


file_size = tk.Label(frame3, text="filesize:",fg='white',bg='#474166',pady=5)
file_size.grid(row=8)

Download_button = tk.Button(frame3, text='Download file',padx=5,pady=4,command=download)
Download_button.grid(pady=5)


master.mainloop()
