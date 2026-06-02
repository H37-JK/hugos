import os
import shutil
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}

sites = [
    {"site_name": "ohang-home", "region_file": "daehwa.md", "title": "서울 전지역 누수탐지"},
    {"site_name": "ohang-homs", "region_file": "juyeop.md", "title": "서울 전지역 누수탐지"},
]


def deploy_matched_sites():
    for item in sites:
        site_name = item['site_name']
        region_file = item['region_file']
        page_title = item['title']

        print(f"--- {site_name} (지역: {region_file}) 작업 시작 ---")

        if os.path.exists("content"):
            shutil.rmtree("content")
        os.makedirs("content")

        source_file = f"regions_data/{region_file}"
        shutil.copy(source_file, "content/_index.md")

        res = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json={"name": site_name})

        if res.status_code == 201:
            site_id = res.json()['id']
        else:
            res_list = requests.get("https://api.netlify.com/api/v1/sites", headers=headers)
            site_id = next(s['id'] for s in res_list.json() if s['name'] == site_name)

        print(f"Building site for {page_title}...")

        current_env = os.environ.copy()
        current_env["HUGO_TITLE"] = page_title

        result = subprocess.run(
            ["hugo", "--cleanDestinationDir"],
            env=current_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode != 0:
            print("❌ Hugo 빌드 에러:")
            print(result.stderr)
            continue

        print(site_id)

        subprocess.run(["netlify", "deploy", "--prod", "--dir", "public", "--site", site_id], check=True, shell=True)
        print(f"✅ {site_name} 배포 완료!\n")


if __name__ == "__main__":
    deploy_matched_sites()
