# SimpleChimeBroadcaster
SimpleChimeBroadcaster is an easy to use, Python-based tool for transmitting messages to Amazon Chime chat rooms.

# Set-up
The tool can be acquired as a pre-packaged Python executable (packaged with pyinstaller) or as source code.
Once set-up, ensure you have **simple_broadcaster_configuration.ini** and **webhooks.csv** files present at the project folder. The files are required dependencies and currently need to share location with the project itself.
* **simple_broadcaster_configuration.ini** - Holds resource URL links for the broadcaster.
* **webhooks.csv** - Should be used to configure target Chime rooms for the tool. First row of the document is reserved for column names, which are used by the tool to compile a target selection list. Any other rows can be used for targets. The tool is primitive and stops reading the file further after a cap is present between rows. Start filling in the file from the first row.

# How to works
Start the tool and a window will appear. On that window you'll find a text area, drop down menu and a button. Type/ paste your message into the text area and choose the target audience from the drop down menu. Once happy with the selection, hit the "Submit" button to broadcast the message.
