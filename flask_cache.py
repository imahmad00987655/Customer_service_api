from flask import Flask, jsonify, request
import aiohttp
import asyncio
from flask_caching import Cache
from flask_cors import CORS
import json
from flask_apscheduler import APScheduler
from datetime import datetime
from pytz import timezone
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure Cache
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 86400  # 24 hours
cache = Cache(app)

# Enable CORS
CORS(app)

# Load Node.js API URL from environment variable (with default)
NODE_API_BASE_URL = os.getenv('NODE_API_BASE_URL', 'http://localhost:3006')

# Fetch data from Node.js API
async def fetch_data_from_node_api():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{NODE_API_BASE_URL}/callcenterreportdata/getdata') as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Failed to fetch data: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Exception during fetch: {str(e)}")
        return None

# Update Cache
def update_cache():
    try:
        logger.info(f"Updating cache at {datetime.now(timezone('Asia/Karachi'))}...")
        data = asyncio.run(fetch_data_from_node_api())

        if data is not None:
            cache.set('callcenter_report_data', data)
            logger.info("Cache updated successfully!")
        else:
            logger.warning("No data retrieved; cache not updated.")
    except Exception as e:
        logger.error(f"Failed to update cache: {str(e)}")

# Route to fetch call center data with optional filtering
@app.route('/callcenterreportdata', methods=['GET'])
def call_center_report_data():
    try:
        # Get filter parameters from query parameters
        user_no = request.args.get('user_no')
        level_type = request.args.get('level-type')
        khi_lhr = request.args.get('khi/lhr?')
        using = request.args.get('using???? Yes/No')

        # Check if cached data exists
        cached_data = cache.get('callcenter_report_data')

        if cached_data:
            logger.info("Returning cached data")
            data = cached_data
        else:
            logger.info("Fetching new data from Node.js API")
            data = asyncio.run(fetch_data_from_node_api())

            if data is None:
                return jsonify({'error': 'Failed to fetch data', 'details': 'No data retrieved'}), 500

            # Cache the fetched data
            cache.set('callcenter_report_data', data)

        # Apply filters based on the provided query parameters
        filtered_data = data

        if user_no:
            filtered_data = [item for item in filtered_data if item.get('user_no') == user_no]
        if level_type:
            filtered_data = [item for item in filtered_data if item.get('level-type') == level_type]
        if khi_lhr:
            filtered_data = [item for item in filtered_data if item.get('khi/lhr?') == khi_lhr]
        if using:
            filtered_data = [item for item in filtered_data if item.get('using???? Yes/No') == using]

        if not filtered_data:
            return jsonify({'error': 'No data found for the specified filters'}), 404

        # Return filtered data
        return app.response_class(response=json.dumps(filtered_data), mimetype='application/json')

    except Exception as e:
        logger.error(f"Error in /callcenterreportdata: {str(e)}")
        return jsonify({'error': 'Failed to fetch data', 'details': str(e)}), 500

# Scheduler Configuration
class Config:
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()
scheduler.init_app(app)
app.config.from_object(Config)

scheduler.add_job(
    id='update_cache_job',
    func=update_cache,
    trigger='cron',
    hour=1,  # 1 AM
    minute=30,  # 30 minutes
    timezone=timezone('Asia/Karachi'),
    replace_existing=True
)

scheduler.start()
logger.info(f"Next cache update scheduled at: {scheduler.get_job('update_cache_job').next_run_time}")

if __name__ == '__main__':
    # For development only; removed in production
    app.run(host="0.0.0.0", port=5008)