import { Event } from '../domain/models';

// Define the handler function type
export type EventHandler = (event: Event) => Promise<void>;

// Define the HandlerRegistry interface
export interface HandlerRegistry {
  registerHandler(eventType: string, handler: EventHandler): void;
  getHandler(eventType: string): EventHandler | undefined;
}

// Implement the HandlerRegistry class
export class HandlerRegistryImpl implements HandlerRegistry {
  private handlers: Map<string, EventHandler>;

  constructor() {
    this.handlers = new Map();
  }

  registerHandler(eventType: string, handler: EventHandler): void {
    this.handlers.set(eventType, handler);
  }

  getHandler(eventType: string): EventHandler | undefined {
    return this.handlers.get(eventType);
  }
}

// Export a singleton instance of the registry
export const handlerRegistry = new HandlerRegistryImpl();