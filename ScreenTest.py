# USAGE
# python recognize_faces_video.py --encodings encodings.pickle
# python recognize_faces_video.py --encodings encodings.pickle --output output/jurassic_park_trailer_output.avi --display 0

# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import mysql.connector
import numpy as np
from mss import mss
from PIL import Image
from datetime import date

#today = date.today()
today = date(2020, 4, 8)
day = today.strftime("%a")

mydb = mysql.connector.connect(
  host="LAPTOP-76O3CEHF",
  user="root",
  passwd="",
  database="students_attendance"
)

mycursor = mydb.cursor()

sql = "Insert into test1(date, day) values (%s, %s)"
val = (today, day)

mycursor.execute(sql, val)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
	help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
	help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start()
writer = None
time.sleep(2.0)

faceOccurrence = {}
count = 0

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()
t=0
tic = time.perf_counter()
toc = time.perf_counter()

# loop over frames from the video file stream
while toc - tic < 10:
	count+=1
	faces=0
	#t+=1
        
	# grab the frame from the threaded video stream
	#frame_vs = vs.read()
	#print(frame_vs)
	sct_img = sct.grab(bounding_box)
	#print(sct_img)
	img = np.array(sct_img)
	frame = np.flip(img[:, :, :3], 2)
	#print(frame)
        
	# convert the input frame from BGR to RGB then resize it to have
	# a width of 750px (to speedup processing)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=750)
	r = frame.shape[1] / float(rgb.shape[1])
	#print(rgb)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input frame, then compute
	# the facial embeddings for each face
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
			if name in faceOccurrence.keys() :
				faceOccurrence[name]+=1
			else :
				faceOccurrence[name] = 0
		
		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# rescale the face coordinates
		top = int(top * r)
		right = int(right * r)
		bottom = int(bottom * r)
		left = int(left * r)

		# draw the predicted face name on the image
		if name == "Unknown":
			cv2.rectangle(img, (left, top), (right, bottom),
			(0, 0, 255), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 0, 255), 2)
		else:
			cv2.rectangle(img, (left, top), (right, bottom),
			(0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)
			print(name)
			faces+=1

	# if the video writer is None *AND* we are supposed to write
	# the output video to disk initialize the writer
	if writer is None and args["output"] is not None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 20,
			(frame.shape[1], frame.shape[0]), True)

	# if the writer is not None, write the frame with recognized
	# faces t odisk
	if writer is not None:
		writer.write(frame)

	# check to see if we are supposed to display the output frame to
	# the screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		import time
		if key== ord('s'):
			cv2.imwrite("./screenshots/{}.png".format(time.time()), frame)
		if count%10 == 0:
#			for name in faceOccurrence.keys():
#				print(name + ',')
#			print('\n')
			toc = time.perf_counter()
		print(faces)


print(count)
print(f"{toc-tic:0.4f}")
# do a bit of cleanup
cv2.destroyAllWindows()
#vs.stop()

# check to see if the video writer point needs to be released
if writer is not None:
	writer.release()


for name in faceOccurrence.keys():
        if name=="Unknown":
                continue
        else:
                if faceOccurrence[name] > count * 0.4 :
                        sql = "update test1 set {0}='P' where date=%s AND day=%s". format(name)
                        val=(today, day)
                        mycursor.execute(sql,val)

mydb.commit()

mycursor.execute("SELECT * from test1")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

