from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_file
import webbrowser
import threading
from playwright.sync_api import sync_playwright
from main import run_scan
from playwright.sync_api import sync_playwright
from pathlib import Path
from flask import send_file
import os
from datetime import*
import json
import csv
from datetime import datetime
import time as tm


def atlas_banner():

    print(r"""

 ██████╗ ██████╗ ███████╗██╗██████╗ ██╗ █████╗ ███╗   ██╗
██╔═══██╗██╔══██╗██╔════╝██║██╔══██╗██║██╔══██╗████╗  ██║
██║   ██║██████╔╝███████╗██║██║  ██║██║███████║██╔██╗ ██║
██║   ██║██╔══██╗╚════██║██║██║  ██║██║██╔══██║██║╚██╗██║
╚██████╔╝██████╔╝███████║██║██████╔╝██║██║  ██║██║ ╚████║
 ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

               O B S I D I A N   A T L A S

      Passive Attack Surface Intelligence Framework

---------------------------------------------------------------
 Version : 1.0.0
 Mode    : Passive Reconnaissance
 Status  : Operational
---------------------------------------------------------------

""")
    
def boot(module, delay=0.08):

    print(f"[BOOT] {module:<45} [ OK ]")

    tm.sleep(delay)

print(">>> LAUNCHER VERSION 2026-06-28 <<<")
app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

latest_report=None
latest_report = None
latest_scan_data = None

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

@app.route("/")

def home():
    return render_template("atlas_launcher.html")

#----------------------------Scan Endpoint ----------------------------------

@app.route("/scan",methods=["POST"])
def scan():
    global latest_report,latest_scan_data
    domain=request.json.get("domain")
    
    if not domain:
        return jsonify({"success":False,"error":"No domain provided"})
    
    try:
        latest_report, latest_scan_data = run_scan(domain)
    
        return jsonify({"success":True})

    except Exception as e:
        return jsonify({"success":False,"error":str(e)})

#----------------------------------------------------------------------------



#-----------------------Report Endpoint -------------------------------------

@app.route("/report")
def report():
    global latest_report
    if not latest_report:
        return "No report generated.",404
    return send_file(latest_report)
#----------------------------------------------------------------------------


#------------------Download -----------------------------------------------

@app.route("/download")
def download():

    return render_template(
        "download_options.html"
    )

#-------------------------------------------------------------------------


#--------------------------------open Browser ------------------------------

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

#---------------------------------------------------------------------------



#------------------------------Export PDF------------------------------------

def get_downloads_folder():
    return str(Path.home() / "Downloads")

@app.route("/export/pdf")
def export_pdf():

    downloads = Path.home() / "Downloads"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = Path(latest_report).stem.replace(" ", "_")
    pdf_path = downloads / f"{target}_{timestamp}.pdf"
    
    
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            "http://127.0.0.1:5000/report",
            wait_until="networkidle"
        )

        page.evaluate("""
        () => {

            document.querySelectorAll('.accordion-item').forEach(item => {
                item.classList.add('active');
            });

        }
        """)

        page.wait_for_timeout(800)

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "10mm",
                "bottom": "10mm",
                "left": "10mm",
                "right": "10mm"
            }
        )

        print("PDF Exists:", pdf_path.exists())
        print("PDF Path:", pdf_path)
        browser.close()

    return send_file(
    pdf_path,
    as_attachment=True,
    download_name=pdf_path.name
)

#---------------------------------------------------------------------------




#------------------------------Export JSON ------------------------------------

@app.route("/export/json")
def export_json():

    global latest_scan_data

    if not latest_scan_data:
        return "No scan data available.", 404

    downloads = Path.home() / "Downloads"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    target = latest_scan_data["target"].replace(".", "_")

    json_filename = f"{target}_Report_{timestamp}.json"

    json_path = downloads / json_filename

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            latest_scan_data,
            f,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    return send_file(
        json_path,
        as_attachment=True,
        download_name=json_filename
    )


