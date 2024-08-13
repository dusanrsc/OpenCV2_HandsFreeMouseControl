# importing module
import cv2
import pyautogui

# importing sub-module
from cvzone.HandTrackingModule import HandDetector

# metadata
__version__ = "v1.1.0-beta"
__updated__ = "13.08.2024"
__by__ = "Dusan Rosic"
__tag__ = "@dusanrsc"

# safety method for pyautogui
pyautogui.FAILSAFE = False

# capturing video source
cap = cv2.VideoCapture(0)

# hand detector
detector = HandDetector(maxHands=1, detectionCon=0.85)

# CONSTANTS
MOUSE_SPEED = 12
WINDOW_TITLE = "Hands-Free Mouse Control"

# main loop while camera is capturing
while cap.isOpened():

	# frame reading
	success, frame = cap.read()

	# frame flipping for mirror effect
	frame = cv2.flip(frame, 1)

	# if frame is not valid break
	if not success:
		break

	# detecting hands
	hands, frame = detector.findHands(frame, draw=False) 

	# if hands are detected
	if hands:

		# hand landmarks
		hand = hands[0]

		# detect fingers
		fingerup = detector.fingersUp(hand)

		# move mouse left 
		if fingerup == [1, 0, 0, 0, 0]:
			pyautogui.moveRel(-MOUSE_SPEED, 0, 0.1)

		# move mouse up
		elif fingerup == [0, 1, 0, 0, 0]:
			pyautogui.moveRel(0, -MOUSE_SPEED, 0.1)

		# move mouse right
		elif fingerup == [1, 1, 0, 0, 0]:
			pyautogui.moveRel(+MOUSE_SPEED, 0, 0.1)

		# move mouse down
		elif fingerup == [0, 1, 1, 0, 0]:
			pyautogui.moveRel(0, +MOUSE_SPEED, 0.1)

		# single left mouse click
		elif fingerup == [1, 1, 1, 1, 1]:
			pyautogui.click()

		# right mouse click
		elif fingerup == [0, 0, 0, 0, 1]:
			pyautogui.rightClick()

		# if middle finger is up exit the program
		elif fingerup == [0, 0, 1, 0, 0]:
			print("Forbidden! How Dare Are You..?")
			break

		### NOTE: MOVE MOUSE WHILE CLICKED
		# move mouse up
		elif fingerup == [1, 0, 1, 1, 1]:
			pyautogui.moveRel(0, -MOUSE_SPEED, 0.1)
			pyautogui.mouseDown(button="left")
		
		# move mouse down
		elif fingerup == [1, 0, 0, 1, 1]:
			pyautogui.moveRel(0, +MOUSE_SPEED, 0.1)
			pyautogui.mouseDown(button="left")
		
		# move mouse right
		elif fingerup == [0, 0, 1, 1, 1]:
			pyautogui.moveRel(+MOUSE_SPEED, 0, 0.1)
			pyautogui.mouseDown(button="left")
		
		# move mouse left
		elif fingerup == [0, 1, 1, 1, 1]:
			pyautogui.moveRel(-MOUSE_SPEED, 0, 0.1)
			pyautogui.mouseDown(button="left")

		# neutral
		else:
			pyautogui.mouseUp(button="left")

	# no input
	else:
		pass

	# displaying video frame
	cv2.imshow(f"{WINDOW_TITLE} | {__version__} | by: {__by__} ({__tag__})", frame)

	# if event key "Escape" is pressed exit the program
	if cv2.waitKey(1) & 0xFF == 27:
		break

# liberating main camera source
cap.release()

# destroying all windows
cv2.destroyAllWindows()
