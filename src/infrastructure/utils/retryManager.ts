import asyncRetry, { Options as RetryOptions } from 'async-retry';
import logger from '../../config/logger';

// RetryManager class to handle retry logic for async operations
export class RetryManager {
  constructor(private readonly maxAttempts: number, private readonly delay: number) {}

  // Execute a function with retry logic
  async execute<T>(fn: () => Promise<T>, options?: RetryOptions): Promise<T> {
    const retryOptions: RetryOptions = {
      retries: this.maxAttempts - 1, // async-retry counts from 0
      factor: this.delay,
      ...options,
    };

    try {
      return await asyncRetry(fn, retryOptions);
    } catch (error) {
      logger.error(`RetryManager: Operation failed after ${this.maxAttempts} attempts`, error);
      throw error;
    }
  }
}

// Default RetryManager instance with common settings
export const retryManager = new RetryManager(3, 1000); // 3 attempts with 1 second delay