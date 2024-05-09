
NOTE: Make sure you have Python installed in your computer
    download exe from (https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe)
    then install the python

1. download and install tesseract from : https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe

2. initially, run this command to install the packages:

    ``pip install -r requirements.txt``

3. go to config.txt(if no config.txt then create the file) and put the folder directories, for example:
   ```
   input_folder = E:\python\jati-python-ocr-demo\ov
   output_file = E:\python\jati-python-ocr-demo\output.csv
   ```
 
4. Then, go to this folder, and run this command -
   
   `` python main.py``
