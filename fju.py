from bs4 import BeautifulSoup
import requests
import re
import json
import time, math


class Table_manager():
	def __init__(self, value_list, key_list):
		self.key_list = key_list
		self.value_list = value_list
		self.tmp_dict = {}

	def remove_some_column(self, table_data, need_remove):
		tmp_list = []
		for i in table_data:
			if self.remove_space(i.get_text()) not in need_remove:
			 	tmp_list.append(i)
		self.value_list = tmp_list	
			
	def manage_dict(self):
		for key, value in zip(self.key_list, self.value_list):
			self.tmp_dict[key] = self.remove_space(value.get_text())

	def remove_space(self, string_data):
		return string_data.replace("\r", "").replace(" ", "").replace("\n", "").replace(u'\xa0', u'')


headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

all_data = {
	'__EVENTTARGET': '',
	'__EVENTARGUMENT': '',
	'__LASTFOCUS': '',
	'__VIEWSTATE': '/wEPDwUJNjM0NjczNTA5D2QWAgIBD2QWFAIDD2QWBAINDw8WAh4EVGV4dGVkZAIPDw8WAh8ABQRCYXNlZGQCBQ8PFgIeB1Zpc2libGVnZBYGAgEPEGRkFgECAWQCAw8QDxYGHg1EYXRhVGV4dEZpZWxkBQZEcHRDbmEeDkRhdGFWYWx1ZUZpZWxkBQVEcHRObx4LXyFEYXRhQm91bmRnZBAVXQpBbGwt5YWo6YOoEjAxLeS4reWci+aWh+WtuOezuw8wMi3mrbflj7Llrbjns7sMMDMt5ZOy5a2457O7FTBFLeS8gealreeuoeeQhuWtuOezux4wRi3ph5Hono3oiIflnIvpmpvkvIHmpa3lrbjns7skMEwt5aSp5Li75pWZ56CU5L+u5a245aOr5a245L2N5a2456iLMDBWLeaVmeiCsumgmOWwjuiIh+enkeaKgOeZvOWxleWtuOWjq+WtuOS9jeWtuOeoizAwVy3phqvlrbjos4foqIroiIflibXmlrDmh4nnlKjlrbjlo6vlrbjkvY3lrbjnqIsVMTAt5ZyW5pu46LOH6KiK5a2457O7FTExLeW9seWDj+WCs+aSreWtuOezuxUxMi3mlrDogZ7lgrPmkq3lrbjns7sVMTMt5buj5ZGK5YKz5pKt5a2457O7GzE2LemrlOiCsuWtuOezu+mrlOiCsuWtuOe1hB4xNy3pq5TogrLlrbjns7vpgYvli5Xnq7bmioDntYQkMTgt6auU6IKy5a2457O76YGL5YuV5YGl5bq3566h55CG57WEGzFCLeaVuOWtuOezu+izh+ioiuaVuOWtuOe1hBUyMC3oi7HlnIvoqp7mloflrbjns7sVMjIt5rOV5ZyL6Kqe5paH5a2457O7GDIzLeilv+ePreeJmeiqnuaWh+WtuOezuxUyNC3ml6XmnKzoqp7mloflrbjns7sYMjUt576p5aSn5Yip6Kqe5paH5a2457O7FTI2LeW+t+iqnuiqnuaWh+WtuOezuxgzMC3mlbjlrbjns7vntJTmlbjlrbjntYQbMzEt5pW45a2457O75oeJ55So5pW45a2457WEDDMzLeWMluWtuOezuw8zOS3lv4PnkIblrbjns7skNDYt57mU5ZOB5pyN6KOd5a2457O757mU5ZOB6Kit6KiI57WEKjQ4Lee5lOWTgeacjeijneWtuOezu+e5lOWTgeacjemjvuihjOmKt+e1hBU1MS3os4foqIrlt6XnqIvlrbjns7sSNTQt55Sf5ZG956eR5a2457O7GDU1LeeJqeeQhuWtuOezu+eJqeeQhue1hB41Ni3niannkIblrbjns7vlhYnpm7vniannkIbntYQVNTct6aSQ5peF566h55CG5a2457O7GDU4LeWFkuerpeiIh+WutuW6reWtuOezuw82My3npL7mnIPlrbjns7sVNjQt56S+5pyD5bel5L2c5a2457O7DzY1Lee2k+a/n+WtuOezuw82Ni3ms5Xlvovlrbjns7sVNjct6LKh57aT5rOV5b6L5a2457O7GDY4LeWtuOWjq+W+jOazleW+i+WtuOezuyQ2OS3nuZTlk4HmnI3oo53lrbjns7vmnI3po77oqK3oqIjntYQPNzEt5pyD6KiI5a2457O7FTc0Leizh+ioiueuoeeQhuWtuOezuxU3Ni3ntbHoqIjos4foqIrlrbjns7sPODAt6Z+z5qiC5a2457O7FTgxLeaHieeUqOe+juihk+WtuOezuxU4Mi3mma/op4DoqK3oqIjlrbjns7sSODUt6aOf5ZOB56eR5a2457O7Ejg2LeeHn+mkiuenkeWtuOezuzE4OS3pm7vmqZ/lt6XnqIvlrbjns7sgICAgICAgICAgICAgICAgICAgICAgICAgICAgDzkwLeWul+aVmeWtuOezuw85MS3orbfnkIblrbjns7sVOTIt5YWs5YWx6KGb55Sf5a2457O7DDk0LemGq+WtuOezuxU5NS3oh6jluorlv4PnkIblrbjns7sVOTYt6IG36IO95rK755mC5a2457O7FTk4LeWRvOWQuOayu+eZguWtuOezuxZLMDUt6Zu75a2Q5ZWG5YuZ5a2456iLE0swOS3ogIHkurrlrbjlrbjnqIsWSzEyLeiLseiqnuiPgeiLseWtuOeoix9LMTgt5aSW5Lqk6IiH5ZyL6Zqb5LqL5YuZ5a2456iLHEsxOS3lsI3lpJboj6/oqp7mlZnlrbjlrbjnqIslSzI3LeatkOebn+iqnuiogOiIh+aWh+WMlueglOeptuWtuOeoixxLMjgt6Zuy56uv5pyN5YuZ6Lao5Yui5a2456iLNEszMC3phqvlrbjlt6XnqIvlrbjliIblrbjnqIsgICAgICAgICAgICAgICAgICAgICAgICA3SzM3LeWkp+aVuOaTmueUoualreaZuuaFp+WtuOWIhuWtuOeoiyAgICAgICAgICAgICAgICAgIDhLNDAt5YuV5oWL6LOH6KiK6KaW6Ka66Kit6KiI5a245YiG5a2456iLICAgICAgICAgICAgICAgIDZLNDEt6auU5oSf5LqS5YuV6Kit6KiI5a245YiG5a2456iLICAgICAgICAgICAgICAgICAgICA2SzQ0LeenkeaKgOWJteaWsOWJtealreWtuOWIhuWtuOeoiyAgICAgICAgICAgICAgICAgICAgOUs0Ny3phqvkuovniK3orbDmup3pgJroiIfomZXnkIblrbjliIblrbjnqIsgICAgICAgICAgICAgIDdLNDkt5YSq6LOq6aCY5bCO6I+B6Iux5b6u5a245YiG5a2456iLICAgICAgICAgICAgICAgICAgK0s1MS3mqILpvaHmlrDlibXnlKLlk4HoqK3oqIjlvq7lrbjliIblrbjnqIsxSzU0LUFJ5b6u5a245YiG5a2456iLICAgICAgICAgICAgICAgICAgICAgICAgICAgIA9BVC3pq5TogrLoqrLnqIsJQ1Qt5ZyL5paHFUUgLeaVmeiCsuWtuOeoi+iqsueoiw9FVC3lsIjmpa3lgKvnkIYPRlQt5aSW6Kqe6Kqy56iLD0lULeWkp+WtuOWFpemWgA9MQy3oi7Hogb3oqrLnqIsPTFQt5Lq655Sf5ZOy5a24IU5ULeiHqueEtuenkeaKgOmgmOWfn+mAmuitmOiqsueoiyFQVC3kurrmlofol53ooZPpoJjln5/pgJrorZjoqrLnqIshU1Qt56S+5pyD56eR5a246aCY5Z+f6YCa6K2Y6Kqy56iLEkNHLeaWh+WtuOmZouiqsueoixVGRy3lpJboqp7lrbjpmaLoqrLnqIsVSEct5rCR55Sf5a246Zmi6Kqy56iLFUpHLeazleW+i+WtuOmZouiqsueoixVTRy3nkIblt6XlrbjpmaLoqrLnqIsVV0ct56S+5pyD5a246Zmi6Kqy56iLFVYgLeWFseWQjOiLseaWh+iqsueoiw9ZVC3ou43oqJPoqrLnqIsVXQpBbGwt5YWo6YOoAjAxAjAyAjAzAjBFAjBGAjBMAjBWAjBXAjEwAjExAjEyAjEzAjE2AjE3AjE4AjFCAjIwAjIyAjIzAjI0AjI1AjI2AjMwAjMxAjMzAjM5AjQ2AjQ4AjUxAjU0AjU1AjU2AjU3AjU4AjYzAjY0AjY1AjY2AjY3AjY4AjY5AjcxAjc0Ajc2AjgwAjgxAjgyAjg1Ajg2Ajg5AjkwAjkxAjkyAjk0Ajk1Ajk2Ajk4A0swNQNLMDkDSzEyA0sxOANLMTkDSzI3A0syOANLMzADSzM3A0s0MANLNDEDSzQ0A0s0NwNLNDkDSzUxA0s1NAJBVAJDVAFFAkVUAkZUAklUAkxDAkxUAk5UAlBUAlNUAkNHAkZHAkhHAkpHAlNHAldHAVYCWVQUKwNdZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgFmZAIFDxBkEBUBABUBABQrAwFnZGQCBw8PFgIfAWhkZAIJDw8WAh8BaGRkAgsPDxYCHwFoZBYEAgEPEGRkFgFmZAIDDxBkZBYAZAINDw8WAh8BaGQWBAIBDxBkZBYBZmQCAw8QZGQWAWZkAg8PDxYCHwFoZBYEAgEPEGRkFgFmZAIDDxBkZBYBZmQCEQ8PFgIfAWdkZAITDw8WAh8BaGRkAhUPDxYCHwFoZBYCAgEPPCsAEQEBEBYAFgAWAGQYAgUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFhAFCkNoZWNrQm94X1IFCkNoZWNrQm94X1MFCkNoZWNrQm94X0cFCkNoZWNrQm94X1QFCkNoZWNrQm94X1UFCkNoZWNrQm94X1cFDUNoZWNrQm94X0hhbGYFDUNoZWNrQm94X1llYXIFEENoZWNrQm94X091dEZsYWcFDENoZWNrQm94X1dLMQUMQ2hlY2tCb3hfV0syBQxDaGVja0JveF9XSzMFDENoZWNrQm94X1dLNAUMQ2hlY2tCb3hfV0s1BQxDaGVja0JveF9XSzYFDENoZWNrQm94X1dLNwUNR1ZfQ291cnNlTGlzdA9nZBbMS/Co7UwzmQnNoCWgPWZvm/W69fzawJMix+JJvvXn',
	'__VIEWSTATEGENERATOR':'9318C2AF',
	'__EVENTVALIDATION':'/wEWnQECisr5gA8C75WY9wwC/t+rqwQCguDiwAoCz+fwtAgCutCQtwMCj5vOyAICn/Tkpg4C0/Tkpg4C0vTkpg4C1vTkpg4C4/Tkpg4ClpvWrQkCnbfSygsChvSwwAUChvS0wAUChvSIwAUChvTA3QUChvTE3QUChvTs3QUChvSE3QUChvSY3QUCmfS8wAUCmfSwwAUCmfS0wAUCmfSIwAUCmfSEwAUCmfSYwAUCmfTcwwUCmfT03QUCmPS8wAUCmPS0wAUCmPSIwAUCmPSMwAUCmPSAwAUCmPSEwAUCm/S8wAUCm/SwwAUCm/SIwAUCm/TQwwUCmvSEwAUCmvTcwwUCnfSwwAUCnfSMwAUCnfSAwAUCnfSEwAUCnfSYwAUCnfTcwwUCnPSIwAUCnPSMwAUCnPSAwAUCnPSEwAUCnPSYwAUCnPTcwwUCnPTQwwUCn/SwwAUCn/SMwAUCn/SEwAUCjvS8wAUCjvSwwAUCjvS0wAUCjvSAwAUCjvSEwAUCjvTQwwUCgfS8wAUCgfSwwAUCgfS0wAUCgfSMwAUCgfSAwAUCgfSEwAUCgfTcwwUCkKb0iQcC1NXqiA0Co5qTyQYCsf7MvQMC1NXuiA0CqpSA4wsCsf7AvQMC6bXXlwICqpSE4wsC6bWrlAICjIPN4gwC/ciiow0CqpSY4wsC1NX6iA0CjIPB4gwC/cimow0CyfSM3QUCy/SM3QUCzfT8wwUCzfSM3QUCzPSM3QUC8fSM3QUC8vTI3QUC8vSM3QUC9PSM3QUC5vSM3QUC+/SM3QUCy/TY3QUCzPTY3QUC/vTY3QUC8PTY3QUC+/TY3QUC//TY3QUC/PT8wwUC4fSM3QUC25qCxQ0ClOOPvQkClOOTvQkClOPjvQkClOOnvQkClOOrvQkClOOjvQkCpJOQ0QcCpLjH9Q4C+afzgwQCkcXr7gkCzaqBgwUCzaqNgwUCzaqJgwUCzaq1gwUCzaqxgwUCzarZngUCzaq9gwUCzaq5gwUCzaqlgwUCzarhgAUCyqqBgwUCyqqNgwUCyqqJgwUCyqq1gwUCyqqxgwUCg8Xr7gkC36qBgwUC36qNgwUC36qJgwUC36q1gwUC36qxgwUC36rZngUC36q9gwUC36q5gwUC36qlgwUC36rhgAUC2KqBgwUC2KqNgwUC2KqJgwUC2Kq1gwUC2KqxgwUCrJ2sqwwCrJ3ovAYCrJ3U4Q0CrJ2Q8wcCrJ38lw8CrJ24qQkCrJ2kTgKslsmmBgKwlv3UD8IAiqG8qUsoxmbYbIgxsB60uEvCspfItzLY+QPhKxjz',
	'DDL_AvaDiv':'D',
	'DDL_Avadpt':'All-全部',
	'DDL_Class':'',
	'DDL_Section_S':'',
	'DDL_Section_E':'',
	'But_Run':'查詢（Search）'
}

