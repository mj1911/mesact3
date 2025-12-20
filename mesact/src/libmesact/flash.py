




def firmware_changed(parent):
	if parent.firmware_cb.currentData():
		parent.flash_pb.setEnabled(True)
		parent.reload_pb.setEnabled(True)
		parent.verify_pb.setEnabled(True)
	else:
		parent.flash_pb.setEnabled(False)
		parent.reload_pb.setEnabled(False)
		parent.verify_pb.setEnabled(False)










