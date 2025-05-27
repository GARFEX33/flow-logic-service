import { EventValidator } from '../domain/eventValidator';
import { HandlerRegistry, HandlerRegistryImpl } from '../application/handlerRegistry';
import { FlowStateManager } from './flowStateManager';
import { retryManager } from '../infrastructure/utils/retryManager';
import logger from '../config/logger';

// FlujoOrchestrator class to manage event processing
export class FlujoOrchestrator {
  constructor(
    private eventValidator: EventValidator,
    private handlerRegistry: HandlerRegistry,
    private flowStateManager: FlowStateManager
  ) {}

  // Main method to process an event
  async processEvent(event: any, flowId: string): Promise<void> {
    try {
      // Validate the event
      this.eventValidator.validate(event);

      // Get the handler for the event type
      const handler = this.handlerRegistry.getHandler(event.type);
      if (!handler) {
        throw new Error(`No handler found for event type: ${event.type}`);
      }

      // Start processing the flow
      await this.flowStateManager.startProcessing(flowId);

      // Execute the handler with retry logic for external calls
      await retryManager.execute(async () => {
        await handler(event);
      });

      // Complete processing
      await this.flowStateManager.completeProcessing(flowId);
    } catch (error) {
      // Log the error
      logger.error(`Error processing event ${event.type}:`, error);

      // Update flow state to failed
      await this.flowStateManager.failProcessing(flowId, (error as Error).message);
      throw error;
    }
  }
}

// Export a singleton instance of the orchestrator
export const flujoOrchestrator = new FlujoOrchestrator(
  new EventValidator(),
  new HandlerRegistryImpl(),
  new FlowStateManager()
);