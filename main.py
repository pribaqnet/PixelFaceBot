# Projecte desenvolupat per Pau Riba - https://pribaq.net

# IMPORTS
from pyimagesearch.face_blurring import anonymize_face_pixelate
from pyimagesearch.face_blurring import anonymize_face_simple
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os, sys, logging, time, random, cv2
import numpy as np

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

#VARIABLES
token = "BOT-TOKEN"
nombot = "usuaridelbot" # Sense l'@
alertes = "USUARI/GRUP/CANAL" # Allà s'enviaran les alertes (Inici del bot)

def censura(imgpath):

	# VARIABLES
	face = "face_detector" # Métode de detecció facial
	method = "pixelated" # Tipus de censura: "simple" o "pixelated"
	blocks = 20 # Número de blocs en el mode pixelated
	preconfidence = "0.5" # Confidencialitat (Entre 0 i 1)

	# SCRIPT DE RECONEIXEMENT FACIAL
	prototxtPath = os.path.sep.join([face, "deploy.prototxt"])
	weightsPath = os.path.sep.join([face,"res10_300x300_ssd_iter_140000.caffemodel"])
	net = cv2.dnn.readNet(prototxtPath, weightsPath)
	image = cv2.imread(imgpath)
	orig = image.copy()
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),(104.0, 177.0, 123.0))
	net.setInput(blob)
	detections = net.forward()

	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > float(preconfidence):
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# EXTREU LA CARA (ROI)
			face = image[startY:endY, startX:endX]

			# APICA LA CENSURA FACIAL
			if method == "simple":
				face = anonymize_face_simple(face, factor=3.0)
			else:
				face = anonymize_face_pixelate(face,
					blocks=blocks)

			# ENGANXA LA CARA CENSURADA A LA IMATGE
			image[startY:endY, startX:endX] = face

	# GUARDAR
	cv2.imwrite(imgpath, image)

	# LOG
	print("Nova imatge censurada!")

def novafoto(update, context):
	nomfoto = str(update.message.chat_id) + '.png'
	path = "fotos/"
	photo_file = update.message.photo[-1].get_file()
	photo_file.download(path + nomfoto)
	imgpath = path + nomfoto
	censura(imgpath)
	context.bot.send_photo(chat_id=update.message.chat_id, photo=open(imgpath, 'rb'))
	os.remove(imgpath)

def start(update, context):
	context.bot.send_message(chat_id=update.message.chat_id, text="""*[CA]* 👉🏼 Utilitza aquest bot per amagar cares de persones a imatges. Envia una foto i el bot te la retornarà amb totes les cares censurades. ❤️

*[EN]* 👉🏼 Use this bot to hide people's faces in pictures. Send a photo and the bot will send it back to you with all the censored faces. ❤️""", parse_mode='MARKDOWN')
	context.bot.send_message(chat_id=update.message.chat_id, text="""🧑🏻‍💻 En desenvolupament / In development ➡️ https://ja.cat/UVU7r""", parse_mode='MARKDOWN')

def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
	updater = Updater(token, use_context=True)
	dp = updater.dispatcher

	#FOTOS
	dp.add_handler(MessageHandler(Filters.photo, novafoto))

	#COMANDAMENTS
	dp.add_handler(CommandHandler("start", start))

	#INICI DEL BOT
	updater.bot.send_message(chat_id=alertes, text="*🙂 @" + nombot + ":* El bot s'ha iniciat correctament!", parse_mode='MARKDOWN')
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
