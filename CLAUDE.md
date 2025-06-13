# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI application deployed on Vercel with Supabase as the backend database. The application provides REST APIs for user and message management with full CRUD operations.

## Key Commands

### Development
- `make dev` - Start local development server with hot reload
- `make install` - Install Python dependencies
- `uvicorn main:app --reload` - Alternative way to start development server

### Database
- Run `database_setup.sql` in Supabase SQL Editor to create tables and initial data
- `./migrate.sh` - Run database migrations using Supabase CLI
- Use `/check-tables` endpoint to verify table creation

### Deployment
- `make deploy` - Deploy to Vercel
- `vercel --prod` - Direct Vercel deployment command

## Architecture

### Core Components
- **main.py**: FastAPI application with all endpoints and data models
- **supabase_simple.py**: Supabase client initialization and connection management
- **database_setup.sql**: Database schema and initial data

### Database Schema
- **users table**: id, name, email, created_at, updated_at
- **messages table**: id, message, user_id (FK), created_at, updated_at
- Foreign key relationship: messages.user_id → users.id

### API Structure
- Health check endpoints: `/health`, `/time`, `/stats`
- User CRUD: `/users` (GET, POST), `/users/{id}` (GET, PUT, DELETE)
- Message CRUD: `/messages` (GET, POST), `/messages/{id}` (GET, DELETE)
- Admin endpoints: `/init-supabase`, `/check-tables`

## Environment Variables

Required for both local development and Vercel deployment:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_SERVICE_KEY` - Supabase service role key

## Development Notes

### Supabase Integration
- Global `supabase` and `supabase_admin` clients initialized in supabase_simple.py
- Connection testing with retry logic implemented
- Graceful degradation when database is unavailable

### Error Handling
- Comprehensive exception handling in all endpoints
- HTTP status codes properly mapped to error conditions
- Logging configured for debugging database operations

### Data Models
- Pydantic models for request/response validation
- Separate Create/Update models for different operations
- Optional fields properly handled for partial updates