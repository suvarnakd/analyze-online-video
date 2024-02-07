import os
import img2pdf

import glob
import argparse


OUTPUT_SLIDES_DIR = f"./output"

FRAME_RATE = 3                   # no.of frames per second that needs to be processed, fewer the count faster the speed
WARMUP = FRAME_RATE              # initial number of frames to be skipped
FGBG_HISTORY = FRAME_RATE * 15   # no.of frames in background object
VAR_THRESHOLD = 16               # Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.
DETECT_SHADOWS = False            # If true, the algorithm will detect shadows and mark them.
MIN_PERCENT = 0.1                # min % of diff between foreground and background to detect if motion has stopped
MAX_PERCENT = 3                  # max % of diff between foreground and background to detect if frame is still in motion


def convert_screenshots_to_pdf(output_folder_screenshot_path):
    output_pdf_path = f"{OUTPUT_SLIDES_DIR}/presentation.pdf"
    print('output_folder_screenshot_path', output_folder_screenshot_path)
    print('output_pdf_path', output_pdf_path)
    print('converting images to pdf..')
    path = os.path.join(os.getcwd(), output_folder_screenshot_path)
    with open(output_pdf_path, "wb") as f:
        file_list = sorted(glob.glob(f"{path}/*.png"))
        print(file_list)
        f.write(img2pdf.convert(file_list))
    print('Pdf Created!')
    print('pdf saved at', output_pdf_path)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("screenshots_path")
    parser.add_argument("screenshots_path", help="path of screenshots to be converted to pdf", type=str)
    args = parser.parse_args()
    screenshots_path = args.screenshots_path
    if screenshots_path is not None:
        print('screenshots_path', screenshots_path)
    output_folder_screenshot_path = screenshots_path
    convert_screenshots_to_pdf(screenshots_path)