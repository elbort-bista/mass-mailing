# -*- coding: utf-8 -*-`r`n# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-`r`nimport os
# -*- coding: utf-8 -*-`r`nimport webbrowser
# -*- coding: utf-8 -*-`r`nimport time
# -*- coding: utf-8 -*-`r`nimport subprocess
# -*- coding: utf-8 -*-`r`nimport sys
# -*- coding: utf-8 -*-`r`nfrom django.core.management import execute_from_command_line
# -*- coding: utf-8 -*-`r`n
# -*- coding: utf-8 -*-`r`nos.environ.setdefault('DJANGO_SETTINGS_MODULE','bluckmail.settings')
# -*- coding: utf-8 -*-`r`n
# -*- coding: utf-8 -*-`r`n# Start the Django server
# -*- coding: utf-8 -*-`r`nserver = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
# -*- coding: utf-8 -*-`r`n
# -*- coding: utf-8 -*-`r`n# Wait a bit for the server to start
# -*- coding: utf-8 -*-`r`ntime.sleep(2)
# -*- coding: utf-8 -*-`r`n
# -*- coding: utf-8 -*-`r`n# Open the browser
# -*- coding: utf-8 -*-`r`nwebbrowser.open('http://127.0.0.1:8000')
# -*- coding: utf-8 -*-`r`n
# -*- coding: utf-8 -*-`r`n# Keep the script running
# -*- coding: utf-8 -*-`r`nserver.wait()
