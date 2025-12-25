
from libmesact import check

def build(parent):
	if not check.checkit(parent):
		return

	if parent.backup_cb.isChecked():
		utilities.backup_files(parent)




