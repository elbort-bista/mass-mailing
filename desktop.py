import subprocess
import webview
subprocess.Popen(['python','manage.py','runserver','127.0.0.1:8000'])
webview.create_window('MassMail App','http://127.0.0.1:8000')
webview.start()
