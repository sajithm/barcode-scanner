import cv2
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar
from datetime import datetime
import winsound
WINSOUND_FREQUENCY = 2500 #2500 Hz
WINSOUND_DURATION = 500 #0.5 s
FILE_RESULTS = "results.txt"

print("Starting webcam")
print("Press x to exit")

vs = VideoStream(src=0).start()
fileWriter = open(FILE_RESULTS, "w")
codesDetected = set()
while True:
	frameData = vs.read()
	frameData = imutils.resize(frameData, width=600)
	barcodes = pyzbar.decode(frameData)
	for barcode in barcodes:
		(x, y, width, height) = barcode.rect
		cv2.rectangle(frameData, (x, y), (x + width, y + height), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type	
		cv2.putText(frameData, barcodeData, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		if barcodeData not in codesDetected:
			textData = "{}\t{}\t{}".format(datetime.now().isoformat(), barcodeType, barcodeData)
			fileWriter.write(textData + "\n")
			fileWriter.flush()
			print(textData)
			codesDetected.add(barcodeData)
			winsound.Beep(WINSOUND_FREQUENCY, WINSOUND_DURATION)
	cv2.imshow("Barcode Scanner", frameData)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("x"):
		break
fileWriter.close()
cv2.destroyAllWindows()
print("Stopping webcam")
vs.stop()
print("Exiting")
