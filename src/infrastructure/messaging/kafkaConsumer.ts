import { Kafka, Consumer, ConsumerRunConfig, ConsumerConfig, Message } from 'kafkajs';
import { config } from '../../config';
import logger from '../../config/logger';
import { flujoOrchestrator } from '../../application/flujoOrchestrator';

// Create a Kafka instance
const kafka = new Kafka({
  clientId: 'flow-logic-service',
  brokers: [config.BROKER_URL],
});

// Create a consumer instance
const consumer = kafka.consumer({ groupId: 'flow-logic-service-group' });

// Function to connect the consumer
export async function connectConsumer() {
  try {
    await consumer.connect();
    logger.info('Kafka consumer connected successfully');
  } catch (error) {
    logger.error('Error connecting to Kafka consumer:', error);
    process.exit(1);
  }
}

// Function to disconnect the consumer
export async function disconnectConsumer() {
  await consumer.disconnect();
  logger.info('Kafka consumer disconnected');
}

// Function to subscribe to topics and process messages
export async function subscribeToTopics(topics: string[]) {
  await consumer.subscribe({ topics, fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        logger.info(
          `Received message: ${message.value?.toString() || ''} ` +
          `from topic: ${topic} partition: ${partition}`
        );

        // Extract event data from Kafka message
        const eventData = message.value ? JSON.parse(message.value.toString()) : {};

        // Create event object
        const event = {
          type: eventData.type,
          payload: eventData.payload,
          metadata: eventData.metadata
        };

        // Record initial flow state if using audit DB
        // await flowStateManager.recordReceived(event.id);

        // Process event through orchestrator
        await flujoOrchestrator.processEvent(event, eventData.flowId);

        logger.info(`Event ${event.type} processed successfully`);
      } catch (error) {
        logger.error(`Error processing message from topic ${topic}:`, error);
      }
    },
  } as ConsumerRunConfig);
}

// Export the consumer for use in other modules
export default consumer;