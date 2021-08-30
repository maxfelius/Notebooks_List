import unittest
import process_arc_flagging
import pandas as pd
import datetime

# https://www.youtube.com/watch?v=6tNS--WetLI&ab_channel=CoreySchafer

class TestFlag(unittest.TestCase):

	def test_get_delta_day(self):
		# epochs = ['d_20151120','d_20151202','d_20151214','d_20151226','d_20160107','d_20160131','d_20160212','d_20160224','d_20160307','d_20160319','d_20160331','d_20160412','d_20160424']
		epochs = ['d_20151214','d_20151226']
		result_days, result_start = process_arc_flagging.process_arc_flagging.get_delta_day(None,epochs)
		self.assertEqual(result_days[0],0)
		self.assertEqual(result_days[1],12)
		self.assertEqual(result_start,datetime.datetime(2015, 12, 14, 0, 0))

	def test_check_earlier_flags(self):
		# row

		# rnum = process_arc_flagging.process_arc_flagging.check_earlier_flags(self,row,latest_epoch)
		pass

	def test_flagging(self):
		#doesnt work yet, have to watch the video further

		a = 1
		b = 1
		y = 2
		sigma_ehat = 2
		delta_day = 12
		rnum = process_arc_flagging.process_arc_flagging.flagging(self,a,b,y,sigma_ehat,delta_day)
		self.assertEqual(rnum,1)

if __name__ == '__main__':
	unittest.main()