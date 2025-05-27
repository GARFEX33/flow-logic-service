import { z } from 'zod';

// Define the Zod schema for the Event model
export const eventSchema = z.object({
  id: z.string(),
  tipo: z.string(),
  payload: z.any(),
  timestamp: z.date(),
});

// Define the Zod schema for the FlujoEjecutado model
export const flujoEjecutadoSchema = z.object({
  id: z.string(),
  tipo_evento: z.string(),
  payload: z.any(),
  estado: z.enum(['recibido', 'en_proceso', 'procesado', 'fallido']),
  timestamp: z.date(),
  error: z.string().optional(),
});

// Export type inference from the schemas
export type Event = z.infer<typeof eventSchema>;
export type FlujoEjecutado = z.infer<typeof flujoEjecutadoSchema>;