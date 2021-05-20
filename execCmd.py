import subprocess

# execute command, and return the output
# def execCmd(cmd):
#     r = os.popen(cmd)
#     text = r.read()
#     r.close()
#     return text

def execCmd(cmd):
    r = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    text = r.stdout.read().decode('utf-8')
    return text

if __name__ == '__main__':
    cmd = r"D:\FYJ\PyQt\QtLearning\venv\Scripts\python.exe D:\FYJ\PyQt\choice_data\test.py"
    # cmd = r"D:\Git_tasks\task_new\azamsServer\venv\Scripts\python.exe D:\Git_tasks\task_new\azamsServer\main_1.py"
    result = execCmd(cmd)
    print(result)