#!/usr/bin/python2.7
import qi
import sys
import time

class Robot(object):

	def __init__(self, settings = { 'IpRobot': "192.168.1.91",
                                    'port'   : 9559,
                                    'name'   : 'Aba',
                                    'MotivationTime':5,
                                    'BorgTime': 3,
                                    'useMemory': False
                                    },
                 ):

        #loading settings
		self.settings = settings

		self.launch_robot()


	def launch_robot(self):

		#load dialogs
		self.dialogs.load_dialogs()
		print('Creating session from Robot Model Source')
		self.session = qi.Session()
		self.connect_session()

		#launching robot services
		self.get_services()
		#self.getBehaviors()
		#launching face tracking service for the robot
		self.face_tracking()

	def connect_session(self):

		print self.settings['IpRobot']

		print "tcp://" + self.settings['IpRobot'] + ":" + str(self.settings['port'])

		self.robotIp = self.settings['IpRobot']
		self.port = str(self.settings['port'])

		try:
			self.session.connect("tcp://" + self.robotIp + ":" + str(self.port))

		except RuntimeError:

			print "Can't connect to Naoqi at ip"

	def get_services(self):

		#Get the service ALMemory
		self.memory = self.session.service("ALMemory")
		self.subscriber = self.memory.subscriber("WordRecognized")
		#Get the service TexttoSpeech
		self.tts = self.session.service("ALTextToSpeech")
		#Get the robot's preprogrammed dialogues durind Autonomus Life

		self.autonomus = self.session.service("ALAutonomousLife")
		#print('AL dialogs', self.AlDialog.getLoadedTopics("English"))
		self.blinking = self.session.service("ALAutonomousBlinking")

		#Get the service SpeechRecognition
		self.asr = self.session.service("ALSpeechRecognition")
		# Get the service Motion
		self.motion = self.session.service("ALMotion")
		# Get the service Tracking
		self.tracker = self.session.service("ALTracker")
		# Get the service Animated Speech
		self.animated = self.session.service("ALAnimatedSpeech")
		self.animatedconfig = {"bodyLanguageMode":"contextual"}
		# Get service Behaviors
		self.behaviors = self.session.service("ALBehaviorManager")

	def talking_questions(self):

		self.animated.say("Something wrong happpened with the calibration")