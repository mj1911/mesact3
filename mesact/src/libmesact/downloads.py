import os, tarfile, shutil, requests, subprocess
import urllib.request
from urllib.error import URLError, HTTPError
from functools import partial

from PyQt6.QtWidgets import QApplication, QFileDialog

from libmesact import firmware
from libmesact import dialogs
from libmesact import utilities

def url_exists(url):
	try:
		# Use a HEAD request to avoid downloading the entire page content
		req = urllib.request.Request(url, method='HEAD')
		with urllib.request.urlopen(req) as response:
			# Check if the status code indicates success (2xx range) or a redirect (3xx range)
			return 200 <= response.getcode() < 400, 'Success'
	except HTTPError as e:
		# Client error (e.g., 404 Not Found, 403 Forbidden) or server error (5xx)
		#print(f"HTTP Error: {e.code}")
		return False, e.code
	except URLError as e:
		# Other errors (e.g., connection issue, unknown host)
		#print(f"URL Error: {e.reason}")
		return False, e.reason
	except ValueError as e:
		# Invalid URL format (missing scheme, etc.)
		#print(f"Invalid URL: {e}")
		return False, e

def downloadFirmware(parent):
	board = parent.boardCB.currentData()
	if board:
		libpath = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}')
		#firmware_url = f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz'
		firmware_url = 'jethornton/mesact_firmware/releases/download/1.0.0/5i25ty.tar.xz'
		exists, error = url_exists(firmware_url)
		if exists:
			destination = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}.tar.xz')
			if os.path.isdir(libpath):
				subprocess.run(["rm", "-rf", libpath])
			download(parent, firmware_url, destination)
			with tarfile.open(destination) as f:
				f.extractall(libpath)
			if os.path.isfile(destination):
				os.remove(destination)
			# update firmware tab
			firmware.load(parent)
		else:
			msg = ('The url for the firmware returned\n'
			f'{error}\n'
			'there could be a network issue or possibly\n'
			'the programmer forgot to upload the firmware\n'
			'to https://github.com/jethornton/mesact_firmware')
			dialogs.msg_ok(msg, 'Download Firmware')
	else:
		dialogs.msg_ok('Select a Board', 'Board')

def download_deb(deb, parent):
	home_dir = os.path.expanduser("~") # Start in the user's home directory
	directory = QFileDialog.getExistingDirectory(parent, "Select Directory", home_dir)
	deb_name = {}

	if directory:
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa CT Version {repoVersion} {deb} Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + f'{deb}.deb')
		deb_url = f'https://github.com/jethornton/mesact2/releases/download/{repoVersion}/mesact_{repoVersion}_{deb}.deb'
		exists, error = url_exists(deb_url)
		if exists:
			download(parent, deb_url, destination)
			parent.statusbar.showMessage(f'Mesa CT Version {repoVersion} Download Complete')
			dialogs.msg_ok('Close the Configuration tool and reinstall', 'Download Complete')
		else:
			msg = ('The url for the deb file returned\n'
			f'{error}\n'
			'there could be a network issue or possibly\n'
			'the programmer forgot to upload the deb\n')
			dialogs.msg_ok(msg, 'Download Deb')

	else:
		parent.statusbar.showMessage('Download Cancled')



