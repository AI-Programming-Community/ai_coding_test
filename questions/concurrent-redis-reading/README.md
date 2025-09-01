# Redis-PostgreSQL Caching Layer

This application implements a Redis caching layer for PostgreSQL database queries to improve query performance.

## Features

- **Query Caching**: Automatically caches SELECT query results in Redis
- **Smart Cache Keys**: Unique cache keys based on query text and parameters
- **Cache Invalidation**: Automatic cache invalidation on data modifications
- **Configurable TTL**: Customizable cache expiration times
- **Performance Metrics**: Track cache hits/misses and performance improvements

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Copy `.env.example` to `.env` and update with your database credentials:
   ```bash
   cp .env.example .env
   ```

3. **Initialize database**:
   ```bash
   python init_db.py
   ```

4. **Start the application**:
   ```bash
   python app.py
   ```

## API Endpoints

### Execute SQL Query with Caching
```http
POST /query
Content-Type: application/json

{
  "query": "SELECT * FROM users WHERE name LIKE %s",
  "params": ["%Alice%"],
  "cache_ttl": 300
}
```

### Get Users (Cached)
```http
GET /users
```

### Create User (Invalidates Cache)
```http
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Testing

Run the test suite to verify caching functionality:
```bash
python test_cache.py
```

## Cache Strategy

- **Cache Key Generation**: `sql:hash(query + json_sorted_params)`
- **Default TTL**: 300 seconds (5 minutes)
- **Cache Invalidation**: Pattern-based invalidation on INSERT/UPDATE/DELETE
- **Supported Queries**: Primarily SELECT queries for read operations

## Performance Benefits

- **Reduced Database Load**: Repeated queries served from cache
- **Faster Response Times**: Cache hits are typically 10-100x faster
- **Scalability**: Redis handles high read traffic efficiently

## Environment Variables

- `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` - Redis connection settings
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB` - PostgreSQL connection
- `POSTGRES_USER`, `POSTGRES_PASSWORD` - Database credentials