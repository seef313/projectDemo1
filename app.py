"""
A little bit of programming 
    Create an HTTP service that complies with the following requirements: 
    1. Written in any language you think is appropriate. (i.e. python,go, rust).  - We can use flask for this it simple and straight forward to use.
    2. Command-line flag for the listening port (defaults to 8080) and environment variable override. 
    3. Use mostly standard libraries. - Flask can make this easy as well 
    4. Please provide a Makefile (or use a similar tool) to define tasks 
    5. Three HTTP endpoints: 
        /helloworld                     -x 
            --> returns "Hello Stranger"                    -x 
        /helloworld?name=AlfredENeumann (any filtered value) <= wasnt sure if this qualifies as a serprate endpoint 
            --> returns "Hello Alfred E Neumann" (camel-case gets cut by spaces) 
        /versionz                                                                    
            --> returns a JSON with git hash and name of the project (needs to be compiled in) #json library with helpful function? 
    6. A structured log is written to standard out with:  # we can use python logging level to make this easy
            ISO date 
            HTTP status  #generated by flask? 
            Request 
    7. Write a readme file with usage examples. 
    8. Unit testing of all functionalities (flags, endpoints, etc.).  #how to do this? 
    9. A production-ready Dockerfile, so the service can run safely inside a 
       container. 
    10. Documentation where it makes sense.
    CI/CD 
    Using gitlab pipeline to control implementation and deplotment. ci.yaml file 
    
    IaC
    Not sure how to use helm properly (sorry)

    K8s Debugging 
    command: ["sleep"] ⇐ problem 


    GCP Architecture 
    Q: Imagine, a customer has some python applications which are already packaged via docker. They want a very easy way with a minimal operational effort to run this application in GCP. Suggest a GCP service that would be an option and tell us why. 
    A: Docker/Kubernetes/GKE 

"""
import subprocess, git, json, datetime, re
from flask import Flask, redirect, url_for, render_template, request


# Flask
# to run on different port  flask run --port=
app = Flask(__name__)
app.config["DEBUG"] = True


#function to get git hash 

def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

@app.route("/") #setting default landing to hello world 
@app.route("/helloworld", methods=["GET", "POST"])
def helloWorld():
    if request.args:
        args = request.args 
        return ("".join(" " + c if c.isupper() else c for c in args.get("name")).strip()) #to turn camel caase into space)

    print(aLog())
    return ("Hello Stranger") #this accomplishes task of /helloworld endpoint (5a) 


#?name=AlfredENeumann



@app.route("/versionz", methods=["GET", "POST"])
def versionz():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    name =  repo.remotes.origin.url.split('.git')[0].split('/')[-1]
    #5c 
    load = {
        "Project": name , 
        "Hash" : sha  
    }
    print(aLog())
    return(load)

# we can do a lot more with this functionality using python logging feeature. But, since no further context 
# was provided about the context based on which the logs should be generated I will just include a basic approach of 
# how to structure it 
# def aLog(): 
#     log = (
#         logging.info(datetime.now().isoformat())
#         logging.info()
#         logging.info()
#     )



def aLog(): 
    log =  json.dumps(
        
        {
            'ISOdate' : datetime.datetime.now().isoformat(),
            'HTTPstatus' : 200,
            'Request': request.method
        }
    
    )
    return(log)    

#unit testing
@app.cli.command("test")
def test(): 
    testApp = app.test_client() 
    with app.app_context():
        print("----------------------------------------------------------")
        print("Checking HelloWorld Endpoint")
        response = testApp.get("/helloworld")
        print("HelloWorld Endpoint: ", "Status: ", response.status)
        print("----------------------------------------------------------")
        print("Checking VersionZ Endpoint")
        response2 = testApp.get("/versionz")
        print("VersionZ Endpoint: ", "Status: ", response2.status)
        print("----------------------------------------------------------")
        print("Checking HelloWorld Filters")
        response3 = testApp.get("/helloworld?name=AlfredENeumann")
        print("Filters working? :",response3.data.decode('utf-8') == "Alfred E Neumann", "Status: ", response2.status)


if __name__ == "__main__":
    with app.app_context():
        app.run(port=3000)

