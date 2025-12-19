import os, requests, subprocess, tarfile

from functools import partial

import urllib.request
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog

from libmesact import dialogs
from libmesact import firmware

class Downloader(QThread):
	# Signals for communication with the main GUI thread
	setTotalProgress = pyqtSignal(int)
	setCurrentProgress = pyqtSignal(int)
	succeeded = pyqtSignal()
	failed = pyqtSignal(str)

	def __init__(self, url, filename):
		super().__init__()
		self._url = url
		self._filename = filename

	def run(self):
		try:
			with urllib.request.urlopen(self._url) as response, open(self._filename, 'wb') as out_file:
				# Get total size from headers
				meta = response.info()
				if 'Content-Length' in meta:
					total_size = int(meta['Content-Length'])
					self.setTotalProgress.emit(total_size)
				else:
					# Handle cases where content-length is unknown
					total_size = None
					self.setTotalProgress.emit(0) # or handle as indeterminate

				read_bytes = 0
				chunk_size = 8192 # Read in chunks
				while True:
					chunk = response.read(chunk_size)
					if not chunk:
						break
					out_file.write(chunk)
					read_bytes += len(chunk)
					self.setCurrentProgress.emit(read_bytes) # Update progress bar value
				self.succeeded.emit()
		except Exception as e:
			self.failed.emit(f'Download failed: {e}')

def download_firmware(parent):
	# print(f' {}')
	board = parent.board_cb.currentData()
	if board:
		url = f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz'
		exists, error = url_exists(url)
		if exists:
			destination = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}.tar.xz')
			lib_path = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}')
			if os.path.isdir(lib_path): # delete the directory and files
				subprocess.run(["rm", "-rf", lib_path])

			# Initialize and run the downloader thread
			parent.downloader = Downloader(url, destination)
			parent.downloader.setTotalProgress.connect(partial(set_max_progress, parent))
			parent.downloader.setCurrentProgress.connect(partial(update_progress, parent))
			parent.downloader.succeeded.connect(partial(download_firmware_succeeded, destination, lib_path, parent))
			parent.downloader.failed.connect(partial(download_failed, parent))
			parent.downloader.start()
	else:
		dialogs.msg_ok(parent, 'Select a Board\nto download firmware', 'Firmware Download')

def download_deb(parent, deb):
	home_dir = os.path.expanduser("~") # Start in the user's home directory
	directory = QFileDialog.getExistingDirectory(parent, "Select Directory", home_dir)

	if directory:
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa CT Version {repoVersion} {deb} Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + f'{deb}.deb')
		url = f'https://github.com/jethornton/mesact2/releases/download/{repoVersion}/mesact_{repoVersion}_{deb}.deb'

	# Initialize and run the downloader thread
	parent.downloader = Downloader(url, destination)
	parent.downloader.setTotalProgress.connect(partial(set_max_progress, parent))
	parent.downloader.setCurrentProgress.connect(partial(update_progress, parent))
	parent.downloader.succeeded.connect(partial(download_succeeded, parent))
	parent.downloader.failed.connect(partial(download_failed, parent))
	parent.downloader.start()

def download_manual(manual, parent):
	home_dir = os.path.expanduser("~") # Start in the user's home directory
	directory = QFileDialog.getExistingDirectory(parent, "Select Directory", home_dir)

	if directory:
		destination = os.path.join(directory, manual)
		url = f'http://www.mesanet.com/pdf/parallel/{manual}'

	# Initialize and run the downloader thread
	parent.downloader = Downloader(url, destination)
	parent.downloader.setTotalProgress.connect(partial(set_max_progress, parent))
	parent.downloader.setCurrentProgress.connect(partial(update_progress, parent))
	parent.downloader.succeeded.connect(partial(download_succeeded, parent))
	parent.downloader.failed.connect(partial(download_failed, parent))
	parent.downloader.start()

def set_max_progress(parent, total_size):
	# Set the maximum value of the progress bar
	if total_size > 0:
		parent.progress_bar.setRange(0, total_size)
	else:
		parent.progress_bar.setRange(0, 0) # Indeterminate state if size unknown

def update_progress(parent, bytes_read):
	# Update the current value of the progress bar
	parent.progress_bar.setValue(bytes_read)

def download_firmware_succeeded(destination, lib_path, parent):
	with tarfile.open(destination) as f:
		f.extractall(lib_path)
	if os.path.isfile(destination):
		os.remove(destination)
	firmware.load(parent) # update firmware tab
	result = dialogs.msg_ok(parent, 'Download Complete', 'File Download')
	parent.progress_bar.setValue(0)
	parent.statusbar.showMessage('Download Complete')

def download_succeeded(parent):
	#self.label.setText("Status: Download Complete!")
	#self.button.setEnabled(True)
	parent.progress_bar.setValue(parent.progress_bar.maximum())
	result = dialogs.msg_ok(parent, 'Download Complete', 'File Download')
	parent.progress_bar.setValue(0)
	parent.statusbar.showMessage('Download Complete')

def download_failed(parent, failure):
	dialogs.msg_ok(parent, failure, 'HTTP Error')
	parent.statusbar.showMessage(failure)


