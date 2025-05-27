import { flujoEjecutadoRepository } from '../infrastructure/database/flujoEjecutadoRepository';
import logger from '../config/logger';

// FlowStateManager class to handle state transitions
export class FlowStateManager {
  // Start processing a flow (recibido -> en_proceso)
  async startProcessing(flowId: string): Promise<void> {
    try {
      // Update state to 'en_proceso'
      await flujoEjecutadoRepository.updateFlowState(flowId, 'en_proceso');
      logger.info(`Flow ${flowId} state updated to 'en_proceso'`);

      // Additional logic for starting processing can be added here
    } catch (error) {
      logger.error(`Error starting processing for flow ${flowId}`, error);
      throw error;
    }
  }

  // Complete processing (en_proceso -> procesado)
  async completeProcessing(flowId: string): Promise<void> {
    try {
      // Update state to 'procesado'
      await flujoEjecutadoRepository.updateFlowState(flowId, 'procesado');
      logger.info(`Flow ${flowId} state updated to 'procesado'`);

      // Additional logic for completing processing can be added here
    } catch (error) {
      logger.error(`Error completing processing for flow ${flowId}`, error);
      throw error;
    }
  }

  // Fail processing (en_proceso -> fallido)
  async failProcessing(flowId: string, errorDetails: string): Promise<void> {
    try {
      // Update state to 'fallido' with error details
      await flujoEjecutadoRepository.updateFlowState(flowId, 'fallido', errorDetails);
      logger.error(`Flow ${flowId} state updated to 'fallido' with error: ${errorDetails}`);

      // Additional logic for handling failures can be added here
    } catch (error) {
      logger.error(`Error updating failure state for flow ${flowId}`, error);
      throw error;
    }
  }
}

// Export a singleton instance of the FlowStateManager
export const flowStateManager = new FlowStateManager();