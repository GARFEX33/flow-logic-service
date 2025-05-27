export interface Event {
  id: string;
  tipo: string;
  payload: any;
  timestamp: Date;
}

export interface FlujoEjecutado {
  id: string;
  tipo_evento: string;
  payload: any;
  estado: 'recibido' | 'en_proceso' | 'procesado' | 'fallido';
  timestamp: Date;
  error?: string;
}