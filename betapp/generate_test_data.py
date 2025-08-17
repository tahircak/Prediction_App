import csv
import random
from datetime import datetime, timedelta
import uuid

# Türk takımları
TURKISH_TEAMS = [
    "Fenerbahce", "Galatasaray", "Besiktas", "Trabzonspor", "Adana Demirspor", 
    "Antalyaspor", "Konyaspor", "Kayserispor", "Alanyaspor", "Sivasspor",
    "Kasimpasa", "Fatih Karagumruk", "Gaziantep FK", "Istanbul Basaksehir", "Karagumruk",
    "Ankaragucu", "Pendikspor", "Hatayspor", "Rizespor", "Samsunspor"
]

# Avrupa takımları
EUROPEAN_TEAMS = [
    "Real Madrid", "Barcelona", "Manchester City", "Liverpool", "Arsenal",
    "Manchester United", "Chelsea", "Tottenham", "Bayern Munich", "Borussia Dortmund",
    "PSG", "Marseille", "Lyon", "Juventus", "Inter Milan", "AC Milan",
    "Napoli", "Roma", "Lazio", "Ajax", "PSV", "Porto", "Benfica",
    "Atletico Madrid", "Sevilla", "Valencia", "Villarreal", "RB Leipzig",
    "Bayer Leverkusen", "Wolfsburg", "Monaco", "Nice", "Lille", "Rennes"
]

# Ligler
LEAGUES = [
    "Super Lig", "Premier Lig", "La Liga", "Bundesliga", "Serie A", 
    "Ligue 1", "Eredivisie", "Primeira Liga", "Champions League", "Europa League",
    "Conference League", "Copa del Rey", "FA Cup", "DFB Pokal", "Coppa Italia"
]

# Tahmin türleri
TIP_TYPES = ["home_win", "away_win", "draw", "over_under", "both_teams_score", "correct_score"]

# Tahmin değerleri
TIP_VALUES = {
    "home_win": ["1", "1X", "12"],
    "away_win": ["2", "X2", "12"],
    "draw": ["X", "1X", "X2"],
    "over_under": ["Over 1.5", "Over 2.5", "Over 3.5", "Under 2.5", "Under 3.5"],
    "both_teams_score": ["Yes", "No"],
    "correct_score": ["1-0", "2-0", "2-1", "3-1", "3-2", "0-0", "1-1", "2-2"]
}

def generate_random_match(match_id):
    # Rastgele tarih (gelecek 30 gün içinde)
    base_date = datetime.now()
    random_days = random.randint(1, 30)
    match_date = base_date + timedelta(days=random_days)
    
    # Rastgele saat (14:00-22:00 arası)
    random_hour = random.randint(14, 22)
    random_minute = random.choice([0, 15, 30, 45])
    kickoff_time = match_date.replace(hour=random_hour, minute=random_minute)
    
    # Rastgele lig
    league = random.choice(LEAGUES)
    
    # Rastgele takımlar
    if league == "Super Lig":
        home_team = random.choice(TURKISH_TEAMS)
        away_team = random.choice([t for t in TURKISH_TEAMS if t != home_team])
    else:
        home_team = random.choice(EUROPEAN_TEAMS)
        away_team = random.choice([t for t in EUROPEAN_TEAMS if t != home_team])
    
    # Rastgele tahmin
    tip_type = random.choice(TIP_TYPES)
    tip_value = random.choice(TIP_VALUES[tip_type])
    
    # Rastgele güven yüzdesi (60-95 arası)
    confidence = random.randint(60, 95)
    
    # Rastgele oran (1.5-3.0 arası)
    odds = round(random.uniform(1.5, 3.0), 2)
    
    # Rastgele analiz notu
    analysis_notes = [
        "Form durumu iyi", "Ev sahibi avantajı", "Derbi atmosferi", 
        "Sakatlık sorunları", "Motivasyon yüksek", "Taktik avantaj",
        "Hava koşulları uygun", "Seyirci desteği", "Teknik direktör değişikliği",
        "Transfer dönemi etkisi", "Avrupa kupası yorgunluğu", "Lig pozisyonu baskısı"
    ]
    analysis_note = random.choice(analysis_notes)
    
    # Premium oranı (%30 premium)
    is_premium = random.random() < 0.3
    
    return {
        "match_id": str(match_id),
        "match_date_utc": match_date.strftime("%Y-%m-%d"),
        "league": league,
        "home_team": home_team,
        "away_team": away_team,
        "kickoff_utc": kickoff_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tip_type": tip_type,
        "tip_value": tip_value,
        "confidence_percent": confidence,
        "odds_decimal": odds,
        "analysis_note": analysis_note,
        "is_premium": str(is_premium).lower()
    }

def generate_test_data(num_matches=300):
    matches = []
    
    for i in range(1, num_matches + 1):
        match = generate_random_match(i)
        matches.append(match)
    
    return matches

def save_to_csv(matches, filename="test_data_300.csv"):
    fieldnames = [
        "match_id", "match_date_utc", "league", "home_team", "away_team",
        "kickoff_utc", "tip_type", "tip_value", "confidence_percent",
        "odds_decimal", "analysis_note", "is_premium"
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)
    
    print(f"✅ {len(matches)} adet maç verisi {filename} dosyasına kaydedildi!")
    print(f"📊 Premium maç sayısı: {sum(1 for m in matches if m['is_premium'] == 'true')}")
    print(f"📊 Ücretsiz maç sayısı: {sum(1 for m in matches if m['is_premium'] == 'false')}")

if __name__ == "__main__":
    print("🎲 Rastgele maç verileri oluşturuluyor...")
    matches = generate_test_data(300)
    save_to_csv(matches)
    
    # İlk 5 maçı göster
    print("\n📋 İlk 5 maç örneği:")
    for i, match in enumerate(matches[:5], 1):
        print(f"{i}. {match['home_team']} vs {match['away_team']} ({match['league']}) - {match['tip_value']} ({match['confidence_percent']}%)")
