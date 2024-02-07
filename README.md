# analyze-online-video
## Description
This repository has few  utility functions to-

1. Download online video 

2. Analyze the video and extract presentation slides as image files(PNG) in a folder. You may manually remove unwanted extracted slides or incorrectly extracted frames (if any). 

3. Create a collated PDF the image files

<br> 


## Setup
Create Python virtual environment  

```
pyenv install 3.10.0
pyenv virtualenv 3.10.0 py310
pyenv activate py310
pip install -r requirements.txt
```

## Script to downlaod youtube video
```
python download_vid.py <video url>
```
## Script to process video, to extract frames with slides and save in <screenshots_path>. You can give relative path.

```
python vid2screenshots.py  <screenshots_path>
```
## Script to process video, to create pdf from the slide screenshots extracted in step 2. 
```
python screenshots2pdf.py  <screenshots_path>
```
