import { Event } from './models';

export class EventValidator {
  constructor() {}

  validate(event: any): void {
    if (!event || typeof event !== 'object') {
      throw new Error('Invalid event format');
    }

    if (!event.id || typeof event.id !== 'string') {
      throw new Error('Event must have a valid id');
    }

    if (!event.tipo || typeof event.tipo !== 'string') {
      throw new Error('Event must have a valid tipo');
    }

    if (!event.payload || typeof event.payload !== 'object') {
      throw new Error('Event must have a valid payload');
    }

    if (!event.timestamp || !(event.timestamp instanceof Date)) {
      throw new Error('Event must have a valid timestamp');
    }
  }
}