csie_data = {
	'__VIEWSTATE':'/wEPDwUJNjM0NjczNTA5D2QWAgIBD2QWFAIDD2QWBAINDw8WAh4EVGV4dGVkZAIPDw8WAh8ABQRCYXNlZGQCBQ8PFgIeB1Zpc2libGVnZBYGAgEPEGRkFgECAWQCAw8QDxYGHg1EYXRhVGV4dEZpZWxkBQZEcHRDbmEeDkRhdGFWYWx1ZUZpZWxkBQVEcHRObx4LXyFEYXRhQm91bmRnZBAVXQpBbGwt5YWo6YOoEjAxLeS4reWci+aWh+WtuOezuw8wMi3mrbflj7Llrbjns7sMMDMt5ZOy5a2457O7FTBFLeS8gealreeuoeeQhuWtuOezux4wRi3ph5Hono3oiIflnIvpmpvkvIHmpa3lrbjns7skMEwt5aSp5Li75pWZ56CU5L+u5a245aOr5a245L2N5a2456iLMDBWLeaVmeiCsumgmOWwjuiIh+enkeaKgOeZvOWxleWtuOWjq+WtuOS9jeWtuOeoizAwVy3phqvlrbjos4foqIroiIflibXmlrDmh4nnlKjlrbjlo6vlrbjkvY3lrbjnqIsVMTAt5ZyW5pu46LOH6KiK5a2457O7FTExLeW9seWDj+WCs+aSreWtuOezuxUxMi3mlrDogZ7lgrPmkq3lrbjns7sVMTMt5buj5ZGK5YKz5pKt5a2457O7GzE2LemrlOiCsuWtuOezu+mrlOiCsuWtuOe1hB4xNy3pq5TogrLlrbjns7vpgYvli5Xnq7bmioDntYQkMTgt6auU6IKy5a2457O76YGL5YuV5YGl5bq3566h55CG57WEGzFCLeaVuOWtuOezu+izh+ioiuaVuOWtuOe1hBUyMC3oi7HlnIvoqp7mloflrbjns7sVMjIt5rOV5ZyL6Kqe5paH5a2457O7GDIzLeilv+ePreeJmeiqnuaWh+WtuOezuxUyNC3ml6XmnKzoqp7mloflrbjns7sYMjUt576p5aSn5Yip6Kqe5paH5a2457O7FTI2LeW+t+iqnuiqnuaWh+WtuOezuxgzMC3mlbjlrbjns7vntJTmlbjlrbjntYQbMzEt5pW45a2457O75oeJ55So5pW45a2457WEDDMzLeWMluWtuOezuw8zOS3lv4PnkIblrbjns7skNDYt57mU5ZOB5pyN6KOd5a2457O757mU5ZOB6Kit6KiI57WEKjQ4Lee5lOWTgeacjeijneWtuOezu+e5lOWTgeacjemjvuihjOmKt+e1hBU1MS3os4foqIrlt6XnqIvlrbjns7sSNTQt55Sf5ZG956eR5a2457O7GDU1LeeJqeeQhuWtuOezu+eJqeeQhue1hB41Ni3niannkIblrbjns7vlhYnpm7vniannkIbntYQVNTct6aSQ5peF566h55CG5a2457O7GDU4LeWFkuerpeiIh+WutuW6reWtuOezuw82My3npL7mnIPlrbjns7sVNjQt56S+5pyD5bel5L2c5a2457O7DzY1Lee2k+a/n+WtuOezuw82Ni3ms5Xlvovlrbjns7sVNjct6LKh57aT5rOV5b6L5a2457O7GDY4LeWtuOWjq+W+jOazleW+i+WtuOezuyQ2OS3nuZTlk4HmnI3oo53lrbjns7vmnI3po77oqK3oqIjntYQPNzEt5pyD6KiI5a2457O7FTc0Leizh+ioiueuoeeQhuWtuOezuxU3Ni3ntbHoqIjos4foqIrlrbjns7sPODAt6Z+z5qiC5a2457O7FTgxLeaHieeUqOe+juihk+WtuOezuxU4Mi3mma/op4DoqK3oqIjlrbjns7sSODUt6aOf5ZOB56eR5a2457O7Ejg2LeeHn+mkiuenkeWtuOezuzE4OS3pm7vmqZ/lt6XnqIvlrbjns7sgICAgICAgICAgICAgICAgICAgICAgICAgICAgDzkwLeWul+aVmeWtuOezuw85MS3orbfnkIblrbjns7sVOTIt5YWs5YWx6KGb55Sf5a2457O7DDk0LemGq+WtuOezuxU5NS3oh6jluorlv4PnkIblrbjns7sVOTYt6IG36IO95rK755mC5a2457O7FTk4LeWRvOWQuOayu+eZguWtuOezuxZLMDUt6Zu75a2Q5ZWG5YuZ5a2456iLE0swOS3ogIHkurrlrbjlrbjnqIsWSzEyLeiLseiqnuiPgeiLseWtuOeoix9LMTgt5aSW5Lqk6IiH5ZyL6Zqb5LqL5YuZ5a2456iLHEsxOS3lsI3lpJboj6/oqp7mlZnlrbjlrbjnqIslSzI3LeatkOebn+iqnuiogOiIh+aWh+WMlueglOeptuWtuOeoixxLMjgt6Zuy56uv5pyN5YuZ6Lao5Yui5a2456iLNEszMC3phqvlrbjlt6XnqIvlrbjliIblrbjnqIsgICAgICAgICAgICAgICAgICAgICAgICA3SzM3LeWkp+aVuOaTmueUoualreaZuuaFp+WtuOWIhuWtuOeoiyAgICAgICAgICAgICAgICAgIDhLNDAt5YuV5oWL6LOH6KiK6KaW6Ka66Kit6KiI5a245YiG5a2456iLICAgICAgICAgICAgICAgIDZLNDEt6auU5oSf5LqS5YuV6Kit6KiI5a245YiG5a2456iLICAgICAgICAgICAgICAgICAgICA2SzQ0LeenkeaKgOWJteaWsOWJtealreWtuOWIhuWtuOeoiyAgICAgICAgICAgICAgICAgICAgOUs0Ny3phqvkuovniK3orbDmup3pgJroiIfomZXnkIblrbjliIblrbjnqIsgICAgICAgICAgICAgIDdLNDkt5YSq6LOq6aCY5bCO6I+B6Iux5b6u5a245YiG5a2456iLICAgICAgICAgICAgICAgICAgK0s1MS3mqILpvaHmlrDlibXnlKLlk4HoqK3oqIjlvq7lrbjliIblrbjnqIsxSzU0LUFJ5b6u5a245YiG5a2456iLICAgICAgICAgICAgICAgICAgICAgICAgICAgIA9BVC3pq5TogrLoqrLnqIsJQ1Qt5ZyL5paHFUUgLeaVmeiCsuWtuOeoi+iqsueoiw9FVC3lsIjmpa3lgKvnkIYPRlQt5aSW6Kqe6Kqy56iLD0lULeWkp+WtuOWFpemWgA9MQy3oi7Hogb3oqrLnqIsPTFQt5Lq655Sf5ZOy5a24IU5ULeiHqueEtuenkeaKgOmgmOWfn+mAmuitmOiqsueoiyFQVC3kurrmlofol53ooZPpoJjln5/pgJrorZjoqrLnqIshU1Qt56S+5pyD56eR5a246aCY5Z+f6YCa6K2Y6Kqy56iLEkNHLeaWh+WtuOmZouiqsueoixVGRy3lpJboqp7lrbjpmaLoqrLnqIsVSEct5rCR55Sf5a246Zmi6Kqy56iLFUpHLeazleW+i+WtuOmZouiqsueoixVTRy3nkIblt6XlrbjpmaLoqrLnqIsVV0ct56S+5pyD5a246Zmi6Kqy56iLFVYgLeWFseWQjOiLseaWh+iqsueoiw9ZVC3ou43oqJPoqrLnqIsVXQpBbGwt5YWo6YOoAjAxAjAyAjAzAjBFAjBGAjBMAjBWAjBXAjEwAjExAjEyAjEzAjE2AjE3AjE4AjFCAjIwAjIyAjIzAjI0AjI1AjI2AjMwAjMxAjMzAjM5AjQ2AjQ4AjUxAjU0AjU1AjU2AjU3AjU4AjYzAjY0AjY1AjY2AjY3AjY4AjY5AjcxAjc0Ajc2AjgwAjgxAjgyAjg1Ajg2Ajg5AjkwAjkxAjkyAjk0Ajk1Ajk2Ajk4A0swNQNLMDkDSzEyA0sxOANLMTkDSzI3A0syOANLMzADSzM3A0s0MANLNDEDSzQ0A0s0NwNLNDkDSzUxA0s1NAJBVAJDVAFFAkVUAkZUAklUAkxDAkxUAk5UAlBUAlNUAkNHAkZHAkhHAkpHAlNHAldHAVYCWVQUKwNdZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgECHWQCBQ8QDxYGHwIFCENsYXNzQ25hHwMFB0NsYXNzTm8fBGdkEBUOCkFsbC3lhajpg6gONTEwMC3os4flt6Xns7sONTEwMS3os4flt6XkuIAONTEwMi3os4flt6XkuowONTEwMy3os4flt6XkuIkONTEwNC3os4flt6Xlm5sRNTExMS3os4flt6XkuIDnlLIRNTExMi3os4flt6XkuoznlLIRNTExMy3os4flt6XkuInnlLIRNTExNC3os4flt6Xlm5vnlLIRNTEyMS3os4flt6XkuIDkuZkRNTEyMi3os4flt6XkuozkuZkRNTEyMy3os4flt6XkuInkuZkRNTEyNC3os4flt6Xlm5vkuZkVDgpBbGwt5YWo6YOoBDUxMDAENTEwMQQ1MTAyBDUxMDMENTEwNAQ1MTExBDUxMTIENTExMwQ1MTE0BDUxMjEENTEyMgQ1MTIzBDUxMjQUKwMOZ2dnZ2dnZ2dnZ2dnZ2dkZAIHDw8WAh8BaGRkAgkPDxYCHwFoZGQCCw8PFgIfAWhkFgQCAQ8QZGQWAWZkAgMPEGRkFgBkAg0PDxYCHwFoZBYEAgEPEGRkFgFmZAIDDxBkZBYBZmQCDw8PFgIfAWhkFgQCAQ8QZGQWAWZkAgMPEGRkFgFmZAIRDw8WAh8BZ2RkAhMPDxYCHwFoZGQCFQ8PFgIfAWhkFgICAQ88KwARAQEQFgAWABYAZBgCBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WEAUKQ2hlY2tCb3hfUgUKQ2hlY2tCb3hfUwUKQ2hlY2tCb3hfRwUKQ2hlY2tCb3hfVAUKQ2hlY2tCb3hfVQUKQ2hlY2tCb3hfVwUNQ2hlY2tCb3hfSGFsZgUNQ2hlY2tCb3hfWWVhcgUQQ2hlY2tCb3hfT3V0RmxhZwUMQ2hlY2tCb3hfV0sxBQxDaGVja0JveF9XSzIFDENoZWNrQm94X1dLMwUMQ2hlY2tCb3hfV0s0BQxDaGVja0JveF9XSzUFDENoZWNrQm94X1dLNgUMQ2hlY2tCb3hfV0s3BQ1HVl9Db3Vyc2VMaXN0D2dkOpLBk0rul1fjWMJFPxPgffN5PaJj+1nl9cWKEhs5A6w=',
	'__VIEWSTATEGENERATOR':'9318C2AF',
	'__EVENTVALIDATION':'/wEWqgECxNXd0woC75WY9wwC/t+rqwQCguDiwAoCz+fwtAgCutCQtwMCj5vOyAICn/Tkpg4C0/Tkpg4C0vTkpg4C1vTkpg4C4/Tkpg4ClpvWrQkCnbfSygsChvSwwAUChvS0wAUChvSIwAUChvTA3QUChvTE3QUChvTs3QUChvSE3QUChvSY3QUCmfS8wAUCmfSwwAUCmfS0wAUCmfSIwAUCmfSEwAUCmfSYwAUCmfTcwwUCmfT03QUCmPS8wAUCmPS0wAUCmPSIwAUCmPSMwAUCmPSAwAUCmPSEwAUCm/S8wAUCm/SwwAUCm/SIwAUCm/TQwwUCmvSEwAUCmvTcwwUCnfSwwAUCnfSMwAUCnfSAwAUCnfSEwAUCnfSYwAUCnfTcwwUCnPSIwAUCnPSMwAUCnPSAwAUCnPSEwAUCnPSYwAUCnPTcwwUCnPTQwwUCn/SwwAUCn/SMwAUCn/SEwAUCjvS8wAUCjvSwwAUCjvS0wAUCjvSAwAUCjvSEwAUCjvTQwwUCgfS8wAUCgfSwwAUCgfS0wAUCgfSMwAUCgfSAwAUCgfSEwAUCgfTcwwUCkKb0iQcC1NXqiA0Co5qTyQYCsf7MvQMC1NXuiA0CqpSA4wsCsf7AvQMC6bXXlwICqpSE4wsC6bWrlAICjIPN4gwC/ciiow0CqpSY4wsC1NX6iA0CjIPB4gwC/cimow0CyfSM3QUCy/SM3QUCzfT8wwUCzfSM3QUCzPSM3QUC8fSM3QUC8vTI3QUC8vSM3QUC9PSM3QUC5vSM3QUC+/SM3QUCy/TY3QUCzPTY3QUC/vTY3QUC8PTY3QUC+/TY3QUC//TY3QUC/PT8wwUC4fSM3QUC0LaGog8C/rTLwg0C/rS36QoC/rSjlAMC/rSPswgC/rT7XwKbjdGEDAKbjb2jBQKbjanODQKbjZX1CgKAmvOTBgKAmt++DwKAmsvlBwKAmreADAKU44+9CQKU45O9CQKU4+O9CQKU46e9CQKU46u9CQKU46O9CQKkk5DRBwKkuMf1DgL5p/ODBAKRxevuCQLNqoGDBQLNqo2DBQLNqomDBQLNqrWDBQLNqrGDBQLNqtmeBQLNqr2DBQLNqrmDBQLNqqWDBQLNquGABQLKqoGDBQLKqo2DBQLKqomDBQLKqrWDBQLKqrGDBQKDxevuCQLfqoGDBQLfqo2DBQLfqomDBQLfqrWDBQLfqrGDBQLfqtmeBQLfqr2DBQLfqrmDBQLfqqWDBQLfquGABQLYqoGDBQLYqo2DBQLYqomDBQLYqrWDBQLYqrGDBQKsnayrDAKsnei8BgKsndThDQKsnZDzBwKsnfyXDwKsnbipCQKsnaROAqyWyaYGArCW/dQPGFFqjk+RfHS8XKnoV+WKTvAH7AVx+Si2VVxzdDycIEk=',
	'DDL_AvaDiv':'D',
	'DDL_Avadpt':'51',
	'DDL_Class':'All-全部',
	'DDL_Section_S':'',
	'DDL_Section_E':'',
	'But_Run':'查詢（Search）'
}


