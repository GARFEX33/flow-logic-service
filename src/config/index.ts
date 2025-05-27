import * as dotenv from 'dotenv';
import * as path from 'path';

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, '../../../.env') });

// Define the configuration interface
export interface Config {
  BROKER_URL: string;
  ENV: string;
  SERVICE_NAME: string;
  LOG_LEVEL: string;
  AUDIT_DB_URL?: string;
}

// Load configuration from environment variables
export const config: Config = {
  BROKER_URL: process.env.BROKER_URL || '',
  ENV: process.env.ENV || '',
  SERVICE_NAME: process.env.SERVICE_NAME || '',
  LOG_LEVEL: process.env.LOG_LEVEL || '',
  AUDIT_DB_URL: process.env.AUDIT_DB_URL || undefined,
};

// Check for missing required variables
const requiredKeys = ['BROKER_URL', 'ENV', 'SERVICE_NAME', 'LOG_LEVEL'];
for (const key of requiredKeys) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}