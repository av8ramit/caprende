'''
The key to solving this problem is to be creative and design classes and methods
that are both efficient and easily adjustable. Make a comprehensive list of features
and schema you support and then start mapping the idea you have into the code. Never simply
start coding without a solid plan. Consider new features that can highlight your ability to
think outside the box. Have fun with this question.
'''

class Account:
	'''
  	This is a basic account class for the new version of Amazon.
  '''

	def __init__(self, username, email):
		self.username = name
	  self.email = email
    self.orders = []

  def add_order(self, item):
    self.orders.append(item)

class Order:
  '''
    This is a basic order that occurs on our site.
  '''
  def __init__(self, buyer, seller, item):
    self.buyer = buyer
    self.seller = seller
    self.item = item
    self.time = time.now()
    self.refunded = False

  def refund_order():
    self.refunded = True
    #Initiate payment return

class Item:
  '''
    This is a basic item that is listed on our site.
  '''
  def __init__(self, name, price, description):
    self.name = name
    self.price = price
    self.item = item
    self.seller = seller
    self.rating = None
    self.ratings_given = 0
    self.reviews = []

  def add_rating(rating):
    self.rating = (self.rating + rating) / (self.ratings_given + 1)
    self.ratings_given += 1

  def word_finder(word, array):
    


  "6" : {
      "text" : "How would you design the data structures for a more basic version of Amazon?",
      "course" : "Coding",
      "section" : "Technical",
      "category" : "Concepts and Algorithms",
      "subcategory" : "System Design and Scalability",
      "passage" : "This question is designed to test your knowledge of fixing a problem in the real world and communicating it effectively.",
      "option_A" : "I feel confident with my answer with multiple ",
      "option_B" : "I was able to come up with an answer in theory, but unable to express it.",
      "option_C" : "I was unable to come up with an answer.",
      "option_D" : "",
      "option_E" : "",
      "answer_letter" : "A",
      "answer_explanation" : ""
  },


>>> def foo(html):
...     return html.replace('"', "'")