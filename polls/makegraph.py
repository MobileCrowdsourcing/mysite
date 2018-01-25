from models import ImageScenario, ImageChain
import pickle
import sys

try:
	fp = open('store/gs.p', 'rb')
except:
	print('Error : ' + str(sys.exc_info()[0]))
	exit()

dgraph = pickle.load(fp)
fp.close()

q = ImageChain.objects.all()
print(q)