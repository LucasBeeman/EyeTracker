import multiprocessing
import cv2
from gaze_tracking import GazeTracking
import vlc
import time

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


def track_eyes():
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break


def play_video():
    media_player = vlc.MediaPlayer()
    media = vlc.Media("C:\\Users\\Lucas Beeman\\Desktop\\Torture.mp4")
    media_player.set_media(media)
    while True:
        while gaze.is_blinking():
            print('blinking')
        media_player.play()
        if cv2.waitKey(1) == 27:
            break


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=track_eyes)
    p2 = multiprocessing.Process(target=play_video)

    p1.start()
    p2.start()
    p1.join()
    p2.join()


