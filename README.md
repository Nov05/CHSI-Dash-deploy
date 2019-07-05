# CHSI-Dash-deploy

<br>

## :point_right: Deployment of Dash App for CHSI Dataset  

**Dash App on Heroku**  
http://dash-app-chsi.herokuapp.com/  
**Data Source and IPython Notebooks**  
https://github.com/Nov05/CHSI-Dash/blob/master/README.md

<img src="https://github.com/Nov05/CHSI-Dash/blob/master/pictures/ezgif.com-optimize.gif?raw=true" width=300>  

<br>

## :point_right: Logs

2019-07-03 Repo created
  
2019-07-04 Debug  
`heroku logs -n 200 -a dash-app-chsi`  
https://devcenter.heroku.com/articles/logging#view-logs    

Add `server = app.server` after `app = dash.Dash(__name__)`, or it would have the follow problem.  
```
2019-07-04T19:59:32.625915+00:00 app[api]: Deploy ff987c7a by user ***@***.com
2019-07-04T19:59:32.625915+00:00 app[api]: Release v12 created by user ***@***.com
2019-07-04T19:59:42.002629+00:00 heroku[web.1]: Starting process with command gunicorn app:server
2019-07-04T19:59:44.144995+00:00 heroku[web.1]: State changed from starting to up
2019-07-04T19:59:43.834964+00:00 app[web.1]: [2019-07-04 19:59:43 +0000] [4] [INFO] Starting gunicorn 19.9.0
2019-07-04T19:59:43.835634+00:00 app[web.1]: [2019-07-04 19:59:43 +0000] [4] [INFO] Listening at: http://0.0.0.0:46428 (4)
2019-07-04T19:59:43.835736+00:00 app[web.1]: [2019-07-04 19:59:43 +0000] [4] [INFO] Using worker: sync
2019-07-04T19:59:43.839311+00:00 app[web.1]: [2019-07-04 19:59:43 +0000] [10] [INFO] Booting worker with pid: 10
2019-07-04T19:59:43.888263+00:00 app[web.1]: [2019-07-04 19:59:43 +0000] [18] [INFO] Booting worker with pid: 18
2019-07-04T19:59:48.617367+00:00 app[web.1]: Failed to find application object 'server' in 'app'
2019-07-04T19:59:48.617526+00:00 app[web.1]: [2019-07-04 19:59:48 +0000] [10] [INFO] Worker exiting (pid: 10)
2019-07-04T19:59:48.646167+00:00 app[web.1]: Failed to find application object 'server' in 'app'
2019-07-04T19:59:48.646378+00:00 app[web.1]: [2019-07-04 19:59:48 +0000] [18] [INFO] Worker exiting (pid: 18)
2019-07-04T19:59:48.906311+00:00 app[web.1]: [2019-07-04 19:59:48 +0000] [4] [INFO] Shutting down: Master
2019-07-04T19:59:48.906408+00:00 app[web.1]: [2019-07-04 19:59:48 +0000] [4] [INFO] Reason: App failed to load.
2019-07-04T19:59:49.011878+00:00 heroku[web.1]: State changed from up to crashed
2019-07-04T19:59:48.990353+00:00 heroku[web.1]: Process exited with status 4
2019-07-04T19:59:55.000000+00:00 app[api]: Build succeeded
2019-07-04T20:02:43.769103+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/" host=dash-app-chsi.herokuapp.com request_id=871a9cfd-c666-4416-af42-dc4cbdf4665f fwd="*.*.*.*" dyno= connect= service= status=503 bytes= protocol=http
2019-07-04T20:02:44.323653+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/favicon.ico" host=dash-app-chsi.herokuapp.com request_id=f9db9ffc-ef64-474e-9bd2-976c6a938b30 fwd="*.*.*.*" dyno= connect= service= status=503 bytes= protocol=http
```

2019-07-04 Debug 3D Surface
```
# this is a plane
trace2 = go.Surface(
    x=tuple(p1),
    y=tuple(p2),
    z=tuple(p3),
    name='slice',
    colorscale="Greys",
    opacity=0.5,
### WARNING: This is invalid. It would not cause problem in Colab.
###          But it would fail the plot when deployed on Heroku.
#     showlegend=False,  # invalid property
    showscale=False,
)
```
