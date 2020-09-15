import json
import os
import argparse
import datetime

now_time1 = datetime.datetime.now()

def outputFile(file_address):
	Users = {}
	Repos = {}
	UsersAndRepos = {}
	json_list = []
	for root, dic, files in os.walk(file_address):
		for file in files:
			if(file[-5:] == '.json'):
				x = open(file_address + '\\' + file, 'r', encoding = 'utf-8').read()
				for line in x.split('\n'):
					if(len(line)>0):
						try:
							json_list.append(json.loads(line))
						except:
							pass

	for i in json_list:
		EventType = i.get('type',0)
		EventUser = i.get('actor',0).get('login',0)
		EventRepo = i.get('repo',0).get('name',0)
		if(not Users.get(EventUser)):
			Users.update({EventUser: {}})
		if(not Users[EventUser].get(EventType)):
			Users[EventUser].update({EventType: 0})
		Users[EventUser][EventType] += 1

		if(not Repos.get(EventRepo)):
			Repos.update({EventRepo: {}})
		if(not Repos[EventRepo].get(EventType)):
			Repos[EventRepo].update({EventType: 0})
		Repos[EventRepo][EventType] += 1


		if(not UsersAndRepos.get(EventUser)):
			UsersAndRepos.update({EventUser: {}})
		if(not UsersAndRepos[EventUser].get(EventRepo)):
			UsersAndRepos[EventUser].update({EventRepo: {}})
		if(not UsersAndRepos[EventUser][EventRepo].get(EventType)):
			UsersAndRepos[EventUser][EventRepo].update({EventType: 0})
		UsersAndRepos[EventUser][EventRepo][EventType] += 1

	with open('Users.json', 'w', encoding='utf-8') as f:
		json.dump(Users,f)
	with open('Repos.json', 'w', encoding='utf-8') as f:
		json.dump(Repos,f)
	with open('UsersAndRepos.json', 'w', encoding='utf-8') as f:
		json.dump(UsersAndRepos,f)


	now_time2 = datetime.datetime.now()
	print(now_time2 - now_time1)


def getEventsRepos(repo, event):
	if(not os.path.exists('Repos.json')):
		print("ERROR: please init first!")
		return 0
	x = open('Repos.json', 'r', encoding='utf-8').read()
	file = json.loads(x)
	if(not file.get(repo,0)):
		print("no")
	else:
		print(file[repo].get(event,0))

def getEventsUsers(user, event):
	if(not os.path.exists('Repos.json')):
		print("ERROR: please init first!")
		return 0
	x = open('Users.json', 'r', encoding='utf-8').read()
	file = json.loads(x)
	if(not file.get(user,0)):
		print("no")
	else:
		print(file[user].get(event,0))

def getEventsUsersAndRepos(user, repo, event):
	if(not os.path.exists('Repos.json')):
		print("ERROR: please init first!")
		return 0
	x = open('UsersAndRepos.json', 'r', encoding='utf-8').read()
	file = json.loads(x)
	if(not file.get(user,0)):
		print("no")
	elif(not file[user].get(repo)):
		print("no 2")
	else:
		print(file[user][repo].get(event,0))



class RunFirst:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.argInit()
		self.analyse()

	def argInit(self):
		self.parser.add_argument('-i', '--init')
		self.parser.add_argument('-u', '--user')
		self.parser.add_argument('-r', '--repo')
		self.parser.add_argument('-e', '--event')

	def analyse(self):
		if(self.parser.parse_args().init):
			outputFile(self.parser.parse_args().init)
			return 0
		else:
			if(self.parser.parse_args().event):
				if(self.parser.parse_args().user):
					if(self.parser.parse_args().repo):
						getEventsUsersAndRepos(
							self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
					else:
						getEventsUsers(
							self.parser.parse_args().user, self.parser.parse_args().event)
				elif(self.parser.parse_args().repo):
					getEventsRepos(
						self.parser.parse_args().reop, self.parser.parse_args().event)
				else:
					print('ERROR: argument -l or -c are required')
					return 0
			else:
				print('ERROR: argument -e is required')
				return 0

if __name__ == '__main__':
	Run = RunFirst()