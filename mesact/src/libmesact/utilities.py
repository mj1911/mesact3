import os

from PyQt6.QtWidgets import QLineEdit, QComboBox, QDoubleSpinBox, QCheckBox
from PyQt6.QtWidgets import QApplication, QFileDialog

def new_config(parent):
	# set main tab visibility
	parent.mainTW.setTabVisible(3, False)
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)
	parent.mainTW.setTabVisible(6, False)
	parent.mainTW.setTabVisible(7, False)

	# clear all entries
	for child in parent.findChildren(QLineEdit):
		child.clear()
	for child in parent.findChildren(QComboBox):
		child.setCurrentIndex(0)
	for child in parent.findChildren(QDoubleSpinBox):
		child.setValue(0)
	for child in parent.findChildren(QCheckBox):
		child.setChecked(False)
	parent.servoPeriodSB.setValue(1000000)
	parent.introGraphicLE.setText('emc2.gif')
	parent.mainTW.setCurrentIndex(0)

def select_dir(parent):
	options = QFileDialog.Option.DontUseNativeDialog
	dir_path = False
	file_dialog = QFileDialog()
	print('here')
	file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
	file_dialog.setOptions(QFileDialog.Option.DontUseNativeDialog)
	file_dialog.setWindowTitle('Open File')
	dir_path, file_type = file_dialog.getOpenFileName(None,
	caption=caption, directory=parent.nc_code_dir,
	filter=parent.ext_filter, options=options)
	if dir_path:
		return dir_path
	else:
		return False

def open_manual(parent):
	if parent.installed:
		doc = os.path.join(parent.docs_path, 'mesact.pdf.gz')
	else:
		doc = os.path.join(parent.docs_path, 'mesact.pdf')
	subprocess.call(('xdg-open', doc))

def machine_name_changed(parent, text):
	if text:
		parent.machine_name_underscored = text.replace(' ','_').lower()
		parent.configPath = os.path.expanduser('~/linuxcnc/configs') + '/' + parent.machine_name_underscored
		parent.config_path_lb.setText(parent.configPath)
	else:
		parent.pathLabel.setText('')


