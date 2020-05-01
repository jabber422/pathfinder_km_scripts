import json
import zipfile
import glob
import os

classes = {
	'48ac8db94d5de7645906c7d0ad3bcfbd' : 'Fighter',
	'84643e02a764bff4a9c1aba333a53c89' : 'Two-Handed Figher',
	
	'67819271767a9dd4fbfd4ae700befea0' : 'Cleric',
	'c4a02990f15c0bb4d8749a90a5ed46b3' : 'Emp Healer',
	
	'f7d7eb166b3dd594fb330d085df41853' : 'Barbarian',
	'48277b221b6ba6e40affb1e9b49faf36' : 'Armored Ravager',
	
	'299aa766dee3cbf4790da4efb8c72484' : 'Rogue',
	'57f93dd8423c97c49989501281296c4a' : 'Eld Scoundrel',
	
	'0937bec61c0dabc468428f496580c721' : 'Alchemist',
	'6af888a7800b3e949a40f558ff204aae' : 'Grenadier',
	'68cbcd9fbf1fb1d489562f829bb97e38' : 'Vivisectionist',
	
	'45a4607686d96a1498891b3286121780' : 'Magus',
	'44388c01eb4a29d4d90a25cc0574320d' : 'Eld Archer',
	
	'e8f21e5b58e0569468e420ebea456124' : 'Monk',
	'f8767821ec805bf479706392fcc3394c' : 'Sensi',
	
	'ba34257984f4c41408ce1dc2004e342e' : 'Wizard',
	
	'cda0615668a6df14eb36ba19ee881af6' : 'Ranger',
	
	'772c83a25e2268e448e841dcd548235f' : 'Bard',
	'3c67fb6458752a1419fb8cd4efaf8eaa' : 'Thunder Caller',
	
	'00b990c8be2117e45ae6514ee4ef561c' : 'Slayer',
	
	'35a3b7bfc663ac74aa8bb50adfe70813' : 'Blight Druid',
	
	'c75e0971973957d4dbad24bc7957e4fb' : 'Sorcerer',
	
	'bfa11238e7ae3544bbeb4d0b92e897ec' : 'Paladin',
	'fec08c1a3187da549abd6b85f27e4432' : 'Divine Hunter',
	
	#'472af8cb3de628f4a805dc4a038971bc' : '?'
}

def isdict(map):
	for k,v in map.items():
		if isinstance(v, dict):
			if 'CustomName' in v and v['CustomName'] != '':
				print('Name: ' + v['CustomName'])
				for prog in v['Progression']['Classes']:
					for at in prog['Archetypes']:
						char_arch_type = classes.get(at,at)
						print(f"ArchType: {char_arch_type}, Level: {prog['Level']}")
						
					if len(prog['Archetypes']) == 0:
						char_class = classes.get(prog['CharacterClass'], prog['CharacterClass'])
						print(f"Class: {char_class}, Level: {prog['Level']}")
				
				for part in v['m_Parts']['m_Parts']:
					if part['Key'].startswith('Kingmaker.Dungeon.Leaderboard.UnitPartDungeonCharacterStats'):
						print('Total Out: ' + str(part['Value']['TotalDamageDealt']))
						print('Total In: ' + str(part['Value']['TotalDamageReceived']))
				print()
		check(v)
		
def check(value):
	if isinstance(value, list):
		for item in value:
			check(item)
	elif isinstance(value, dict):
		isdict(value)

user_input = True
if user_input:
#will extract all save files (.zks) to their own folders in cwd, then read each party.json
	saves_path = os.path.join(os.environ['USERPROFILE'], 'AppData\\LocalLow\\Owlcat Games\\Pathfinder Kingmaker\\Saved Games')
	files = glob.glob(saves_path + '\\*.zks')
	
	waiting_for_input = True
	files_cnt = 1
	while(waiting_for_input):
		sorted_files = {}
		for file in files:
			mtime = os.path.getmtime(file)
			sorted_files[mtime] = file
		
		sorted_files = dict(sorted(sorted_files.items()))
		
		for k,v in sorted_files.items():
			print(f"{files_cnt} - {os.path.basename(v)}")
			files_cnt += 1
		
		print('Enter index to process: ')
		
		try:
			user_sel = input()
			print(f"user sel: '{user_sel}'")
			index = int(user_sel)
			foo = list(sorted_files)[index-1]
			print(foo)
			files = [sorted_files[foo]]
			waiting_for_input = False
		except Exception as ex:
			print(ex)
			if user_sel == 'q' or user_sel == 'x':
				files = []
				waiting_for_input = False
			else:	
				print('Bad input, try again')
else:
	#only open a single file, todo: cli args
	save_file = 'Quick_2.zks'
	files = [os.path.join(os.environ['USERPROFILE'], 'AppData/LocalLow/Owlcat Games/Pathfinder Kingmaker/Saved Games/', save_file)]

cnt = 0
for file in files:
	with zipfile.ZipFile(file, 'r') as zip_ref:
		zip_ref.extractall(os.path.join(os.getcwd(), str(cnt)))
	
	file_path = os.path.join(os.getcwd(), str(cnt), 'party.json')
	
	with open(file_path, 'r') as fh:
		data = json.load(fh)
	
	print()
	print(str(file))
	check(data)
	print()
	cnt+=1
