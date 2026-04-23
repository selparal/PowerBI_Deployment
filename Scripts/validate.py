import yaml
import os
import json
import sys

def load_config():
    with open("Config/deploy_config.yml") as f:
        return yaml.safe_load(f)

def validate_pages(report):
    name = report["name"]
    report_path = report["report_path"]
    required_pages = report.get("required_pages", [])
    errors = []

    print(f"\nValidating pages for: {name}")

    pages_path = os.path.join(report_path, "definition", "pages")

    if not os.path.isdir(pages_path):
        errors.append(f"Pages folder not found at: {pages_path}")
        return errors

    found_pages = []
    for page_folder in os.listdir(pages_path):
        page_json_path = os.path.join(pages_path, page_folder, "page.json")
        if os.path.isfile(page_json_path):
            with open(page_json_path) as f:
                page_data = json.load(f)
            display_name = page_data.get("displayName")
            if display_name:
                found_pages.append(display_name)

    print(f"  Pages found: {found_pages}")

    for page in required_pages:
        if page in found_pages:
            print(f"  + {page}")
        else:
            errors.append(f"Required page missing: '{page}'")

    return errors

def main():
    config = load_config()
    all_errors = []

    for report in config["reports"]:
        if not report.get("enabled", True):
            print(f"Skipping {report['name']} (disabled in config)")
            continue
        errors = validate_pages(report)
        all_errors.extend(errors)

    if all_errors:
        print("\nValidation failed:")
        for e in all_errors:
            print(f"  x {e}")
        sys.exit(1)
    else:
        print("\nAll validations passed.")

if __name__ == "__main__":
    main()
