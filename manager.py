from app import create_app

app=create_app('default')

run_config={'develop':{'debug':True,'host':'0.0.0.0','port':8081}}
if __name__=="__main__":
    app.run(**run_config['develop'])