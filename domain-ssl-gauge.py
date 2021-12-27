from logging import error
import os
import prometheus_client
import subprocess
import time
from flask import Flask,Response
import yaml


def get_config(file):
    try:
        with open(file,'r') as f:
            config=yaml.safe_load(f)
            return(config)
    except error as e:
        print('config file {} do not exist'.format(file)) 
        exit

absdir=os.path.dirname(os.path.realpath(__file__))
config_file = absdir + os.sep + "config/config.yml"
print(config_file)
config=get_config(config_file)

flaskPort=config['flask']['port']
print(config['urls'])
print('port={}'.format(flaskPort))

def getdelta(host,port=443):
    expiry_time = "echo |openssl s_client -servername %s -connect %s:%d 2>/dev/null | openssl x509 -noout -dates|awk -F '=' '/notAfter/{print $2}'" %(host,host,port)
    expiry_ts = f'date +%s -d "$({expiry_time})"'
    now=int(time.time())
    sub_res = subprocess.run(expiry_ts, timeout=150, encoding='utf-8', stdout=subprocess.PIPE, shell=True).stdout
    # print(sub_res,type(sub_res))
    delta=int(sub_res)-now
    # print(delta,type(delta))
    return delta

deltaGauge=prometheus_client.Gauge('TimeDelta','time left',['domain'])
app=Flask(__name__)
@app.route('/metrics')
def res():
    for host in config['urls']:
        deltaGauge.labels(domain='{}'.format(host)).set(getdelta(host))
        # deltaGauge.labels(domain='{}'.format(host))
    return Response(prometheus_client.generate_latest(deltaGauge),
        mimetype='text/plain')

if __name__== '__main__':
    app.run(port=flaskPort,host='0.0.0.0')
