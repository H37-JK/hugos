import os
import shutil
import subprocess
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}

sites = [
    {"name": "homecarees-ssulbis"},
    # {"name": "recarees-semuns"},
    # {"name": "fullcarees-sujuns"},
]
area_data = {
    "서울특별시": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "경기도": ["가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"],
    "인천광역시": ["강화군", "계양구", "미추홀구", "남동구", "동구", "부평구", "서구", "연수구", "옹진군", "중구"],
}


import random

def generate_random_body(region, category):
    # 1. 인사말 및 도입부 (여러 버전)
    intros = [
        f"안녕하세요! {region} 지역에서 {category} 문제를 가장 신속하게 해결해 드리는 베테랑 팀입니다.",
        f"{region} 주민 여러분, 갑작스러운 {category} 때문에 당황하셨나요? 저희가 즉시 달려갑니다.",
        f"믿을 수 있는 {region} 전담 {category} 수리 업체입니다. 365일 24시간 대기 중입니다."
    ]

    # 2. 서비스 특징 (여러 버전)
    features = [
        f"저희는 최신형 고화질 배관 내시경을 투입하여 {region} 현장의 원인을 정확히 파악합니다.",
        f"단순히 뚫는 것에 그치지 않고, 강력한 고압 세척 장비로 배관 내부 스케일링까지 완벽하게 진행합니다.",
        f"특수 석션 장비를 활용해 이물질을 근본적으로 제거하여 재발 가능성을 최소화하고 있습니다."
    ]

    # 3. 지역 관련 멘트 (랜드마크 등과 결합하면 베스트)
    local_mentions = [
        f"{region} 인근 아파트 단지는 물론 상가, 빌라 어디든 15분 내외로 도착이 가능합니다.",
        f"이미 {region} 내 많은 고객님들께서 저희의 꼼꼼한 시공 서비스에 만족하고 계십니다.",
        f"지역 특성을 잘 아는 {region} 전담 기사가 배정되어 거품 없는 투명한 견적을 약속드립니다."
    ]

    # 4. 마무리 및 호출
    closings = [
        f"지금 바로 전화주시면 {region} 전문 상담원이 친절하게 안내해 드리겠습니다.",
        f"어려운 배관 문제, 더 이상 혼자 고민하지 마시고 전문가에게 맡겨주세요.",
        f"합리적인 비용과 확실한 A/S로 {region} 고객님의 만족을 책임지겠습니다."
    ]

    # 각 리스트에서 하나씩 무작위 선택
    body = [
        random.choice(intros),
        random.choice(features),
        random.choice(local_mentions),
        random.choice(closings)
    ]

    # [중요] 섹션의 순서까지 섞어주면 중복 판정 확률이 더 낮아집니다.
    # random.shuffle(body)

    return "\n\n".join(body)


def generate_random_title(region, category):
    prefixes = ["", "", ""]
    suffixes = ["전문 업체", "가장 잘하는 곳", "10곳 비교", "업체 리스트"]

    pre = random.choice(prefixes)
    suf = random.choice(suffixes)

    return f"{pre} {region} {category} {suf}".strip()

now = datetime.now()
today_str = now.strftime("%Y-%m-%dT%H:%M:%S+09:00") # 한국 시간대(+09:00) 포함

# "부산광역시": ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
# "대구광역시": ["중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"],
# "광주광역시": ["동구", "서구", "남구", "북구", "광산구"],
# "대전광역시": ["동구", "중구", "서구", "유성구", "대덕구"],
# "울산광역시": ["중구", "남구", "동구", "북구", "울주군"],
# "강원도": ["원주시", "춘천시", "강릉시", "동해시", "속초시", "삼척시", "홍천군", "태백시", "철원군", "횡성군", "평창군", "영월군", "정선군", "인제군", "고성군", "양양군", "화천군", "양구군"],
# "충청북도": ["청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"],
# "충청남도": ["천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"],
# "경상북도": ["포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "군위군", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"],
# "경상남도": ["창원시", "김해시", "진주시", "양산시", "거제시", "통영시", "사천시", "밀양시", "함안군", "거창군", "창녕군", "고성군", "하동군", "합천군", "남해군", "함양군", "산청군", "의령군"],
# "전라북도": ["전주시", "익산시", "군산시", "정읍시", "완주군", "김제시", "남원시", "고창군", "부안군", "임실군", "순창군", "진안군", "장수군", "무주군"],
# "전라남도": ["여수시", "순천시", "목포시", "광양시", "나주시", "무안군", "해남군", "고흥군", "화순군", "영암군", "영광군", "완도군", "담양군", "장성군", "보성군", "신안군", "장흥군", "강진군", "함평군", "진도군", "곡성군", "구례군"],
# "제주특별자치도": ["제주시", "서귀포시"]


# 변환 로직
with open('dong.txt.new', 'r', encoding='utf-8') as f:
    regions = [line.strip() for line in f if line.strip()]




# for sido, sigungu_list in area_data.items():
#     for sigungu in sigungu_list:
#         regions.append({
#             "name": sigungu,
#             "region": f"{sido} {sigungu}"
#         })


