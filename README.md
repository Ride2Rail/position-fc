# Feature collector "position-fc"
***Version:*** 1.0

***Date:*** 24.05.2021

***Authors:***  [Zisis Maleas](https://github.com/zisismaleas); [Panagiotis Tzenos](https://github.com/ptzenos)

***Address:*** The Hellenic Institute of Transport (HIT), Centre for Research and Technology Hellas (CERTH)

# Description 

The "position-fc" feature collector is  a module of the **Ride2Rail Offer Categorizer** responsible for the computation of the determinant factors:  ***"road_dist"***, ***"ratio_dist"***, 
, ***"total_stops"***, ***"total_legs"***, ***"origin"***, ***"destination"***, ***"road_dist_norm"***, ***"total_stops_norm"***, ***"total_legs_norm"***, ***"ratio_dist_norm"***. 

***"road_dist"***, ***"road_dist_norm"*** : The total distance performed by transport modes using a road (car, bus, motorbike)  
***"ratio_dist"*** ,  ***"ratio_dist_norm"***: The proportion of distance using road network over the total trip distance. 
***"total_stops"***, ***"total_stops_norm"*** : The total number of stops this offer have. 
***"total_legs"***, ***"total_legs_norm"*** : The total number of legs this offer have. 


Computation can be executed from ***["position.py"](https://github.com/Ride2Rail/position-fc/blob/main/position.py)*** by running the procedure ***extract()*** which is binded under the name ***compute*** with URL using ***[FLASK](https://flask.palletsprojects.com)*** (see example request below). Computation is composed of three phases (***Phase I:***, ***Phase II:***, and  ***Phase III:***) in the same way the
 ***(https://github.com/Ride2Rail/tsp-fc)*** use it.

# Configuration

The following values of parameters can be defined in the configuration file ***"position.conf"***.

Section ***"running"***:
- ***"verbose"*** - if value __"1"__ is used, then feature collector is run in the verbose mode,
- ***"scores"*** - if  value __"minmax_score"__ is used, the minmax approach is used for normalization of weights, otherwise, the __"z-score"__ approach is used. 

Section ***"cache"***: 
- ***"host"*** - host address where the cache service that should be accessed by ***"position-fc"*** feature collector is available
- ***"port"*** - port number where the cache service that should be accessed used by ***"position-fc"*** feature collector is available

**Example of the configuration file** ***"position.conf"***:
```bash
[service]
name = position
type = feature collector
developed_by = Zisis Maleas <https://github.com/zisismaleas> and Panagiotis Tzenos <https://github.com/ptzenos>

[running]
verbose = 1
scores  = minmax_scores

[cache]
host = cache
port = 6379
```

# Usage
### Local development (debug on)

The feature collector "position-fc" can be launched from the terminal locally by running the script "position.py":

```bash
$ python3 position.py
 * Serving Flask app "position" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 
```

The repository contains also configuration files required to launch the feature collector in Docker from the terminal by the command docker-compose up:

```bash
docker-compose up
Starting position_fc ... done
Attaching to position_fc
position_fc    |  * Serving Flask app "position.py" (lazy loading)
position_fc    |  * Environment: development
position_fc    |  * Debug mode: on
position_fc    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
position_fc    |  * Restarting with stat
position_fc    |  * Debugger is active!
position_fc    |  * Debugger PIN: 
```

### Example Request
To make a request (i.e. to calculate values of determinant factors assigned to the "position-fc" feature collector for a given mobility request defined by a request_id) the command curl can be used:
```bash
$ curl --header 'Content-Type: application/json' \
       --request POST  \
       --data '{"request_id": "123x" }' \
         http://localhost:5007/compute
```
