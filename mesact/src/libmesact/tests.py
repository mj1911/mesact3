
from functools import partial

from libmesact import dialogs

def connect(parent):
	parent.msg_open_abort_cancel_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_open_cancel_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_cancel_ok_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_error_ok_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_question_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_yes_no_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_yes_no_check_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_ok_pb.clicked.connect(partial(test_dialogs, parent))

def test_dialogs(parent):
	name = parent.sender().objectName()
	match name:
		case 'msg_open_abort_cancel_pb':
			result = dialogs.msg_open_abort_cancel('Test', 'Title')
			print(result)
		case 'msg_open_cancel_pb':
			result = dialogs.msg_open_cancel('Test', 'Title')
			print(result)
		case 'msg_cancel_ok_pb':
			result = dialogs.msg_cancel_ok('Test', 'Title')
			print(result)
		case 'msg_error_ok_pb':
			result = dialogs.msg_error_ok('Test', 'Title')
			print(result)
		case 'msg_question_pb':
			result = dialogs.msg_question('Test', 'Title')
			print(result)
		case 'msg_yes_no_pb':
			result = dialogs.msg_yes_no('Test', 'Title')
			print(result)
		case 'msg_yes_no_check_pb':
			result = dialogs.msg_yes_no_check('Test', 'Title', 'Text')
			print(result)
		case 'msg_ok_pb':
			result = dialogs.msg_ok('Test', 'Title')
			print(result)



