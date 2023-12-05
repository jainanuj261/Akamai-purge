import os
from dotenv import load_dotenv
import jenkins

env_path = ".env"

load_dotenv(env_path)

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])


# Jenkins server configuration
jenkins_url = "http://10.36.4.113:8080/"
jenkins_username = "admin"
jenkins_password = os.environ["JENKINS_API_TOKEN"]
server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)

# Define a slash command endpoint (/purge)
@app.command("/purge")
def purge_command(ack, body, say):
    job_name = "Akamai-Purge-Cache"
    ack()  # Acknowledge the command
    try:
        args = body["text"].split()
        environment = args[-1]  # Last argument is the environment
        urls = args[:-1]  # All other arguments are URLs
        
        
        parameters = {
            "DOMAIN": environment,
            "URL": "\n".join(urls)  # Concatenate all URLs separated by newline
        }
        server.build_job(job_name, parameters=parameters)
        say(f"Jenkins job triggered for {len(urls)} urls in {environment} environment.")
    except ValueError:
        say("Invalid command format. Please use `/purge <URL> <environment>`.")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()






