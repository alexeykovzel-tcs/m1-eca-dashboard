To run the project on the localhost please write the following commands in the ./eca-dashboard-p2000:
```
./test.sh - for Linux
/test/bat - for Windows
python3 neca.py -s dashboard.py
```
The main work was conducted in the './dashboard_static/' directory and in the following directory files:
'cities-population.json', 'dashboard.py', 'dataconverter.py', 'datafixer.py', 'p2000-tweets.txt')

'template_static' was renamed to 'dashboard_static'
'template.py' was renamed to 'dashboard.py'

Before working with the flot and ECA, we decided to:

1. Combine 'lib' directories in the 'template_static' and 'dejvian_static'. Since we needed tweets.js from 'template_static' and 'barchart.js' from 'dejvian_static'.

2. Add a new method to 'barchart.js'. Namely 'setbarFull', which is the same as 'setbar' but inserts the full bar structure (all categories and their values). It was done for performance's sake, so we do not have to create the cycle in python and set [category, value] elements separately. The same was implemented for the piechart in 'charts.js'.

3. Change the core file 'generators.py':
   1. To increase the delta-time between tweet publications.
   2. To add emergency types and priority levels to JSON tweets through the python script 'dataconverter.py' 

4. Change the core file 'tweets.js' to include conditions for icons to be displayed.

The 'dashboard.py' is the core of our dashboard. It contains the init function named 'setup' which triggers the main tweets' cycle. The file operates functions related to the displayed content: the tweet list, the barchart and the piechart. The 'generate_tweet' function publishes the tweet and takes the data required to fill both barchart and piechart. Both functions are called during the execution of the 'generate_tweet' function.

All events, which are connected to functions, are bounded with HTML objects via id.

About the files:
1. 'datafixer.py' deletes test accounts, fixes image paths and deletes no name accounts(approximately 56 out of 17k) from 'p2000-tweets-orig.txt' and write the new data to 'p2000-tweets.txt' which is used further.

2. 'dataconverter.py' analyzes the given tweets from 'p2000-tweets.txt' and retrieves the emergency codes, priority codes, types of emergency calls and has a function, which returns top elements by values as a dictionary.

3. 'cities-population.json' contains all Dutch cities with their populations according to [this source](https://simplemaps.com/data/nl-cities).

4. 'dashboard_static/index.html' contains the web page structure.

5. 'dashboard_static/style' contains web page styles. CSS framework 'Bootstrap' was used.

6. 'dashboard_static/media' contains icons and images used in the dashboard.