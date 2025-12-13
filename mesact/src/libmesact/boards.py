

from libmesact import utilities
from libmesact import firmware

def boardChanged(parent, index):

	if index > 0: # set common items for all boards
		parent.board_name = parent.boardCB.currentText()
		parent.board_hal_name = parent.boardCB.currentData()
		parent.mainTW.setTabVisible(3, True)
		parent.mainTW.setTabText(3, parent.board_name)
		parent.c0_JointTW.setTabText(0, parent.board_name)
		if parent.mesaflash:
			parent.read_hmid_gb.setEnabled(True)
			firmware.load(parent)



	match index:
		case 0:
			print('no board selected')
			address(parent, None)
			daughter_boards(parent, None , None)
			parent.mainTW.setTabVisible(3, False)
			parent.board_name = None
			parent.board_hal_name = None
			parent.mesaflash_name = None
		case 1: # 5i25
			print('5i25 selected')
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_io(parent, None, False, False, None, False)
			parent.mesaflash_name = '5i25'
		case 2: # 5i25T
			print('5i25T selected')
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_io(parent, None, False, False, None, False)
			parent.mesaflash_name = '5i25t'
		case 3: # 6i25
			print('6i25 selected')
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_io(parent, None, False, False, None, False)
			parent.mesaflash_name = '5i25'
		case 4: # 7c80
			print('7c80 selected')
			address(parent, 'spi')
			# FIXME dunno what daughter boards there are
			daughter_boards(parent, None , None)
			set_io(parent, None, False, False, None, False)
			parent.mesaflash_name = '7c80'
		case 5: # 7c81
			print('7c81 selected')
			address(parent, 'spi')
			# FIXME dunno what daughter boards there are
			daughter_boards(parent, None , None)
			set_io(parent, None, False, False, None, False)
			parent.mesaflash_name = '7c81'
		case 6: # 7i76E 5 step/dir 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			print('7i76E selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_io(parent, 32, True, False, 16, True)
			parent.mesaflash_name = '7i76e'
		case 7: # 7i76EU
			print('7i76EU selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P3')
			parent.mesaflash_name = '7i76eu'
		case 8: # 7i92
			print('7i92 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			parent.mesaflash_name = '7i92'
		case 9: # 7i92T
			print('7i92T selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			parent.mesaflash_name = '7i92t'
		case 10: # 7i93
			print('7i93 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			parent.mesaflash_name = '7i93'
		case 11: # 7i95
			print('7i95 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			parent.mesaflash_name = '7i95'
		case 12: # 7i95T
			print('7i95T selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			parent.mesaflash_name = '7i95t'
		case 13: # 7i96
			print('7i96 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			parent.mesaflash_name = '7i96'
		case 14: # 7i96S
			print('7i96S selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			parent.mesaflash_name = '7i96s'
		case 15: # 7i97
			print('7i97 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			parent.mesaflash_name = '7i97'
		case 16: # 7i97T
			address(parent, 'ip')
			print('7i97T selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P2' , None)
			parent.mesaflash_name = '7i97t'
		case 17: # 7i98
			print('7i98 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			parent.mesaflash_name = '7i98'


def address(parent, type):
	match type:
		case 'ip':
			ip_address = [
			['Select', False],
			['10.10.10.10', '10.10.10.10'],
			['192.168.1.121', '192.168.1.121']
			]
			parent.address_cb.clear()
			for item in ip_address:
				parent.address_cb.addItem(item[0], item[1])
			parent.address_cb.setEditable(True)
			parent.address_cb.setEnabled(True)
			parent.address_lb.setText('IP Address')
		case 'spi':
			spi_address = [
			['Select', False],
			['/dev/spidev0.0', '/dev/spidev0.0']]
			parent.address_cb.clear()
			for item in spi_address:
				parent.address_cb.addItem(item[0], item[1])
			parent.address_cb.setEditable(True)
			parent.address_cb.setEnabled(True)
			parent.address_lb.setText('SPI Address')
		case None:
			parent.address_cb.clear()
			parent.address_cb.setEditable(False)
			parent.address_cb.setEnabled(False)
			parent.address_lb.setText('N/A')

def daughter_boards(parent, port_1 , port_2):
	boards = [
	['Select', None],
	['7i76', '7i76'],
	['7i77', '7i77'],
	['7i78', '7i78'],
	['7i85', '7i85'],
	['7i85S', '7i85s']
	]
	parent.daughterCB_0.clear()
	parent.daughterLB_0.clear()
	parent.daughterCB_1.clear()
	parent.daughterLB_1.clear()

	if port_1:
		parent.daughterLB_0.setText(port_1)
		for item in boards:
			parent.daughterCB_0.addItem(item[0], item[1])

	if port_2:
		parent.daughterLB_1.setText(port_2)
		for item in boards:
			parent.daughterCB_1.addItem(item[0], item[1])

def set_io(parent, inputs, i_invert, i_debounce, outputs, o_invert):
	# inputs, input invert, input debounce, outputs, output invert
	# first thing set all to disabled
	for i in range(32):
		getattr(parent, f'c0_input_{i}').setEnabled(False)
		getattr(parent, f'c0_input_invert_{i}').setEnabled(False)
		getattr(parent, f'c0_input_debounce_{i}').setEnabled(False)
	for i in range(16):
		getattr(parent, f'c0_output_{i}').setEnabled(False)
		getattr(parent, f'c0_output_invert_{i}').setEnabled(False)

	if inputs:
		parent.c0_JointTW.setTabVisible(7, True)
		for i in range(inputs):
			getattr(parent, f'c0_input_{i}').setEnabled(True)
			if i_invert:
				getattr(parent, f'c0_input_invert_{i}').setEnabled(True)
			if i_debounce:
				getattr(parent, f'c0_input_debounce_{i}').setEnabled(True)
	else:
		parent.c0_JointTW.setTabVisible(7, False)
	if outputs:
		parent.c0_JointTW.setTabVisible(8, True)
		for i in range(outputs):
			getattr(parent, f'c0_output_{i}').setEnabled(True)
			if o_invert:
				getattr(parent, f'c0_output_invert_{i}').setEnabled(True)
	else:
		parent.c0_JointTW.setTabVisible(8, False)




