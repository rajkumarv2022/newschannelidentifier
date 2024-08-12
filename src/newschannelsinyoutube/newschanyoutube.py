import csv
import re

# Raw data as a multi-line string
raw_data = """
#1 Zee News YouTube channel avatar Zee News 183.48K 37M 22.54B
#2 Narendra Modi YouTube channel avatar Narendra Modi 27.32K 25.1M 5.88B
#3 SOMOY TV YouTube channel avatar SOMOY TV 204.46K 24.5M 16.76B
#4 Jamuna TV YouTube channel avatar Jamuna TV 142.23K 21.8M 17.43B
#5 NMF News YouTube channel avatar NMF News 130.8K 19.2M 8.81B
#6 BBC News Hindi YouTube channel avatar BBC News Hindi 26.87K 19M 8.63B
#7 NDTV India YouTube channel avatar NDTV India 126.67K 17.5M 8.06B
#8 CNN YouTube channel avatar CNN 166.16K 16.7M 16.29B
#9 Tu COSMOPOLIS YouTube channel avatar Tu COSMOPOLIS 10.95K 16.7M 5.15B
#10 Daftar Populer YouTube channel avatar Daftar Populer 4.74K 15.8M 2.34B
#11 The Infographics Show YouTube channel avatar The Infographics Show 5.03K 14.3M 5.97B
#12 tvOneNews YouTube channel avatar tvOneNews 151.14K 14.1M 9.2B
#13 Knowledge Tv हिन्दी YouTube channel avatar Knowledge Tv हिन्दी 4.79K 13.5M 2.22B
#14 Channel 24 YouTube channel avatar Channel 24 146.79K 12.3M 6.61B
#15 Fox News YouTube channel avatar Fox News 108.11K 11.7M 17.46B
#16 BBC News عربي 41.47K 11.7M 4.98B
#17 Ravish Kumar Official 719 11.5M 1.49B
#18 เรื่องเล่าเช้านี้ 132.79K 11.2M 8.23B
#19 CNN Indonesia 112.24K 11.2M 6.11B
#20 Navbharat Times नवभारत टाइम्स 86.44K 10.7M 4.37B
#21 Nondito Tv 469 10.6M 173.01M
#22 HIT TV Today 11.65K 10.5M 19.05M
#23 NBC News 67.22K 10.3M 7.55B
#24 EnnaharTv 133.11K 10.3M 3.7B
#25 вДудь 193 10.3M 2.23B
#26 Sab Kuchh Sekho Jano 3.55K 10.1M 1.1B
#27 Independent Television 144.37K 10M 4.91B
#28 National Dastak 46.42K 9.61M 3.75B
#29 Live Hindustan 69.67K 9.57M 4.39B
#30 LastWeekTonight 561 9.55M 3.95B
#31 India Today 198.69K 9.42M 4B
#32 Manorama News 455.44K 9.34M 10.18B
#33 Headlines India 14.11K 9.33M 3.27B
#34 Rahul Gandhi 2.56K 8.58M 2.16B
#35 Sansad TV 84.73K 8.29M 1.59B
#36 NMás 117.4K 8.24M 6.26B
#37 Jovem Pan News 145.92K 8.15M 4.95B
#38 CNN-News18 185.09K 8M 3.91B
#39 DB Live 78.02K 7.98M 3.93B
#40 Amar Ujala 103.96K 7.61M 2.84B
#41 TRT World 55.31K 7.6M 1.83B
#42 RealLifeLore 367 7.54M 1.66B
#43 عربي TRT 36.28K 7.51M 1.16B
#44 Al Jazeera Mubasher قناة الجزيرة مباشر 79.58K 7.5M 2.78B
#45 The Live Tv 14.16K 7.43M 3.68B
#46 ANTV - Truyền hình Công an Nhân dân 64.35K 7.33M 3.69B
#47 24 Канал 256.73K 7.32M 11.12B
#48 SOMOY TV Bulletin 63.02K 7.27M 2.54B
#49 Yaaro Ka Yaar DOST 386 7.26M 1.02B
#50 News18 UP Uttarakhand 175.34K 7.2M 2.94B
#51 It’s aman07 551 7.11M 1.35B
#52 Hindustan Times 65.66K 7.1M 5.38B
#53 Aaj Tak HD 89.1K 7.06M 2.74B
#54 MILENIO 207.4K 7.05M 5.68B
#55 Abhisar Sharma 2.53K 6.91M 2.01B
#56 FRANCE 24 119.23K 6.9M 3.05B
#57 Russell Brand 2.99K 6.85M 1.37B
#58 Live Cities Media Private Limited 82.2K 6.65M 2.75B
#59 ANI News 153.53K 6.59M 3.42B
#60 Yunus Khan 975 6.59M 1.5B
#61 Jair Bolsonaro 3.99K 6.59M 366.04M
#62 ABP Ganga 175.93K 6.55M 3.65B
#63 Philip DeFranco 2.02K 6.55M 2.18B
#64 HJ NEWS 36.06K 6.45M 2.48B
#65 Gaurav Thakur 804 6.31M 1.11B
#66 InKhabar Official 110.43K 6.27M 1.76B
#67 Ajit Anjum 4.09K 6.26M 1.85B
#68 Bharatiya Janata Party 43.55K 6.11M 2.22B
#69 Báo Thanh Niên 61.48K 5.82M 5.82B
#70 Valuetainment 4.73K 5.82M 1.51B
#71 ISPR Official 1.27K 5.77M 1.54B
#72 StevenCrowder 1.8K 5.75M 1.9B
#73 VTV24 40.45K 5.73M 4.53B
#74 News18 MP Chhattisgarh 139.55K 5.72M 2.01B
#75 matichon tv 60.06K 5.7M 3.79B
#76 DW Documentary 1.15K 5.69M 824.71M
#77 News Express 79.72K 5.68M 1.5B
#78 سكاي نيوز عربية 176.1K 5.67M 2.87B
#79 The Telegraph 34.94K 5.66M 4.15B
#80 The Sun 22.48K 5.62M 4.73B
#81 El Universal 117.03K 5.55M 6.26B
#82 Band Jornalismo 141.17K 5.55M 2.64B
#83 Indian National Congress 32.31K 5.53M 2.19B
#84 Sikera Junior 9.94K 5.52M 1.32B
#85 The Wall Street Journal 27.72K 5.48M 1.96B
#86 AP Archive 604.58K 5.47M 3.05B
#87 TIMES NOW 126.36K 5.47M 2.73B
#88 The Wire 10.3K 5.46M 2.63B
#89 We On News 141.27K 5.39M 3.06B
#90 Os Pingos nos Is 15.04K 5.35M 3.24B
#91 DW News 35.44K 5.35M 2.43B
#92 Timeline - World History Documentaries 1.14K 5.3M 1.16B
#93 ATN Bangla News 47.82K 5.24M 1.78B
#94 SPN9NEWS सामाजिक आईना 103.62K 5.2M 2.13B
#95 News7 Tamil 138.26K 5.2M 1.85B
#96 Alsharqiya Tube 28.11K 5.18M 748.6M
#97 TOÀN CẢNH 24H 74.13K 5.17M 5.05B
#98 CNN Brasil 94.14K 5.14M 3.03B
#99 Citizen TV Kenya 176.44K 5.12M 2.06B
#100 varlamov 1.8K 5.12M 1.73B
"""

# Function to parse the raw data
def parse_data(raw_data):
    channels = []
    pattern = re.compile(r'#(\d+)\s+([^\d]+)\s+(\d+\.?\d*[KM]*)\s+(\d+\.?\d*[KM]*)\s+(\d+\.?\d*[BM]*)')
    matches = pattern.finditer(raw_data)
    
    for match in matches:
        rank = match.group(1)
        name = match.group(2).strip()
        subscribers = match.group(3).strip()
        views = match.group(4).strip()
        total_views = match.group(5).strip()
        channels.append({
            'Rank': rank,
            'Name': name,
            'Subscribers': subscribers,
            'Views': views,
            'Total Views': total_views
        })
    
    return channels

# Parse the data
channels = parse_data(raw_data)

# Display the results
for channel in channels:
    print(f"Rank: {channel['Rank']}, Name: {channel['Name']}, Subscribers: {channel['Subscribers']}, Views: {channel['Views']}, Total Views: {channel['Total Views']}")


# Write to CSV
csv_file_path = 'youtube_channels.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Rank', 'Name', 'Subscribers', 'Views', 'Total Views'])
    writer.writeheader()
    writer.writerows(channels)

print(f"Data has been written to {csv_file_path}")