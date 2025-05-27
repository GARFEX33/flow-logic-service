declare module 'async-retry' {
  export interface Options {
    retries?: number;
    factor?: number;
    minTimeout?: number;
    maxTimeout?: number;
    randomize?: boolean;
    [key: string]: any;
  }

  export default function asyncRetry<T>(
    fn: () => Promise<T>,
    options?: Options
  ): Promise<T>;
}