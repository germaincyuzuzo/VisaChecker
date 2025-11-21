from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

class VisaChecker:
    """Visa checker using free Passport Visa API."""
    
    def __init__(self):
        self.api_base_url = "https://rough-sun-2523.fly.dev"
        self.rest_countries_url = "https://restcountries.com/v3.1"
        self.cache = {}
    
    def get_visa_type_and_docs(self, visa_status):
        """Map visa status to visa type and required documents."""
        visa_info = {
            'Visa Free': {
                'type': 'Tourist/Visitor',
                'documents': [
                    'Valid Passport (6+ months validity)',
                    'Return/Onward ticket',
                    'Proof of accommodation',
                    'Travel insurance (recommended)'
                ]
            },
            'Visa on Arrival': {
                'type': 'Tourist/Visitor (On Arrival)',
                'documents': [
                    'Valid Passport',
                    'Return ticket',
                    'Proof of funds',
                    'Completed application form',
                    'Passport photos (usually 1-2)',
                    'Proof of accommodation'
                ]
            },
            'e-Visa': {
                'type': 'Electronic Visa',
                'documents': [
                    'Valid Passport',
                    'Digital photo (digital submission)',
                    'Email address',
                    'Credit/Debit card for payment',
                    'Return ticket',
                    'Proof of accommodation'
                ]
            },
            'Visa Required': {
                'type': 'Standard Visa',
                'documents': [
                    'Valid Passport',
                    'Completed visa application form',
                    'Passport photos (usually 2-4)',
                    'Proof of funds',
                    'Return ticket',
                    'Letter of invitation (if required)',
                    'Proof of accommodation',
                    'Travel insurance',
                    'Yellow fever vaccination (if applicable)',
                    'Bank statements',
                    'Employment letter',
                    'Hotel reservations'
                ]
            },
            'Not Mentioned': {
                'type': 'Unknown',
                'documents': ['Contact the destination embassy for details']
            }
        }
        
        return visa_info.get(visa_status, visa_info['Not Mentioned'])
    
    def get_country_info(self, country_code):
        """Get country information from REST Countries API."""
        try:
            url = f"{self.rest_countries_url}/alpha/{country_code.lower()}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    data = data[0]
                
                return {
                    'name': data.get('name', {}).get('common', country_code),
                    'capital': data.get('capital', ['N/A'])[0] if data.get('capital') else 'N/A',
                    'region': data.get('region', 'N/A'),
                    'currencies': list(data.get('currencies', {}).keys()),
                    'languages': list(data.get('languages', {}).values()),
                    'population': data.get('population', 'N/A')
                }
        except:
            pass
        
        return {'name': country_code}
    
    def check_visa(self, passport_country, destination_country):
        """Check visa requirements from the free API."""
        passport_country = passport_country.upper()
        destination_country = destination_country.upper()
        
        cache_key = f"{passport_country}_{destination_country}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            url = f"{self.api_base_url}/visa/{passport_country}/{destination_country}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.cache[cache_key] = data
                return data
            else:
                return {'error': f'Invalid country codes. Please use ISO 2-letter codes (e.g., US, JP)'}
        
        except Exception as e:
            return {'error': f'Error fetching data: {str(e)}'}


# Initialize visa checker
visa_checker = VisaChecker()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/check-visa', methods=['POST'])
def check_visa_api():
    """API endpoint to check visa requirements."""
    data = request.json
    passport = data.get('passport', '').upper()
    destination = data.get('destination', '').upper()
    
    if not passport or not destination:
        return jsonify({'error': 'Passport and destination codes are required'}), 400
    
    if passport == destination:
        return jsonify({'error': 'Passport and destination countries must be different'}), 400
    
    try:
        # Get visa information from API
        visa_data = visa_checker.check_visa(passport, destination)
        
        if 'error' in visa_data:
            return jsonify(visa_data), 400
        
        # Extract the structure from API response (same as CLI version)
        passport_info = visa_data.get('passport', {})
        destination_info = visa_data.get('destination', {})
        category = visa_data.get('category', {})
        
        # Get visa status from category name
        visa_status = category.get('name', 'N/A')
        
        # Get enhanced country info
        country_info = visa_checker.get_country_info(destination)
        
        # Get visa type and documents
        visa_type_info = visa_checker.get_visa_type_and_docs(visa_status)
        
        # Prepare response matching the web UI expectations
        result = {
            'status': 'success',
            'passport': {
                'code': passport,
                'name': passport_info.get('name', passport)
            },
            'destination': {
                'name': country_info.get('name', destination_info.get('name', destination)),
                'code': destination,
                'capital': country_info.get('capital', 'N/A'),
                'region': country_info.get('region', 'N/A'),
                'currency': ', '.join(country_info.get('currencies', [])) if country_info.get('currencies') else 'N/A',
                'language': ', '.join(country_info.get('languages', [])) if country_info.get('languages') else 'N/A',
                'population': f"{country_info.get('population', 'N/A'):,}" if country_info.get('population') != 'N/A' else 'N/A'
            },
            'visa': {
                'status': visa_status,
                'type': visa_type_info.get('type', 'N/A'),
                'stay_duration': visa_data.get('dur', 'Varies'),
                'documents': visa_type_info.get('documents', []),
                'last_updated': visa_data.get('last_updated', 'N/A')
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)