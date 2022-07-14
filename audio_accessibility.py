import pyaudio, os, wave
import speech_recognition as sr

class haudio:
	def record_Audio(self): # https://realpython.com/playing-and-recording-sound-python/#recording-audio
		self.chunk, self.sample_format, self.channels, self.fs, self.seconds, self.filename = \
		1024,       pyaudio.paInt16,    2,             44100,   5,            "./recordings/voice_Input_1.wav"
		if os.path.exists(self.filename):
			os.remove(self.filename)
		self.p = pyaudio.PyAudio()
		print("Recording starting...")
		self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs, frames_per_buffer=self.chunk, input=True)
		self.frames = []
		for self.i in range(0, int(self.fs / self.chunk * self.seconds)):
			self.data = self.stream.read(self.chunk)
			self.frames.append(self.data)
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
		print('Recording ended')
		self.wf = wave.open(self.filename, 'wb')
		self.wf.setnchannels(self.channels)
		self.wf.setsampwidth(self.p.get_sample_size(self.sample_format))
		self.wf.setframerate(self.fs)
		self.wf.writeframes(b''.join(self.frames))
		self.wf.close()
		return True if os.path.exists(self.filename) else False

	def speech2Words(self): # https://www.analyticsvidhya.com/blog/2022/01/speech-to-text-conversion-in-python-a-step-by-step-tutorial/
		self.r = sr.Recognizer()
		with sr.AudioFile('./recordings/voice_Input_1.wav') as self.source:
			self.audio_text = self.r.listen(self.source)
		try:
			self.text = self.r.recognize_google(self.audio_text)
			print("Recorded audio : ", self.text)
			return True, self.text
		except:
			print('Sorry.. run again...')
			return False, " "

	def matchIt(self, words, options):
		self.words = list(words.split(" "))
		self.options = options
		print("Transcription from audio : ", self.words)
		self.recognizedWord = ''
		if len(self.words) == 1 :
			if self.words[0] in self.options:
				self.recognizedWord = self.words[0]
			else :
				print("unrecognisable")
				return False, ""
		elif len(self.words) > 1 :
			for self.wor in self.words:
				if self.wor in self.options:
					self.recognizedWord = self.wor
					break
		print("Recognized word : _", self.recognizedWord, "_")
		return True, self.recognizedWord