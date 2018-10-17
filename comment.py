"""
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+
|  ~>>       // Triangulation //           <<~  |
+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+



"""

bar = "+==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==+"
top = "\"\"\"\n"+bar+"\n"
bottom = bar+"\n\n\n\"\"\""
left = "|  ~>>"
right = "<<~  |"

def buffer(s, l, right=True):
    if len(s) < l:
        if right:
            s = s + " "
        else:
            s = " " + s
        return buffer(s, l, not right)
    else:
        return s


def make_file_header(title):
    s = top
    s += left
    title_space = len(bar) - len(left) - len(right)
    s += buffer(title, title_space)
    s += right
    s += "\n" + bottom
    return s

print(make_file_header("Coxeter Graph"))