from modules.graph_downloader.graph_downloader import Downloader

## Download all the abromics reports marked as ready to report
downloadDir = "data/public-reports"
choiceDownloadFreshReports = input(f"Download fresh reports data from abromics (this action is destructive) (target directory: {downloadDir}) ? [yes/no] ")
if choiceDownloadFreshReports == "yes": 
     downloader = Downloader(downloadDir = downloadDir)
     downloader.authenticate()
     print("Preparing the downloading process can be a bit long. Please wait..")
     downloader.getAllAbromicsReadyReports()

