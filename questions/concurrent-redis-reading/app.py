from flask import Flask, render_template, request, jsonify
import redis
import psycopg2
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Redis connection
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_db = int(os.environ.get('REDIS_DB', 0))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'localhost'),
        port=os.environ.get('POSTGRES_PORT', 5432),
        user=os.environ.get('POSTGRES_USER', 'postgres'),
        password=os.environ.get('POSTGRES_PASSWORD', ''),
        database=os.environ.get('POSTGRES_DB', 'postgres')
    )

def generate_cache_key(query, params=None):
    """Generate a unique cache key for SQL query"""
    key_parts = [query]
    if params:
        key_parts.append(json.dumps(params, sort_keys=True))
    return f"sql:{hash(''.join(key_parts))}"

def execute_query_with_cache(query, params=None, cache_ttl=300):
    """Execute SQL query with Redis caching"""
    cache_key = generate_cache_key(query, params)
    
    # Try to get from cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result), True  # Return cached result
    
    # If not in cache, execute query against PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            # Convert datetime objects to strings for JSON serialization
            serializable_rows = []
            for row in results:
                serializable_row = []
                for value in row:
                    if hasattr(value, 'isoformat'):
                        serializable_row.append(value.isoformat())
                    else:
                        serializable_row.append(value)
                serializable_rows.append(serializable_row)
            
            result_data = {
                'columns': columns,
                'rows': serializable_rows,
                'cached_at': datetime.now().isoformat()
            }
            
            # Store in Redis with TTL
            redis_client.setex(cache_key, cache_ttl, json.dumps(result_data))
            return result_data, False
        else:
            conn.commit()
            return {'affected_rows': cursor.rowcount}, False
            
    finally:
        cursor.close()
        conn.close()

def invalidate_cache_pattern(pattern):
    """Invalidate cache entries matching pattern"""
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def execute_query():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    query = data['query']
    params = data.get('params')
    cache_ttl = data.get('cache_ttl', 300)  # Default 5 minutes
    
    try:
        result, from_cache = execute_query_with_cache(query, params, cache_ttl)
        response = {
            'result': result,
            'from_cache': from_cache,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users')
def get_users():
    """Example endpoint with caching"""
    query = "SELECT id, name, email, created_at FROM users ORDER BY created_at DESC"
    result, from_cache = execute_query_with_cache(query, cache_ttl=60)
    
    return jsonify({
        'users': result,
        'from_cache': from_cache,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/users', methods=['POST'])
def create_user():
    """Create user and invalidate cache"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    query = "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id"
    params = (data['name'], data['email'])
    
    try:
        result, _ = execute_query_with_cache(query, params)
        
        # Invalidate user-related cache
        invalidate_cache_pattern("sql:*users*")
        invalidate_cache_pattern("sql:*SELECT*FROM*users*")
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': result['affected_rows']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)