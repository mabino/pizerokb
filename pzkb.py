#!/usr/bin/env python3
import os, time

NULL_CHAR = chr(0)
current_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_dir,'password.txt')

def write_report(report):
	try:
		with open('/dev/hidg0', 'rb+') as fd:
			fd.write(report.encode())
	except: pass

def transcribe(key):
	lower_case = {'a':4,'b':5,'c':6,'d':7,'e':8,'f':9,'g':10,'h':11,'i':12,'j':13,'k':14,'l':15,'m':16,'n':17,'o':18,'p':19,'q':20,'r':21,'s':22,'t':23,'u':24,'v':25,'w':26,'x':27,'y':28,'z':29,'-':45,'=':46,'[':47,']':48,'\\':49,';':51,"'":52,',':54,'.':55,'/':56,'1':30,'2':31,'3':32,'4':33,'5':34,'6':35,'7':36,'8':37,'9':38,'0':39,'`':53,r'\n':40,'\t':43,' ':44}
	upper_case = {'A':4,'B':5,'C':6,'D':7,'E':8,'F':9,'G':10,'H':11,'I':12,'J':13,'K':14,'L':15,'M':16,'N':17,'O':18,'P':19,'Q':20,'R':21,'S':22,'T':23,'U':24,'V':25,'W':26,'X':27,'Y':28,'Z':29,'_':45,'+':46,'{':47,'}':48,'|':49,':':51,'"':52,'<':54,'>':55,'?':56,'!':30,'@':31,'#':32,'$':33,'%':34,'^':35,'&':36,'*':37,'(':38,')':39,'~':53}

	if key in lower_case:
		write_report(NULL_CHAR*2+chr(lower_case[key])+NULL_CHAR*5)
	elif key in upper_case:
		write_report(chr(32)+NULL_CHAR+chr(upper_case[key])+NULL_CHAR*5)
write_report(NULL_CHAR*5)

def translate(doc):
	for index in range(len(doc)):
	# repr adds single quotes
		hit_key = repr(doc[index])
		
		if eval(hit_key) == "'" or eval(hit_key) == '\\':
			print(eval(hit_key))
			transcribe(eval(hit_key))
		else:
			print(hit_key.strip("'"))
			transcribe(hit_key.strip("'"))

def interpret(path):
	action_key = {'\ENTER':40,'\ESCAPE':41,'\DELETE':42,'\TAB':43,'\SPACE':44,'\PRINT':70,'\SCROLL':71,'\PAUSE':72,'\INSERT':73,'\HOME':74,'\PAGEUP':75,'\END':77,'\PAGEDOWN':78,'\RIGHTARROW':79,'\LEFTARROW':80,'\DOWNARROW':81,r'\UPARROW':82,'\POWER':102,'\LEFTCTRL':224,'\LEFTSHIFT':225,'\LEFTALT':226,'\LEFTGUI':227,'\RIGHTCTRL':228,'\RIGHTSHIFT':229,'\RIGHTALT':230,'\RIGHTGUI':231}
	function_key = {'\F1':58,'\F2':59,'\F3':60,'\F4':61,'\F5':62,'\F6':63,'\F7':64,'\F8':65,'\F9':66,'\F10':67,'\F11':68,'\F12':69,'\F13':104,'\F14':105,'\F15':106,'\F16':107,'\F17':108,'\F18':109,'\F19':110,'\F20':111,'\F21':112,'\F22':113,'\F23':114,'\F24':115}
	menu_key = {'\EXECUTE':116,'\HELP':117,'\MENU':118,'\SELECT':119,'\STOP':120,'\AGAIN':121,r'\UNDO':122,'\CUT':123,'\COPY':124,'\PASTE':125,'\FIND':126,'\MUTE':127,'\VOLUP':128,'\VOLDOWN':129,'\CAPLOCK':130,r'\NUMLOCK':131,'\SCROLLLOCk':132}
	#mod_key​ = {'\LEFTCTRL':1,'\LEFTSHIFT':2,'\LEFTALT':4,'\LEFTWIN':8,'\RIGHTCTRL':16,'\RIGHTSHIFT':32,'\RIGHTALT':64,'\RIGHTWIN':128}

	merged_key = {}
	merged_key.update(action_key)
	merged_key.update(function_key)
	merged_key.update(menu_key)
	
	with open(path,'r') as script:
		script_contents = script.read()
	
	# Makes a list of lines in the document.
	for count1, line in enumerate(script_contents.split('\n')):
		# Makes a list of the words on the current line.
		for count2, word in enumerate(line.split(' ')):
			if word in merged_key:
				write_report(NULL_CHAR*2+chr(merged_key[word])+NULL_CHAR*5)
			elif word[:6] == '\SLEEP':
				time.sleep(int(word[6:]))
			elif word not in merged_key and count2 < 1:
			# Don't put a space back for the first word.
				translate(word)
			else:
			# Put the space back.
				translate(' ')
				translate(word)
		if count1 < len(script_contents.split('\n')) - 1:
			# Put the new line characters back as long as it isn't the last word.
			translate('\n')
	# Insurance policy to make sure all the keys are released at the end.
	write_report(NULL_CHAR*8)

if __name__ == '__main__':
	interpret(path)
