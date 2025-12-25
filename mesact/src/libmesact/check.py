

def check_config(parent):
	print('here')

	config_errors = []
	tab_error = False
	next_header = 0

	# check the Machine Tab for errors
	if not parent.machine_name_le.text():
		tabError = True
		config_errors.append('\tA configuration name must be entered')
	if not parent.board_cb.currentData():
		tabError = True
		config_errors.append('\tA Board must be selected')

	if tabError:
		config_errors.insert(next_header, 'Machine Tab:')
		next_header = len(config_errors)
		tab_error = False
	# end of Machine Tab


	parent.info_pte.clear()
	parent.main_tw.setCurrentIndex(11)

	if config_errors:
		parent.info_pte.setPlainText('\n'.join(config_errors))
		return False
	else:
		parent.info_pte.setPlainText('Configuration checked OK')
		return True






