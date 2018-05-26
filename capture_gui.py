from Tkinter import *
import subprocess


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.start_capture = Button(frame, text="Start Still Image Capture", command=self.run_capture, height=20, width=30)
        self.start_capture.pack(side=LEFT)

        self.stop = Button(frame, text="Stop", fg="red", command=frame.quit, height=20, width=30)
        self.stop.pack(side=LEFT)

        self.start_record = Button(frame, text="Start Looped Recording", command=self.run_record, height=20, width=30)
        self.start_record.pack()

    def run_capture(self):
        i = 0
        while i < 4:
            subprocess.Popen(["python", "capture.py", str(i), '3', '10'])
            i = i + 1     

    def run_record(self):
        subprocess.call(["python", "record2.py"])

root = Tk()
root.geometry("800x500")
app = App(root)
root.mainloop()
root.destroy()
