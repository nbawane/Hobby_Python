# script to search a text in stack of files and directory
import os
import os.path
class Search_text:

    def search_fun(self,search_path,search_word):
        self.search_path = search_path
        self.search_word = search_word
        test_list = os.listdir(self.search_path)

        for file_name in test_list:
            if os.path.isfile(os.path.join(self.search_path,file_name)):
                fd = open(os.path.join(self.search_path,file_name),'r')
                for line in fd:
                    #print line
                    if self.search_word in line:
                        print line
                        print 'found in file',file_name


path = r'C:\San_py\test_folder2\M3ARelease_ShortDuration_WithSDR50'
search_word = 'azkaban'
obj = Search_text()
obj.search_fun(path,search_word)

