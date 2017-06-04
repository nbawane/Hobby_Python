import re

string = r'/url?q=http://dl2.mihanpix.com/Serial/Friends/&sa=U&ved=0ahUKEwjc7c6R_qPUAhWFNY8KHb9nCusQFggZMAE&usg=AFQjCNGQ8RtbPF6VD322FNhK6Ev8q3AUEg'
urls = re.search("(?P<url>https?://[^\s]+)", string).group("url")
print urls