def downloadAmd64Deb(parent):

	dialog = QFileDialog(parent)
	dialog.setWindowTitle("Select a Directory")
	'''
	QFileDialog.FileMode.AnyFile: The user can select any file, including
	non-existent files. This is useful for "Save As" dialogs.
	QFileDialog.FileMode.ExistingFile: The user can only select existing files.
	QFileDialog.FileMode.Directory: The user can only select a directory.
	QFileDialog.FileMode.ExistingFiles: The user can select multiple existing files.
	'''
	dialog.setFileMode(QFileDialog.FileMode.Directory)
	if dialog.exec():
		directory = dialog.selectedFiles()[0]
		print("Selected Directory:", directory)

	return
	print(utilities.select_dir(parent))

	dir_path = QFileDialog.getExistingDirectory(
		parent=parent.dialog,
		caption="Select directory",
		directory=os.path.expanduser("~"),
		options=QFileDialog.Option.DontUseNativeDialog,
	)
	print(dir_path)


	parent.dialog.setWindowTitle("Select a File")
	'''
	QFileDialog.FileMode.AnyFile: The user can select any file, including
	non-existent files. This is useful for "Save As" dialogs.
	QFileDialog.FileMode.ExistingFile: The user can only select existing files.
	QFileDialog.FileMode.Directory: The user can only select a directory.
	QFileDialog.FileMode.ExistingFiles: The user can select multiple existing files.
	QFileDialog.FileMode.DirectoryOnly: The user can only select a directory,
	and no files will be displayed.
	'''


	parent.dialog.setFileMode(QFileDialog.FileMode.Directory)
	if parent.dialog.exec():
		filename = parent.dialog.selectedFiles()[0]
		print("Selected file:", filename)


	dialog = QFileDialog(parent)



	dir_path = QFileDialog.getExistingDirectory(
		parent=parent.widget,
		caption="Select directory",
		directory=os.path.expanduser("~"),
		options=QFileDialog.Option.DontUseNativeDialog,
	)
	print(dir_path)


	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} amd64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_amd64.deb')
		deb_url = f'https://github.com/jethornton/mesact2/releases/download/{repoVersion}/mesact_{repoVersion}_amd64.deb'
		exists, error = url_exists(deb_url)
		if exists:
			download(parent, deb_url, destination)
			parent.statusbar.showMessage(f'Mesa CT Version {repoVersion} Download Complete')
			dialogs.msg_ok('Close the Configuration tool and reinstall', 'Download Complete')
		else:
			msg = ('The url for the deb file returned\n'
			f'{error}\n'
			'there could be a network issue or possibly\n'
			'the programmer forgot to upload the deb\n')
			dialogs.msg_ok(msg, 'Download Deb')

	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArmhDeb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} armhf Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_armhf.deb')
		deb_url = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_armhf.deb'
		exists, error = url_exists(deb_url)
		if exists:
			download(parent, deb_url, destination)
			parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
			dialogs.msg_ok('Close the Configuration tool and reinstall', 'Download Complete')
		else:
			msg = ('The url for the deb file returned\n'
			f'{error}\n'
			'there could be a network issue or possibly\n'
			'the programmer forgot to upload the deb\n')
			dialogs.msg_ok(msg, 'Download Deb')

	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArm64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} arm64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_arm64.deb')
		deb_url = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_arm64.deb'
		exists, error = url_exists(deb_url)
		if exists:
			print('exists')
			download(parent, deb_url, destination)
			parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
			dialogs.msg_ok('Close the Configuration tool and reinstall', 'Download Complete')
		else:
			msg = ('The url for the deb file returned\n'
			f'{error}\n'
			'there could be a network issue or possibly\n'
			'the programmer forgot to upload the deb\n')
			dialogs.msg_ok(msg, 'Download Deb')
	else:
		parent.statusbar.showMessage('Download Cancled')

def download(parent, url, output_file):
	try:
		with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
			shutil.copyfileobj(response, out_file)
		print(f"File successfully downloaded and saved as: {output_file}")
	except urllib.error.URLError as e:
		print(f"Error downloading file: {e.reason}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")

	return

	def Handle_Progress(blocknum, blocksize, totalsize):
		# calculate the progress
		readed_data = blocknum * blocksize
		#if totalsize > 0:
		#	download_percentage = readed_data * 100 / totalsize
		#	parent.progressBar.setValue(int(download_percentage))
		#	QApplication.processEvents()
	urllib.request.urlretrieve(down_url, save_loc, Handle_Progress)
	parent.progressBar.setValue(100)
	parent.statusbar.showMessage('Download Complete')
	parent.timer.start(5000)

def clearProgressBar(parent):
	parent.progressBar.setValue(0)
	parent.statusbar.clearMessage()
	parent.timer.stop()


