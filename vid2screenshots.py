import os
import time
import cv2
import imutils
import shutil
import img2pdf
import glob
import argparse


OUTPUT_SLIDES_DIR = f"./output"

FRAME_RATE = 3                   #   lower rate results in  faster processing
WARMUP = FRAME_RATE              # initial few frames to be skipped
FGBG_HISTORY = FRAME_RATE * 15   # no.of frames in background 
VAR_THRESHOLD = 16               # Threshold on the squared Mahalanobis distance between the pixel and the bkground model 
DETECT_SHADOWS = False            # If true, the algorithm will detect shadows and mark them.
MIN_PERCENT = 0.1                # min % of diff between foreground and background to detect if motion has stopped
MAX_PERCENT = 3                  # max % of diff between foreground and background to detect if frame is still in motion


def get_frames(video_path):
    '''A function to return the frames from a video located at video_path
    this function skips frames as defined in FRAME_RATE'''
    vs = cv2.VideoCapture(video_path)
    if not vs.isOpened():
        raise Exception(f'unable to open file {video_path}')
    total_frames = vs.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_time = 0
    frame_count = 0
    print("total_frames: ", total_frames)
    print("FRAME_RATE", FRAME_RATE)
    while True:
        # grab a frame from the video
        vs.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)    # move frame to a timestamp
        frame_time += 1/FRAME_RATE

        (_, frame) = vs.read()
        # if the frame is None, then we have reached the end of the video file
        if frame is None:
            break

        frame_count += 1
        yield frame_count, frame_time, frame

    vs.release()
 


def detect_unique_screenshots(video_path, output_folder_screenshot_path):
    ''''''
    # Initialize fgbg a Background object with Parameters
    fgbg = cv2.createBackgroundSubtractorMOG2(history=FGBG_HISTORY, varThreshold=VAR_THRESHOLD,detectShadows=DETECT_SHADOWS)
    captured = False
    start_time = time.time()
    (W, H) = (None, None)
    screenshoots_count = 0
    for frame_count, frame_time, frame in get_frames(video_path):
        orig = frame.copy() # clone the original frame (so we can save it later), 
        frame = imutils.resize(frame, width=600) # resize the frame
        mask = fgbg.apply(frame) # apply the background subtractor
        # if the width and height are empty, grab the spatial dimensions
        if W is None or H is None:
            (H, W) = mask.shape[:2]

        # compute the percentage of the mask that is "foreground"
        p_diff = (cv2.countNonZero(mask) / float(W * H)) * 100

        # if p_diff less than N% then motion has stopped, thus capture the frame

        if p_diff < MIN_PERCENT and not captured and frame_count > WARMUP:
            captured = True
            filename = f"{screenshoots_count:03}_{round(frame_time/60, 2)}.png"

            path = os.path.join(output_folder_screenshot_path, filename)
            print("saving {}".format(path))
            cv2.imwrite(path, orig)
            screenshoots_count += 1

        elif captured and p_diff >= MAX_PERCENT:
            captured = False
    print(f'{screenshoots_count} screenshots Captured!')
    print(f'Time taken {time.time()-start_time}s')
    return 


def initialize_output_folder(video_path):
    '''Clean the output folder if already exists'''
    output_folder_screenshot_path = f"{OUTPUT_SLIDES_DIR}/screenshots"
    if os.path.exists(output_folder_screenshot_path):
        shutil.rmtree(output_folder_screenshot_path)
    os.makedirs(output_folder_screenshot_path, exist_ok=True)
    print('initialized output folder', output_folder_screenshot_path)
    return output_folder_screenshot_path



if __name__ == "__main__":
    parser = argparse.ArgumentParser("video_path")
    parser.add_argument("video_path", help="path of video to be converted to pdf slides", type=str)
    args = parser.parse_args()
    video_path = args.video_path

    print('video_path', video_path)
    output_folder_screenshot_path = initialize_output_folder(video_path)
    detect_unique_screenshots(video_path, output_folder_screenshot_path)