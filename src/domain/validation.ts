import { eventSchema, flujoEjecutadoSchema } from './eventSchema';

// Function to validate an event object
export function validateEvent(event: unknown) {
  try {
    return eventSchema.parse(event);
  } catch (error) {
    throw new Error(`Invalid event: ${(error as { errors: { message: string }[] }).errors.map(e => e.message).join(', ')}`);
  }
}

// Function to validate a FlujoEjecutado object
export function validateFlujoEjecutado(flujo: unknown) {
  try {
    return flujoEjecutadoSchema.parse(flujo);
  } catch (error) {
    throw new Error(`Invalid flujo: ${(error as { errors: { message: string }[] }).errors.map(e => e.message).join(', ')}`);
  }
}