

from PyQt5.QtWidgets import QLineEdit, QComboBox, QDoubleSpinBox, QCheckBox

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


