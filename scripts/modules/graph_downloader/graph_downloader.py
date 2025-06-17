
from alive_progress import alive_bar
import time
import requests
import os
import json
from dotenv import load_dotenv
from getpass4 import getpass


## Downloader class allows to fetch abromics reports from the api, filter them 
## and save them locally
class Downloader():

    def __init__(self, downloadDir = ".", email = "", password = ""):

        ## env variables (get the user ABRomics credentials from .env file)
        load_dotenv()
        
        ## load the environment variables
        self.api_url = "https://analysis.abromics.fr" # os.getenv('API_URL') 
        self.email = email
        self.password = password
        self.api_user_token = ""
        self.downloadDir = downloadDir

    ## Public methods

    ## Method used for manual authentification
    def authenticate(self):

        email = self.email
        password = self.password

        if self.email == "" or self.password == "":
            print("User authenfication")
            email = input("Enter your email: ")
            password = getpass("Password: ")

        response = requests.post(
            "https://analysis.abromics.fr/api/login/", 
            json={
                "email": email,
                "password": password
            }
        )
        try:
            response.raise_for_status()
            response = response.json()
            self.api_user_token = response['access']
        except requests.exceptions.HTTPError as e:
            print(e)
            exit()


    ## download all the abromics reports marked as "ready to report" 
    ## downloadDir (string) : indicate the directory in which the reports should be saved
    def getAllAbromicsReadyReports(self):
        response = { "next": "https://analysis.abromics.fr/api/analysis/" }
        exploitable_analysis_ids = []
        while "next" in response and response["next"] != None: 
            response = requests.get(
                response["next"],
                params={'status': 'ready_to_report'},
                headers = {
                    'Authorization': f"Bearer {self.api_user_token}", ## replace Basic with Bearer if it's a Bearer token
                }
            )
            response = response.json()
            for analysis in response["results"]:
                exploitable_analysis_ids.append(analysis["id"])

        print(f"{len(exploitable_analysis_ids)} reports will be downloaded ...")

        if not os.path.exists(self.downloadDir):
            os.makedirs(self.downloadDir)
    
        with alive_bar(len(exploitable_analysis_ids)) as bar:
            countDownloadFails = 0
            countDownloadSuccess = 0
            for report_id in exploitable_analysis_ids:
                print(report_id)
                response = requests.get(
                    f"https://analysis.abromics.fr/api/analysis/{report_id}/report/",
                    headers = {
                        'Authorization': f"Bearer {self.api_user_token}", ## replace Basic with Bearer if it's a Bearer token
                    }
                )
                try:
                    report = response.json()
                    # save the reports in a local file
                    with open(f'{self.downloadDir}/abr_report_{report_id}.json', 'w') as f:
                        json.dump(report, f)
                    countDownloadSuccess += 1
                except:
                    print("report not downloaded - Wrong format")
                    countDownloadFails += 1
                bar()
            print(f"Download finished ! \nnb success: {countDownloadSuccess}\nnb fails: {countDownloadFails}")