def write_txt(idx):
	f = open('t.txt', 'w', encoding='utf-8')
	for i in idx:
		f.write(str(i) + '\n')


def to_json(idx):
	f = open('fju.json', 'w', encoding='utf-8')
	f.write(json.dumps(idx, ensure_ascii=False))


def write_test(all_html):
	f = open('all.txt', 'w', encoding='utf-8')
	f.write(str(all_html))

def main():

	# start
	print('START')
	tStart = time.time()

	print('Parse HTML start')
	res = requests.post('http://estu.fju.edu.tw/fjucourse/firstpage.aspx', all_data)
	soup = BeautifulSoup(res.text, 'html.parser')


	# Cource table
	table = soup.find(id= "GV_CourseList")
	print('Parse HTML end')


	# get data
	title_bs4 = table.select('tr th')
	
	# for 處理重複名字column, like 週別,星期,節次...(重複三次)
	title = []
	list_counter = 1
	for i in title_bs4:
		if 15 <= list_counter and list_counter <= 18:
			title.append(i.get_text() + '2')
		elif 19 <= list_counter and list_counter <= 22:
			title.append(i.get_text() + '3')
		else:
			title.append(i.get_text())	
		list_counter = list_counter + 1


	# 課程內容list
	content_bs4 = table.select('tr td')
	content = []


	# all_data
	db = []
	col_cnt = 0

	# for message variable
	counter = 0
	now = 0

	# filt the data
	for i in content_bs4:
		
		if col_cnt == 0:
			dic = {}
			content = []

		if col_cnt == 28:

			counter += 1
			print("[{now}]".format(now=counter) + ' is finished')

			# reset
			col_cnt = 0
			dic = {}

			for key,value in zip(title,content):
				# print(key)
				# print(value)
				# print('---------')
				dic[key] = value
			db.append(dic)
			continue

		elif i.select('table tr td'):
			
			filt_select = i.select('table tr td span')
			if col_cnt == 4:
				tb = Table_manager(filt_select, ["中文", "英文"])
				tb.manage_dict()

			elif col_cnt == 8:
				tb = Table_manager(filt_select, ["教師", "專長"])
				tb.remove_some_column(filt_select, ["專長："])
				# print(tb.tmp_dict)
				tb.manage_dict()

			elif col_cnt == 24:
				tb = Table_manager(filt_select, ["最低年級", "最高年級", "分發優先順序"])
				tb.remove_some_column(filt_select, ["最低年級：",  "最高年級：", "分發優先順序："])
				tb.manage_dict()

			elif col_cnt == 25:
				tb = Table_manager(filt_select, ["開放", "外系", "屬性", "拒退年級"])
				tb.remove_some_column(filt_select, ["開放：",  "外系：", "屬性：", "拒退年級："])
				tb.manage_dict()

			elif col_cnt == 26:
				tb = Table_manager(filt_select, ["領域", "學群"])
				tb.remove_some_column(filt_select, ["領域：", "學群："])
				tb.manage_dict()

			content.append(tb.tmp_dict)

		elif i.select('td span'):
			continue
		elif i.select('td font'):
			content.append(i.get_text().replace("\r", "").replace(" ", "").replace("\n", "").replace(u'\xa0', u''))

		col_cnt = col_cnt + 1

	write_txt(db)
	to_json(db)


	tEnd = time.time()  # 計時結束
	print("END")
	print("You used:" + str(round(tEnd - tStart)) + "s")


if  __name__ == "__main__":
	main()
