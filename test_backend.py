import requests
import json

print("🧪 Testing Backend Integration...")

# Test backend ML route
try:
    data = {
        "description": "A modern Indian villa with glass windows"
    }
    
    response = requests.post(
        "http://localhost:5000/api/ml/generate-house", 
        json=data,
        timeout=30
    )
    
    print(f"✅ Backend Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: {result.get('success', False)}")
        print(f"✅ Message: {result.get('message', 'N/A')}")
        print(f"\n📋 Backend Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Backend Error: {response.text}")
        
except Exception as e:
    print(f"❌ Backend Test Failed: {e}")

print("\n🔚 Backend Test Complete!")