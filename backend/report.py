import json

def generate_report(sessions, progress_summary):
    report_data = {
        "Sessions": sessions,
        "ProgressSummary": progress_summary
    }
    with open("progress_report.json", "w") as report_file:
        json.dump(report_data, report_file, indent=4)
    print("Progress report saved to progress_report.json")