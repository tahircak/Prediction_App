import requests
import time

def test_api():
    print("🔍 API test ediliyor...")
    
    # API'nin başlaması için bekle
    time.sleep(3)
    
    try:
        # Ana endpoint'i test et
        response = requests.get("http://127.0.0.1:8000/matches", timeout=5)
        print(f"✅ API çalışıyor! Status: {response.status_code}")
        print(f"📊 Maç sayısı: {len(response.json())}")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ API çalışmıyor! Bağlantı hatası.")
        return False
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    test_api()
