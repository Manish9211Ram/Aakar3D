import requests
import json

# Test ML service
print("🧪 Testing ML Service...")

# Test health
try:
    health_response = requests.get("http://localhost:5001/health")
    print(f"✅ Health Check: {health_response.status_code}")
    print(f"   Response: {health_response.json()}")
except Exception as e:
    print(f"❌ Health Check Failed: {e}")
    exit(1)

# Test generation
try:
    print("\n🏠 Testing House Generation...")
    data = {
        "description": "A traditional Indian house with 2 stories and a balcony"
    }
    
    generate_response = requests.post(
        "http://localhost:5001/generate", 
        json=data,
        timeout=30
    )
    
    print(f"✅ Generation Status: {generate_response.status_code}")
    
    if generate_response.status_code == 200:
        result = generate_response.json()
        print(f"✅ Success: {result['success']}")
        print(f"✅ Message: {result['message']}")
        
        if 'data' in result:
            data = result['data']
            print(f"✅ Processing Time: {data.get('processing_time', 'N/A')}s")
            print(f"✅ Files Generated: {len(data.get('files', []))}")
            
            if 'attributes' in data:
                attrs = data['attributes']
                print(f"✅ Style: {attrs.get('style', 'N/A')}")
                print(f"✅ Floors: {attrs.get('num_floors', 'N/A')}")
                print(f"✅ Type: {attrs.get('house_type', 'N/A')}")
        
        print(f"\n📋 Full Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Generation Failed: {generate_response.text}")
        
except Exception as e:
    print(f"❌ Generation Test Failed: {e}")

print("\n🔚 Test Complete!")