#-------------------------------------------------------------------------




#----------------------Export CSV ----------------------------------------

@app.route("/export/csv")
def export_csv():

    global latest_scan_data

    downloads = Path.home() / "Downloads"

    target = latest_scan_data["target"].replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path = downloads / f"{target}_{timestamp}.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # ================= TARGET =================

        writer.writerow(["TARGET"])
        writer.writerow(["Field", "Value"])
        writer.writerow(["Target", latest_scan_data["target"]])
        writer.writerow([])

        # ================= WHOIS =================

        writer.writerow(["WHOIS"])
        writer.writerow(["Field", "Value"])

        for key, value in latest_scan_data["whois"].items():
            writer.writerow([key, str(value)])

        writer.writerow([])

        # ================= DNS =================

        writer.writerow(["DNS RECORDS"])
        writer.writerow(["Record Type", "Value"])

        for record_type, values in latest_scan_data["dns"].items():

            if isinstance(values, list):
                for value in values:
                    writer.writerow([record_type, value])
            else:
                writer.writerow([record_type, values])

        writer.writerow([])

        # ================= SUBDOMAINS =================

        writer.writerow(["SUBDOMAINS"])
        writer.writerow(["Subdomain"])

        for subdomain in latest_scan_data["subdomains"]:
            writer.writerow([subdomain])

        writer.writerow([])

        # ================= PORTS =================

        writer.writerow(["OPEN PORTS"])
        writer.writerow(["Port"])

        for port in latest_scan_data["ports"]:
            writer.writerow([port])

        writer.writerow([])

        # ================= TECHNOLOGIES =================

        writer.writerow(["TECHNOLOGIES"])
        writer.writerow(["Technology"])

        for tech in latest_scan_data["technologies"]:
            writer.writerow([tech])

        writer.writerow([])

        # ================= HTTP =================

        http = latest_scan_data["http"]

        writer.writerow(["HTTP SUMMARY"])
        writer.writerow(["Field", "Value"])

        writer.writerow(["Status Code", http.get("status_code")])
        writer.writerow(["Server", http.get("server")])
        writer.writerow(["Response Time", http.get("response_time")])
        writer.writerow(["Content Type", http.get("content_type")])
        writer.writerow(["Redirect URL", http.get("redirect_url")])

        writer.writerow([])

        # ================= HEADERS =================

        writer.writerow(["HTTP HEADERS"])
        writer.writerow(["Header", "Value"])

        for key, value in http["headers"].items():
            writer.writerow([key, str(value)])

        writer.writerow([])

        # ================= COOKIES =================

        writer.writerow(["COOKIES"])
        writer.writerow(["Cookie", "Value"])

        for key, value in http["cookies"].items():
            writer.writerow([key, value])

    return send_file(
        csv_path,
        as_attachment=True,
        download_name=csv_path.name
    )

#--------------------------------------------------------------------------




#---------------------- RUN ------------------------------------------------

if __name__=="__main__":
    atlas_banner()

    modules = [

    "Initializing Runtime Environment",
    "Checking Python Environment",
    "Loading Atlas Core",
    "Loading Passive Intelligence Engine",
    "WHOIS Enumeration Engine",
    "DNS Enumeration Engine",
    "Subdomain Discovery Engine",
    "Port Scanning Engine",
    "HTTP Fingerprinting Engine",
    "Technology Detection Engine",
    "Threat Assessment Engine",
    "Report Generation Engine",
    "Export Engine (PDF / JSON / CSV)",
    "Data Visualization Engine",
    "Starting Flask Web Interface"

]

    for module in modules:
        boot(module)

    print()
    print("-" * 64)
    print("[*] Atlas Core Initialized Successfully")
    print("[*] Web Server Online : http://127.0.0.1:5000")
    print("[*] Opening Tactical Dashboard...")
    print("-" * 64)
    print()
    threading.Timer(
        1,
        open_browser
    ).start()

    app.run(
        debug=False,
        use_reloader=False
    )