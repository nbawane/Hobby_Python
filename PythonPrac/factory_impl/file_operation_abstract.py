#abstract factory impl for file ooperation

class input_op:
	def read(self):
		pass

	def open_file(self):
		pass


class output_op:
	def write(self):
		pass

	def open_file(self):
		pass

class txtfile_ip(input_op):
	pass

class excel_ip(input_op):
	pass

class txtfile_op(output_op):
	pass

class excel_op(output_op):
	pass


