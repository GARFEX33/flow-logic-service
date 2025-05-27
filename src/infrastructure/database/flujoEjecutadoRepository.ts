import { Pool } from 'pg';
type PoolType = typeof Pool;
import { config } from '../../config';
import logger from '../../config/logger';

// Initialize the database connection pool if AUDIT_DB_URL is provided
let dbPool: PoolType | null = null;

if (config.AUDIT_DB_URL) {
  dbPool = new Pool({
    connectionString: config.AUDIT_DB_URL,
  });

  dbPool.on('error', (err: Error) => {
    logger.error('Unexpected error on idle database connection', err);
  });
}

// FlujoEjecutadoRepository class for database operations
export class FlujoEjecutadoRepository {
  // Save a new flow record with 'recibido' state
  async saveFlow(flowId: string, flowData: Record<string, any>): Promise<void> {
    if (!dbPool) {
      logger.warn('Database connection not available, skipping saveFlow');
      return;
    }

    const client = await dbPool.connect();
    try {
      await client.query(
        'INSERT INTO flujo_ejecutado (id, data, estado) VALUES ($1, $2, $3)',
        [flowId, JSON.stringify(flowData), 'recibido']
      );
    } finally {
      client.release();
    }
  }

  // Update flow state and error details
  async updateFlowState(flowId: string, newState: string, errorDetails?: string): Promise<void> {
    if (!dbPool) {
      logger.warn('Database connection not available, skipping updateFlowState');
      return;
    }

    const client = await dbPool.connect();
    try {
      await client.query(
        'UPDATE flujo_ejecutado SET estado = $1, error_details = $2 WHERE id = $3',
        [newState, errorDetails || null, flowId]
      );
    } finally {
      client.release();
    }
  }
}

// Export a singleton instance of the repository
export const flujoEjecutadoRepository = new FlujoEjecutadoRepository();