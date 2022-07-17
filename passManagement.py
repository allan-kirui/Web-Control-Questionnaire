import yaml

# Use your own yaml file, file looks like https://stackoverflow.com/questions/34230673/hide-login-credentials-in-python-script

conf = yaml.safe_load(open('D:\Education\PersonalProjects\Web Control Questionnaire\pass.yml'))

username = conf['user']['username']
pwd = conf['user']['password']
