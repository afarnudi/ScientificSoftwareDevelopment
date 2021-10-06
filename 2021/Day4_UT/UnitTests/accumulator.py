class Accumulator():
	"""Keep track of the sum of numbers and the last number added."""
	def __init__(self, initial_value):
		self.sum = initial_value
		self.last = initial_value

	def add(self, number):
		self.sum += number
