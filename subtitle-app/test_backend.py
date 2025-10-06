import requests
import sys

def test_backend():
    """Test if backend is running and responding"""
    try:
        print("Testing backend connection...")
        response = requests.get("http://localhost:8001/")
        
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print("\nTo start the backend, run:")
        print("  cd subtitle-app/backend")
        print("  .\\venv\\Scripts\\python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_languages_endpoint():
    """Test the languages endpoint"""
    try:
        print("\nTesting /api/languages endpoint...")
        response = requests.get("http://localhost:8001/api/languages")
        
        if response.status_code == 200:
            print("✅ Languages endpoint working!")
            data = response.json()
            print(f"Available translation languages: {len(data['data']['translation_languages'])}")
            return True
        else:
            print(f"❌ Languages endpoint returned: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Health Check")
    print("=" * 50)
    
    backend_ok = test_backend()
    
    if backend_ok:
        languages_ok = test_languages_endpoint()
        
        if languages_ok:
            print("\n" + "=" * 50)
            print("✅ All tests passed! Backend is healthy.")
            print("=" * 50)
            sys.exit(0)
    
    print("\n" + "=" * 50)
    print("❌ Backend tests failed!")
    print("=" * 50)
    print("\nTroubleshooting:")
    print("1. Check if backend is running: npm run backend")
    print("2. Check backend logs for errors")
    print("3. Verify all dependencies installed: pip install -r requirements.txt")
    print("4. Check .env file has ELEVENLABS_API_KEY set")
    sys.exit(1)