categories = [
    {"category": "변기"},
    {"category": "세면대"},
    {"category": "수전"},
]

dos = [
    '막힘', '교체', '수리', '고장'
]


all_images = [f"/images/{i}.png" for i in range(1, 7)] # 1.jpg ~ 20.jpg 가 있다고 가정



def clean_xml_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            xml_start_index = content.find('<?xml')

            if xml_start_index != -1:
                cleaned_content = content[xml_start_index:].strip()

                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    f.write(cleaned_content)
                print(f"🧹 {file_path} 공백 완벽 제거 완료!")
            else:
                print(f"⚠️ {file_path}에서 xml 선언문을 찾지 못했습니다.")

        except Exception as e:
            print(f"❌ {file_path} 처리 중 에러: {e}")


def prepare_content(num, images_str):
    if os.path.exists("content"):
        shutil.rmtree("content")
    os.makedirs("content")

    selected_imgs = random.sample(all_images, 6)

    img_param = str(selected_imgs).replace("'", '"')
    print(img_param)

    with open("content/_index.md", "w", encoding="utf-8") as f:
        region = '서울 특별시'
        category = categories[num - 1]['category'] + random.choice(dos)
        unique_body = generate_random_body(region, category)
        summary = f"{region}{category} 전문 업체입니다. 24시 신속 출동 및 정직한 비용으로 해결해 드립니다."
        f.write(f''f'---\n'
                f'title: "{region} {category} 업체 가장 잘하는 곳"\n'
                f'description: "{unique_body}"\n' # 👈 이 줄을 추가하세요!
                f'region: "{region}"\n'
                f'category: "{category}"\n'
                f'date: {today_str}\n'
                f'unique_body: "{unique_body}"\n'
                f'images: {images_str}\n' # 👈 이미지 리스트 주입
                f'id: "0"\n'
                f'---\n')

    counter = 1
    for region in regions:
        for action in dos:
            category = categories[num - 1]['category'] + action
            summary = f"{region} {category} 전문 업체입니다. 24시 신속 출동 및 정직한 비용으로 해결해 드립니다."
            unique_title = generate_random_title(region, category)
            unique_body = generate_random_body(region, category)
            selected_imgs = random.sample(all_images, 6)
            img_param = str(selected_imgs).replace("'", '"')
            with open(f"content/{counter}.md", "w", encoding="utf-8") as f:
                f.write(f''f'---\n'
                        f'title: "{unique_title}"\n'
                        f'description: "{unique_body}"\n' # 👈 이 줄을 추가하세요!
                        f'region: "{region}"\n'
                        f'category: "{category}"\n'
                        f'date: {today_str}\n'
                        f'images: {images_str}\n' # 👈 이미지 리스트 주입
                        f'id: "{counter}"\n'
                        f'unique_body: "{unique_body}"\n'
                        f'---\n') # 랜덤 생성된 본문 주입
            counter += 1

def deploy_all():
    for i, site in enumerate(sites, start=1):
        site_name = site['name']
        print(site, site_name)
        site_url = f"https://{site_name}.netlify.app"

        print(f"\n--- 🚀 [{site_name}] 배포 프로세스 시작 ---")
        all_images = [f"{site_url}/images/{i}.png" for i in range(1, 7)]
        shuffled_images = random.sample(all_images, 5) # 5개를 무작위로 선택
        images_str = "[" + ",".join([f'"{img}"' for img in shuffled_images]) + "]"
        prepare_content(i, images_str)

        print(f"🔨 빌드 중: {site_url}")
        output_dir = f"public_{site_name}"
        cmd = f'hugo -b "{site_url}/" --destination {output_dir} --cleanDestinationDir'

        env = os.environ.copy()
        env["HUGO_BASEURL"] = f"{site_url}/" # 환경변수로 한 번 더 쐐기 박기

        subprocess.run(cmd, env=env, shell=True, check=True)

        # 3. 빌드된 사이트맵 청소 (새로 만든 폴더 안의 파일을 청소)
        sitemap_path = f"{output_dir}/sitemap.xml"
        clean_xml_file(sitemap_path)
        clean_xml_file(f"{output_dir}/index.xml")

        # res = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json={"name": site_name})
        #
        # if res.status_code == 200:
        #     site_id = res.json()['id']
        # else:
        #     res_list = requests.get("https://api.netlify.com/api/v1/sites", headers=headers)
        #     site_id = next(s['id'] for s in res_list.json() if s['name'] == site_name)
        #
        # print(f"📦 Netlify 배포 중...")
        # try:
        #     subprocess.run(
        #         ["netlify", "deploy", "--prod", "--dir", output_dir, "--site", site_id],
        #         shell=True, check=True
        #     )
        #     print(f"✅ {site_name} 배포 완료!")
        # except subprocess.CalledProcessError:
        #     print(f"❌ {site_name} 배포 실패. (Netlify 사이트 이름이 정확한지 확인하세요.)")
        #

if __name__ == "__main__":
    deploy_all()
