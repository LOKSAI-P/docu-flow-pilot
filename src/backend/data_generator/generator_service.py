
"""
Sample Data Generator
Generate fake JSON/XML records using templates.
"""
import os
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from jinja2 import Template
from faker import Faker
import requests

class DataGeneratorService:
    def __init__(self):
        self.faker = Faker()
        self.templates = {}

    def load_template(self, template_id, template_content, template_type="json"):
        """Load a template for generating data"""
        self.templates[template_id] = {
            "content": template_content,
            "type": template_type
        }
        return {"status": "success", "message": f"Template {template_id} loaded"}

    def generate_data(self, template_id, count=1):
        """Generate data using the specified template"""
        if template_id not in self.templates:
            return {"status": "error", "message": f"Template {template_id} not found"}
        
        template_data = self.templates[template_id]
        
        try:
            template = Template(template_data["content"])
            results = []
            
            for _ in range(count):
                # Create a dictionary of faker functions
                faker_dict = {
                    "name": self.faker.name(),
                    "address": self.faker.address(),
                    "email": self.faker.email(),
                    "company": self.faker.company(),
                    "job": self.faker.job(),
                    "phone": self.faker.phone_number(),
                    "ssn": self.faker.ssn(),
                    "date": self.faker.date(),
                    "time": self.faker.time(),
                    "datetime": self.faker.date_time().isoformat(),
                    "uuid": str(self.faker.uuid4()),
                    "number": self.faker.random_int(min=1, max=100),
                    "decimal": self.faker.random_number(digits=2) / 100,
                    "paragraph": self.faker.paragraph(),
                    "sentence": self.faker.sentence(),
                    "word": self.faker.word(),
                    "url": self.faker.url(),
                    "image_url": self.faker.image_url(),
                    "ipv4": self.faker.ipv4(),
                    "ipv6": self.faker.ipv6(),
                    "user_agent": self.faker.user_agent(),
                    "color": self.faker.color_name(),
                    "hex_color": self.faker.hex_color(),
                    "rgb_color": self.faker.rgb_color(),
                    "credit_card_number": self.faker.credit_card_number(),
                    "credit_card_provider": self.faker.credit_card_provider(),
                    "currency_code": self.faker.currency_code(),
                    "currency_name": self.faker.currency_name(),
                    "cryptocurrency_name": self.faker.cryptocurrency_name(),
                    "cryptocurrency_code": self.faker.cryptocurrency_code(),
                    "iban": self.faker.iban(),
                }
                
                # Render the template with faker data
                result = template.render(faker=faker_dict)
                
                if template_data["type"].lower() == "json":
                    # Parse as JSON to ensure validity
                    result = json.loads(result)
                elif template_data["type"].lower() == "xml":
                    # Parse as XML to ensure validity
                    root = ET.fromstring(result)
                    result = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
                
                results.append(result)
            
            return {
                "status": "success", 
                "data": results if count > 1 else results[0],
                "format": template_data["type"]
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def upload_to_confluence(self, page_id, content, content_type, base_url, auth_token):
        """Upload generated data to Confluence page"""
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        # First, get the current version of the page
        version_url = f"{base_url}/rest/api/content/{page_id}"
        try:
            response = requests.get(version_url, headers=headers)
            response.raise_for_status()
            
            page_data = response.json()
            current_version = page_data.get("version", {}).get("number", 1)
            
            # Prepare content based on type
            if content_type.lower() == "json":
                formatted_content = f"<ac:structured-macro ac:name=\"code\"><ac:parameter ac:name=\"language\">json</ac:parameter><ac:plain-text-body><![CDATA[{json.dumps(content, indent=2)}]]></ac:plain-text-body></ac:structured-macro>"
            else:  # XML
                formatted_content = f"<ac:structured-macro ac:name=\"code\"><ac:parameter ac:name=\"language\">xml</ac:parameter><ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body></ac:structured-macro>"
            
            # Update the page
            update_data = {
                "version": {
                    "number": current_version + 1
                },
                "title": page_data.get("title", "Generated Data"),
                "type": "page",
                "body": {
                    "storage": {
                        "value": formatted_content,
                        "representation": "storage"
                    }
                }
            }
            
            update_url = f"{base_url}/rest/api/content/{page_id}"
            update_response = requests.put(
                update_url, 
                headers=headers, 
                data=json.dumps(update_data)
            )
            update_response.raise_for_status()
            
            return {"status": "success", "message": "Data uploaded to Confluence"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
