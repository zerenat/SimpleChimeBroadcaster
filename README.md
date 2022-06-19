# SimpleChimeBroadcaster
SimpleChimeBroadcaster is an easy to use, Python-based tool for transmitting messages to Amazon Chime chat rooms.

# How it works
The tool can be acquired as a pre-packaged Python executable (packaged with pyinstaller) or as source code.
Once set-up, ensure you have **simple_broadcaster_configuration.ini** and **webhooks.csv** files present at the project folder. The files are required dependencies and currently need to share location with the project itself.
* **simple_broadcaster_configuration.ini** - Holds resource information on the project.
* **webhooks.csv** - Should be used to configure target Chime rooms for the tool. First row of the document is reserved for column names, which are used by the tool to compile a target selection list. Any other rows can be used for targets. The tool is primitive and stops reading the file further after a cap is present between rows.

