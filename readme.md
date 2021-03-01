# Install
(install requirements)

```
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

# Create Schedule
The input files provided is found in `data/case1` directory. 

* Run the following command to ger the schedule.

```
 python ./main.py
```
* You will be asked if you want to use your own directory.

```Do you want to use the default directory (./data/case1/) with input files [y/n]:```

* Say yes if you want to use the default directory `data/case1/`. This is were the original input files provided is found.

* Say no if you want to provide your own directory. But please make sure that the files inside
of this directory has the correct naming (forced_day_off.csv, qualified_route.csv, pref_day_off.csv)
```Please provide directory that contains input files
Don't forget to add the / at the end of the directory:
Your directory: 
```

# Run Tests
To run unit test please run the following command.
```
 pytest
```