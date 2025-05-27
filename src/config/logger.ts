import pino, { Logger } from 'pino';
import pretty = require('pino-pretty');
import { config } from './index';

// Determine if we're in development mode
const isDevelopment = config.ENV === 'development';

// Create a stream for pretty printing in development
const prettyStream = pretty({
  colorize: true,
  translateTime: true,
  ignore: 'pid,hostname',
});

// Configure the logger based on the environment
const logger: Logger = pino({
  level: config.LOG_LEVEL,
  name: config.SERVICE_NAME,
  base: {
    env: config.ENV,
    service: config.SERVICE_NAME,
  },
  transport: isDevelopment
    ? {
        target: 'pino-pretty',
        options: {
          colorize: true,
          translateTime: true,
          ignore: 'pid,hostname',
        },
      }
    : undefined,
});

// Export the logger for use throughout the application
export default logger;