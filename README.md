# DevOps-Summer21-Customers-Squads/customers

### Members: 

Du, Li | ld2342@nyu.edu

Cai, Shuhong |  sc8540@nyu.edu

Zhang, Teng |  tz2179@nyu.edu | Ningbo | GMT+8 

Zhang, Ken | sz1851@nyu.edu | Shanghai, China | GMT+8 

Wang,Yu-Hsing | yw5629@nyu.edu | Taiwan | GMT+8 



### Code Conventions

Please follow the code convention described below (subject to change):

```python
## --------------------------------
## Class: Stopwords
## Author: Ken S. Zhang
## Usage: Read Stopword File
## --------------------------------
class Stopwords(object):
  	# read & preprocess the file
    # Params:
  	# file_dir: str | directory of file
    # Return:
    # None
    def __init__(self, file_dir):
        self.stopwords_list = list()
        try:
            print("Loading Stopwords File {}\n".format(file_dir))
            file_handle = open(file_dir, "r")
            lines = file_handle.readlines()
            file_handle.close()
        except Exception as e:
            print(e)
            print("Failed to Load Stopwords File {}".format(file_dir))
            exit()
        self.stopwords_list = [_.replace("\n","").strip().lower() for _ in lines]
		
    # give the list of stopwords
    # Params:
  	# None
    # Return:
    # self.stopwords_list: list | list of stopwords
    def dump_stopwords(self):
        return self.stopwords_list

```



