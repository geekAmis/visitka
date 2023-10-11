from _init_ import *

def get_stofnum(num):
	spisok ='userid,fname,lname,uname,do,ocenka,otziv,otime,page'.split(',')
	return spisok[int(num)]

def voprs(data):  return ",".join(['?' for i in data])

class DB(object):
	"""docstring for DB"""
	def __init__(self, name):
		self.name = name + '.db'
		self.conn = sqlite3.connect(self.name,check_same_thread=False) # или :memory: чтобы сохранить в RAM
		self.cur = self.conn.cursor()
		self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
			userid INT PRIMARY KEY,
			fname TEXT,
			lname TEXT,
			uname TEXT,
			do TEXT,
			ocenka INT,
			otziv TEXT,
			otime TIME,
			page INT

		);""")
		print('Core [db] -> [__init__] -> Stable')

	def add_to_base(self,data):
		self.cur.execute(f"INSERT INTO users VALUES({voprs(data)});", data)
		self.conn.commit()


	def get_of_id(self,param):
		self.cur.execute("""SELECT * from users""")
		for row in self.cur.fetchall():
			if str(row[0]) == str(param):
				return row

	def change_per(self,idS,number_st,hanging_data):
		st=get_stofnum(number_st)
		sql = """UPDATE users
		SET {} = ? WHERE userid = ?""".format(st)

		self.cur.execute(sql, (f"{hanging_data}",idS))
		self.conn.commit()

	def get_all(self):
		records = self.cur.execute("""SELECT * from users""").fetchall();print(f"Всего строк:  ", len(records))
		return records

	def idS(self):
		return [i[0] for i in self.cur.execute("""SELECT * from users""").fetchall()]

	def ocens(self):
		return [i[5] for i in self.cur.execute("""SELECT * from users""").fetchall()]

	def text_split_ocens(self):
		return [str(i[0])+'_!!@!!_'+str(i[1])+'_!!@!!_'+str(i[5])+'_!!@!!_'+str(i[6])+'_!!@!!_'+str(i[7]) for i in self.cur.execute("""SELECT * from users""").fetchall()]
	

base = DB('base')

if (len(base.get_all()) < 1):
	base.add_to_base((
		admin,
		'Верховный',
		'Администратор',
		'Lilanga',
		'menu',
		'5',
		'Владелец бота,тестовый отзыв.',
		time.ctime(),
		0
	))