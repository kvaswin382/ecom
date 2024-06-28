from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

# Define OCR function
def perform_ocr(image_path):
    try:
        # Load the image
        image = Image.open(image_path)
        
        # Perform OCR on the image
        text = pytesseract.image_to_string(image)
        
        return text.strip()  # Strip whitespace from the extracted text
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Define keywords for different platforms
PLATFORM_KEYWORDS = {
    'amazon': ["Order date", "Order #", "Order total", "View order details", 
               "View Order Summary", "Download Invoice", "Shipment details", 
               "Delivery Estimate"],
    'flipkart': [ "Order Details", "Order ID", "Order Confirmed", "Cancel"],
    'nykaa': ["Order Details","ORDER ID","PLACED","TOTAL"],
    'meesho': ["ORDER DETAILS","Sub Order ID","Product Details","Order Tracking","Order Details","Price Details","Total Price","Order Total"],
    'myntra': ["Arriving By","Placed","Order placed","Total Order Price","Order ID #"]
}

# Define API endpoint for handling GET requests with platform parameter
@app.route('/<platform>/check', methods=['GET'])
def analyze_image(platform):
    # Validate platform
    keywords = PLATFORM_KEYWORDS.get(platform)
    if keywords is None:
        return jsonify({'ok': False, 'msg': f'Invalid platform {platform}'}), 400
    
    # Get image_path parameter from GET request
    image = request.args.get('img', '')
    image_path = f'/img/{str(image)}.jpg'
    if not image:
        return jsonify({'ok': False, 'msg': 'Missing image_path parameter'}), 400
    
    # Perform OCR on the image
    extracted_text = perform_ocr(image_path)
    
    if extracted_text:
        # Check if keywords are present in the extracted text
        is_order_screenshot = all(keyword in extracted_text for keyword in keywords)
        
        # Prepare JSON response
        response = {
            'ok': True,
            'platform': platform,
            'image_path': image_path,
            'extracted_text': extracted_text,
            'is_order_screenshot': is_order_screenshot
        }
        return jsonify(response), 200
    else:
        return jsonify({'ok': False, 'msg': 'Failed to process image'}), 500

if __name__ == '__main__':
    app.run(debug=True)