# Vanna AI Demo App with Qdrant and OpenRouter

A Flask-based web application that demonstrates natural language to SQL query conversion using Vanna AI, with Qdrant as the vector store and OpenRouter for LLM capabilities. This application allows users to ask questions in natural language and get SQL queries and their results from a Snowflake database.

## Features

- Natural language to SQL query conversion
- Vector storage with Qdrant for efficient similarity search
- Integration with OpenRouter for LLM capabilities
- Snowflake database integration
- RESTful API endpoints for:
  - Generating SQL queries from natural language questions
  - Executing SQL queries
  - Managing training data
  - Retrieving available questions
  - Vector collection management

## Prerequisites

- Python 3.x
- Snowflake account
- Qdrant account/instance
- OpenRouter API key
- Cloudflare API Gateway setup

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
SNOWFLAKE_WAREHOUSE=your_snowflake_warehouse
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=your_snowflake_username
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ROLE=your_snowflake_role
CLOUDFLARE_API_GATEWAY_NAME=your_cloudflare_gateway_name
CLOUDFLARE_API_GATEWAY_TOKEN=your_cloudflare_gateway_token
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vanna-qdrant-openrouter-demo-app
```

2. Create and activate a virtual environment:
```bash
make venv
source venv/bin/activate
```

3. Install dependencies:
```bash
make install
```

## Development

To run the development server:
```bash
make dev
```

The application will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Health check endpoint
- `GET /api/collections`: Get all vector collections
- `GET /api/questions`: Get suggested questions
- `POST /api/generate-sql`: Generate SQL from natural language
- `POST /api/run-sql`: Execute SQL query
- `GET /api/training-data`: Get current training data
- `DELETE /api/remove-all-training-data`: Remove all training data
- `POST /api/ingest-training-data-from-file`: Add new training data

## Deployment

This project is configured for deployment on Railway. To deploy:

```bash
make deploy
```

## Project Structure

```
.
├── app/
│   ├── api/            # API routes and handlers
│   ├── core/           # Core configuration and setup
│   ├── models/         # Data models and schemas
│   └── services/       # Business logic and services
├── docs/              # Documentation files
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
├── Makefile          # Development commands
└── nixpacks.toml     # Railway deployment configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 